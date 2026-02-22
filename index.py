import cv2
import numpy as np
import math
import zipfile
import shutil
import json
import os
from pathlib import Path
from tkinter import filedialog

# =====================================================
# BASE PATHS
# =====================================================

BASE = Path(__file__).parent
INPUT_DIR = BASE / "input/folder_to_encode"
OUTPUT_VIDEO = BASE / "output/encoded_video"
OUTPUT_EXTRACT = BASE / "output/extracted_files"
COVER_DIR = BASE / "cover_video"
SETTINGS_FILE = BASE / "settings.json"
TEMP_ARCHIVE = BASE / "temp_payload.zip"

# Ensure directories exist
for d in [INPUT_DIR, OUTPUT_VIDEO, OUTPUT_EXTRACT, COVER_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# =====================================================
# SETTINGS MANAGER
# =====================================================

DEFAULT_SETTINGS = {
    "resolution": "256x256",
    "fps": 24,
    "steganography": False,
    "auto_sort": False
}

def load_settings():
    """Safely load settings, restoring defaults if corrupt."""
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        print("Settings file corrupted. resetting defaults.")
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

def save_settings(settings):
    SETTINGS_FILE.write_text(json.dumps(settings, indent=4))

def get_resolution():
    s = load_settings()
    try:
        w, h = s["resolution"].split("x")
        return int(w), int(h)
    except:
        return 256, 256

def is_steg_enabled():
    return load_settings().get("steganography", False)

# =====================================================
# FILE OPERATIONS
# =====================================================

def upload_files():
    files = filedialog.askopenfilenames(title="Select files")
    if files:
        # Clear input dir first to avoid mixing previous files
        for f in INPUT_DIR.glob("*"):
            if f.is_file(): f.unlink()
        
        for f in files:
            shutil.copy(f, INPUT_DIR)
        return True
    return False

def upload_folder():
    folder = filedialog.askdirectory(title="Select folder")
    if folder:
        # Clear input dir
        for f in INPUT_DIR.glob("*"):
            try:
                if f.is_file(): f.unlink()
                else: shutil.rmtree(f)
            except: pass

        shutil.copytree(folder, INPUT_DIR / Path(folder).name, dirs_exist_ok=True)
        return True
    return False

def upload_cover_video():
    video = filedialog.askopenfilename(
        title="Select cover video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mkv")]
    )
    if video:
        # Clear old covers
        for f in COVER_DIR.glob("*"):
            f.unlink()
        shutil.copy(video, COVER_DIR)
        return True
    return False

# =====================================================
# ZIP LOGIC
# =====================================================

def zip_input():
    with zipfile.ZipFile(TEMP_ARCHIVE, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in INPUT_DIR.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(INPUT_DIR))

# =====================================================
# ENCODING LOGIC
# =====================================================

def encode_normal():
    WIDTH, HEIGHT = get_resolution()
    FPS = load_settings().get("fps", 24)

    zip_input()
    payload = TEMP_ARCHIVE.read_bytes()

    # Header: 8 bytes file size
    size_header = len(payload).to_bytes(8, 'big')
    payload = size_header + payload

    byte_array = np.frombuffer(payload, dtype=np.uint8)
    
    # Calculate capacity per frame
    capacity = WIDTH * HEIGHT * 3
    total_frames = math.ceil(len(byte_array) / capacity)
    
    out_path = OUTPUT_VIDEO / "encoded.avi"
    
    # FFV1 is a lossless codec (crucial for data integrity)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    video = cv2.VideoWriter(str(out_path), fourcc, FPS, (WIDTH, HEIGHT))

    idx = 0
    for _ in range(total_frames):
        chunk = byte_array[idx:idx+capacity]
        idx += capacity
        
        # Pad last chunk if needed
        if len(chunk) < capacity:
            chunk = np.pad(chunk, (0, capacity-len(chunk)), mode='constant')
            
        frame = chunk.reshape((HEIGHT, WIDTH, 3)).astype(np.uint8)
        video.write(frame)

    video.release()
    TEMP_ARCHIVE.unlink(missing_ok=True)
    return str(out_path)

def encode_steganography():
    cover_videos = list(COVER_DIR.glob("*"))
    if not cover_videos:
        raise FileNotFoundError("No cover video found.")

    cover = cover_videos[0]
    zip_input()
    payload = TEMP_ARCHIVE.read_bytes()
    
    size_header = len(payload).to_bytes(8, 'big')
    payload = size_header + payload
    
    # Convert payload to bits string
    # Optimization: using a generator or bitwise ops directly in loop is faster for huge files
    # but this is safer for readability.
    bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
    total_bits = len(bits)
    
    cap = cv2.VideoCapture(str(cover))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out_path = OUTPUT_VIDEO / f"embedded_{cover.stem}.avi"
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(str(out_path), fourcc, fps, (width, height))
    
    bit_idx = 0
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        if bit_idx < total_bits:
            flat = frame.flatten()
            available = len(flat)
            needed = total_bits - bit_idx
            
            take = min(available, needed)
            
            # Embed bits into LSB
            # Clear LSB
            flat[:take] &= 254 
            # Set LSB from payload
            flat[:take] |= bits[bit_idx : bit_idx+take]
            
            bit_idx += take
            frame = flat.reshape(frame.shape)
            
        out.write(frame)

    cap.release()
    out.release()
    TEMP_ARCHIVE.unlink(missing_ok=True)
    return str(out_path)

def encode():
    if is_steg_enabled():
        return encode_steganography()
    else:
        return encode_normal()

# =====================================================
# DECODING LOGIC
# =====================================================

def extract(video_path):
    cap = cv2.VideoCapture(str(video_path))
    
    # We need to read the first 64 bits (8 bytes) to know the file size
    # This naive implementation reads everything into memory. 
    # For large files, a streaming approach is better, but this fits the current logic.
    
    extracted_bits = []
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        flat = frame.flatten()
        # Extract LSB
        extracted_bits.append(flat & 1)
        
    cap.release()
    
    all_bits = np.concatenate(extracted_bits)
    
    # Reconstruct bytes
    # Pack bits back into bytes
    byte_data = np.packbits(all_bits)
    
    # Read Header (first 8 bytes)
    size_header = byte_data[:8]
    payload_size = int.from_bytes(size_header.tobytes(), 'big')
    
    # Extract payload
    payload = byte_data[8 : 8 + payload_size].tobytes()
    
    archive_path = OUTPUT_EXTRACT / "recovered.zip"
    archive_path.write_bytes(payload)
    
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(OUTPUT_EXTRACT)
    
    archive_path.unlink() # Cleanup zip
    
    if load_settings().get("auto_sort", False):
        auto_sort(OUTPUT_EXTRACT)

def auto_sort(folder):
    categories = {
        "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Programs": [".exe", ".apk", ".msi", ".bat", ".py"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Audio": [".mp3", ".wav", ".flac"]
    }
    
    for file in folder.iterdir():
        if file.is_file():
            found = False
            for cat, exts in categories.items():
                if file.suffix.lower() in exts:
                    target = folder / cat
                    target.mkdir(exist_ok=True)
                    try: shutil.move(str(file), target / file.name)
                    except: pass 
                    found = True
                    break
            if not found:
                target = folder / "Others"
                target.mkdir(exist_ok=True)
                try: shutil.move(str(file), target / file.name)
                except: pass