"""BitStream storage engine.

Container v1 stores a fixed binary header followed by a ZIP payload. In normal
mode the bytes are written directly into FFV1 frame channels. In steganography
mode the same container bytes are written into the least-significant bits of
cover-video channels. The decoder detects the mode from the header signature.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from tkinter import filedialog
from typing import Callable, Optional

import cv2
import numpy as np

BASE = Path(__file__).resolve().parent
INPUT_DIR = BASE / "input" / "folder_to_encode"
OUTPUT_VIDEO = BASE / "output" / "encoded_video"
OUTPUT_EXTRACT = BASE / "output" / "extracted_files"
COVER_DIR = BASE / "cover_video"
SETTINGS_FILE = BASE / "settings.json"

for directory in (INPUT_DIR, OUTPUT_VIDEO, OUTPUT_EXTRACT, COVER_DIR):
    directory.mkdir(parents=True, exist_ok=True)

MAGIC = b"BSTREAM1"
FORMAT_VERSION = 1
# magic(8), version(1), mode(1), payload length(8), sha256(32)
HEADER_SIZE = 50
MODE_NORMAL = 0
MODE_STEG = 1
DEFAULT_SETTINGS = {
    "resolution": "256x256",
    "fps": 24,
    "steganography": False,
    "auto_sort": False,
}
ALLOWED_RESOLUTIONS = {"256x256", "512x512", "1024x1024", "1920x1080"}
ALLOWED_FPS = {15, 24, 30, 60}


def _progress(callback, value: float, message: str) -> None:
    if callback:
        callback(max(0.0, min(1.0, float(value))), message)


def _validated_settings(raw) -> dict:
    result = dict(DEFAULT_SETTINGS)
    if not isinstance(raw, dict):
        return result
    resolution = raw.get("resolution")
    if resolution in ALLOWED_RESOLUTIONS:
        result["resolution"] = resolution
    try:
        fps = int(raw.get("fps", DEFAULT_SETTINGS["fps"]))
        if fps in ALLOWED_FPS:
            result["fps"] = fps
    except (TypeError, ValueError):
        pass
    for key in ("steganography", "auto_sort"):
        if isinstance(raw.get(key), bool):
            result[key] = raw[key]
    return result


def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    try:
        return _validated_settings(json.loads(SETTINGS_FILE.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        # Preserve a damaged file for diagnosis instead of silently overwriting it.
        return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> None:
    validated = _validated_settings(settings)
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="settings_", suffix=".tmp", dir=SETTINGS_FILE.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(validated, stream, indent=4)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, SETTINGS_FILE)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def get_resolution() -> tuple[int, int]:
    width, height = load_settings()["resolution"].split("x")
    return int(width), int(height)


def is_steg_enabled() -> bool:
    return load_settings()["steganography"]


def _clear_directory(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for item in directory.iterdir():
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink(missing_ok=True)


def upload_files():
    selected = filedialog.askopenfilenames(title="Select files")
    if not selected:
        return False
    _clear_directory(INPUT_DIR)
    for source in selected:
        source_path = Path(source)
        if not source_path.is_file():
            raise FileNotFoundError(f"Selected file does not exist: {source_path}")
        shutil.copy2(source_path, INPUT_DIR / source_path.name)
    return True


def upload_folder():
    selected = filedialog.askdirectory(title="Select folder")
    if not selected:
        return False
    source = Path(selected).resolve()
    if not source.is_dir():
        raise NotADirectoryError(source)
    _clear_directory(INPUT_DIR)
    destination = INPUT_DIR / source.name
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return True


def upload_cover_video():
    selected = filedialog.askopenfilename(
        title="Select cover video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov"), ("All files", "*.*")],
    )
    if not selected:
        return False
    source = Path(selected)
    if not source.is_file():
        raise FileNotFoundError(source)
    cap = cv2.VideoCapture(str(source))
    try:
        if not cap.isOpened():
            raise ValueError("OpenCV cannot open the selected cover video.")
        ok, frame = cap.read()
        if not ok or frame is None:
            raise ValueError("The selected cover video contains no readable frames.")
    finally:
        cap.release()
    _clear_directory(COVER_DIR)
    shutil.copy2(source, COVER_DIR / source.name)
    return True


def _create_archive() -> Path:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="bitstream_payload_", suffix=".zip", dir=BASE)
    os.close(fd)
    archive = Path(name)
    try:
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(INPUT_DIR.rglob("*")):
                if path.is_symlink():
                    raise ValueError(f"Symbolic links are not supported: {path}")
                if path.is_file():
                    zf.write(path, path.relative_to(INPUT_DIR).as_posix())
        return archive
    except Exception:
        archive.unlink(missing_ok=True)
        raise


def _make_container(archive_bytes: bytes, mode: int) -> bytes:
    digest = hashlib.sha256(archive_bytes).digest()
    header = MAGIC + bytes((FORMAT_VERSION, mode)) + len(archive_bytes).to_bytes(8, "big") + digest
    assert len(header) == HEADER_SIZE
    return header + archive_bytes


def _parse_container(data: bytes, expected_mode: Optional[int] = None) -> bytes:
    if len(data) < HEADER_SIZE:
        raise ValueError("Video does not contain a complete BitStream header.")
    if data[:8] != MAGIC:
        raise ValueError("This video does not contain a BitStream payload.")
    version, mode = data[8], data[9]
    if version != FORMAT_VERSION:
        raise ValueError(f"Unsupported BitStream format version: {version}")
    if mode not in (MODE_NORMAL, MODE_STEG):
        raise ValueError("Invalid BitStream encoding mode.")
    if expected_mode is not None and mode != expected_mode:
        raise ValueError("BitStream payload mode does not match the decoder.")
    length = int.from_bytes(data[10:18], "big")
    digest = data[18:50]
    if length > len(data) - HEADER_SIZE:
        raise ValueError("Video is truncated: declared payload is larger than recovered data.")
    payload = data[HEADER_SIZE:HEADER_SIZE + length]
    if hashlib.sha256(payload).digest() != digest:
        raise ValueError("Payload integrity check failed (SHA-256 mismatch).")
    return payload


def _open_writer(path: Path, fps: float, size: tuple[int, int]):
    writer = cv2.VideoWriter(
        str(path), cv2.VideoWriter_fourcc(*"FFV1"), float(fps), size
    )
    if not writer.isOpened():
        writer.release()
        raise RuntimeError(
            "Could not initialise an FFV1 video writer. Install an OpenCV build "
            "with FFV1 support, or use a compatible video backend."
        )
    return writer


def encode_normal(progress: Optional[Callable] = None) -> str:
    archive = _create_archive()
    out_path = OUTPUT_VIDEO / "encoded.avi"
    OUTPUT_VIDEO.mkdir(parents=True, exist_ok=True)
    temp_out = out_path.with_name(out_path.stem + ".partial.avi")
    try:
        payload = _make_container(archive.read_bytes(), MODE_NORMAL)
        width, height = get_resolution()
        fps = load_settings()["fps"]
        capacity = width * height * 3
        frames = math.ceil(len(payload) / capacity)
        writer = _open_writer(temp_out, fps, (width, height))
        try:
            for index in range(frames):
                chunk = payload[index * capacity:(index + 1) * capacity]
                frame_bytes = np.zeros(capacity, dtype=np.uint8)
                frame_bytes[:len(chunk)] = np.frombuffer(chunk, dtype=np.uint8)
                writer.write(frame_bytes.reshape((height, width, 3)))
                _progress(progress, (index + 1) / frames, f"Writing frame {index + 1}/{frames}")
        finally:
            writer.release()
        _verify_video_readable(temp_out, expected_frames=frames)
        # Verify the actual decoded channel bytes, not merely that a video exists.
        recovered = _read_normal_bytes(temp_out)
        _parse_container(recovered, MODE_NORMAL)
        if recovered[:len(payload)] != payload:
            raise RuntimeError(
                "The installed FFV1/OpenCV pipeline altered frame bytes. "
                "This build cannot safely encode BitStream normal-mode data."
            )
        os.replace(temp_out, out_path)
        return str(out_path)
    finally:
        archive.unlink(missing_ok=True)
        temp_out.unlink(missing_ok=True)


def _verify_video_readable(path: Path, expected_frames: Optional[int] = None) -> None:
    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            raise RuntimeError("Output video could not be reopened for verification.")
        count = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame is None:
                raise RuntimeError("Video decoder returned an empty frame.")
            count += 1
        if count == 0 or (expected_frames is not None and count != expected_frames):
            raise RuntimeError(
                f"Video verification failed: expected {expected_frames} frames, read {count}."
            )
    finally:
        cap.release()


def encode_steganography(progress: Optional[Callable] = None) -> str:
    covers = [p for p in COVER_DIR.iterdir() if p.is_file()]
    if not covers:
        raise FileNotFoundError("Upload a cover video before using steganography mode.")
    archive = _create_archive()
    cap = cv2.VideoCapture(str(covers[0]))
    OUTPUT_VIDEO.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_VIDEO / f"embedded_{covers[0].stem}.avi"
    temp_out = out_path.with_name(out_path.stem + ".partial.avi")
    writer = None
    try:
        container = _make_container(archive.read_bytes(), MODE_STEG)
        bits = np.unpackbits(np.frombuffer(container, dtype=np.uint8))
        if not cap.isOpened():
            raise ValueError("Could not open the selected cover video.")
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        if width <= 0 or height <= 0 or not math.isfinite(fps) or fps <= 0:
            raise ValueError("Cover video reports invalid dimensions or frame rate.")
        capacity = width * height * 3
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count > 0 and len(bits) > frame_count * capacity:
            raise ValueError(
                f"Payload does not fit: needs {len(bits)} bits, cover capacity is {frame_count * capacity} bits."
            )
        writer = _open_writer(temp_out, fps, (width, height))
        bit_index = 0
        total_frames = max(frame_count, 1)
        processed = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            flat = frame.reshape(-1)
            take = min(len(flat), len(bits) - bit_index)
            if take > 0:
                flat[:take] = (flat[:take] & 0xFE) | bits[bit_index:bit_index + take]
                bit_index += take
            writer.write(frame)
            processed += 1
            _progress(progress, min(processed / total_frames, 0.99), f"Embedding frame {processed}")
        if bit_index < len(bits):
            raise ValueError(
                f"Cover video is too short: embedded {bit_index} of {len(bits)} required bits."
            )
        cap.release()
        writer.release()
        cap = None
        writer = None
        _verify_video_readable(temp_out)
        # Confirm the encoded LSB stream survives the selected writer/decoder.
        recovered = _read_steg_bytes(temp_out)
        _parse_container(recovered, MODE_STEG)
        os.replace(temp_out, out_path)
        return str(out_path)
    finally:
        if cap is not None:
            cap.release()
        if writer is not None:
            writer.release()
        archive.unlink(missing_ok=True)
        temp_out.unlink(missing_ok=True)


def encode(progress: Optional[Callable] = None) -> str:
    result = encode_steganography(progress) if is_steg_enabled() else encode_normal(progress)
    _progress(progress, 1.0, "Encoding complete")
    return result


def _read_normal_bytes(video_path: Path, progress: Optional[Callable] = None) -> bytes:
    cap = cv2.VideoCapture(str(video_path))
    chunks = []
    try:
        if not cap.isOpened():
            raise ValueError("Could not open the selected video.")
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        count = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame is None or frame.ndim != 3 or frame.shape[2] != 3:
                raise ValueError("Video contains an unsupported frame format.")
            chunks.append(frame.reshape(-1).tobytes())
            count += 1
            if total:
                _progress(progress, count / total, f"Reading frame {count}/{total}")
    finally:
        cap.release()
    if not chunks:
        raise ValueError("Video contains no readable frames.")
    return b"".join(chunks)


def _read_steg_bytes(video_path: Path, progress: Optional[Callable] = None) -> bytes:
    cap = cv2.VideoCapture(str(video_path))
    bit_chunks = []
    try:
        if not cap.isOpened():
            raise ValueError("Could not open the selected video.")
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
        count = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if frame is None:
                raise ValueError("Video contains an unreadable frame.")
            bit_chunks.append((frame.reshape(-1) & 1).astype(np.uint8))
            count += 1
            if total:
                _progress(progress, count / total, f"Reading embedded frame {count}/{total}")
    finally:
        cap.release()
    if not bit_chunks:
        raise ValueError("Video contains no readable frames.")
    return np.packbits(np.concatenate(bit_chunks)).tobytes()


def _safe_extract(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive_path, "r") as zf:
        members = zf.infolist()
        total_uncompressed = sum(member.file_size for member in members)
        if total_uncompressed > 20 * 1024**3:
            raise ValueError("Archive exceeds the 20 GiB extraction safety limit.")
        for member in members:
            name = member.filename.replace("\\", "/")
            relative = PurePosixPath(name)
            if relative.is_absolute() or not relative.parts or any(
                part in ("", ".", "..") for part in relative.parts
            ):
                raise ValueError(f"Unsafe archive path rejected: {member.filename}")
            # Reject Unix symlinks and special file types.
            mode = (member.external_attr >> 16) & 0xFFFF
            if mode and not (mode & 0o170000) in (0, 0o100000, 0o040000):
                raise ValueError(f"Unsupported special file in archive: {member.filename}")
            target = (root / Path(*relative.parts)).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"Archive path escapes extraction directory: {member.filename}")
        zf.extractall(root)


def extract(video_path: Path, progress: Optional[Callable] = None) -> Path:
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError(video_path)
    raw = _read_normal_bytes(video_path, progress)
    try:
        archive_bytes = _parse_container(raw, MODE_NORMAL)
    except ValueError as normal_error:
        # A steganographic stream is represented as one bit per channel byte.
        try:
            steg_raw = _read_steg_bytes(video_path, progress)
            archive_bytes = _parse_container(steg_raw, MODE_STEG)
        except Exception as steg_error:
            raise ValueError(
                f"Not a valid BitStream video. Normal decode: {normal_error} "
                f"Steganography decode: {steg_error}"
            ) from steg_error

    fd, temp_name = tempfile.mkstemp(prefix="bitstream_recovered_", suffix=".zip", dir=OUTPUT_EXTRACT)
    os.close(fd)
    archive_path = Path(temp_name)
    try:
        archive_path.write_bytes(archive_bytes)
        # Test the archive before extracting any member.
        with zipfile.ZipFile(archive_path, "r") as zf:
            bad_member = zf.testzip()
            if bad_member:
                raise ValueError(f"Recovered ZIP failed CRC validation at {bad_member}.")
        _safe_extract(archive_path, OUTPUT_EXTRACT)
    finally:
        archive_path.unlink(missing_ok=True)

    if load_settings()["auto_sort"]:
        auto_sort(OUTPUT_EXTRACT)
    _progress(progress, 1.0, "Extraction complete")
    return OUTPUT_EXTRACT


def auto_sort(folder: Path) -> None:
    categories = {
        "Images": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff"},
        "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv"},
        "Programs": {".exe", ".apk", ".msi", ".bat", ".py", ".sh"},
        "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm"},
        "Audio": {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    }
    folder = Path(folder)
    for file in list(folder.iterdir()):
        if not file.is_file() or file.name == "recovered.zip":
            continue
        category = next((name for name, exts in categories.items()
                         if file.suffix.lower() in exts), "Others")
        target = folder / category
        target.mkdir(exist_ok=True)
        destination = target / file.name
        if destination.exists():
            destination = target / f"{file.stem}_{hashlib.sha1(str(file).encode()).hexdigest()[:8]}{file.suffix}"
        shutil.move(str(file), destination)
