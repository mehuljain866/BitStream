# BitStream

BitStream is an experimental desktop application that stores file archives in lossless video frames. It supports direct pixel-byte storage and an LSB steganography mode using a cover video.

**Important:** Treat this as an experimental format, not as your only backup. Test recovery on your own OpenCV/FFmpeg build before relying on it for important data.

## Downloads

Tagged releases publish standalone builds for Windows, macOS and Linux. See [GitHub Releases](https://github.com/mehuljain866/BitStream/releases). Development builds are available from [GitHub Actions](https://github.com/mehuljain866/BitStream/actions).

## Features

- Modern PySide6 desktop interface with drag-and-drop file input.
- File and folder archiving into ZIP.
- Normal mode: stores container bytes in FFV1 video frame channels.
- Steganography mode: embeds the container as least-significant bits in cover-video frames.
- Versioned container header with payload length and SHA-256 verification.
- ZIP CRC checks and guarded extraction paths.
- Optional post-extraction file sorting.
- Background encoding and extraction with live progress updates.

## Requirements

- Python 3.10+
- FFmpeg/OpenCV build with FFV1 encoder and decoder support
- Windows, macOS or Linux with a graphical desktop

Install:

```bash
git clone https://github.com/mehuljain866/BitStream.git
cd BitStream
python -m pip install -r requirements.txt
python main.py
```

On Windows, `run_bitstream.bat` can launch the Python application using the Python launcher or `python` from PATH. It no longer depends on a machine-specific installation path.

## Use

### Encode

1. Open the **Encode** workspace.
2. Add files or folders, or drag them into the application.
3. Open **Settings** to select resolution, FPS and normal/steganography mode.
4. In steganography mode, select a cover video with sufficient capacity.
5. Select **Encode video**. The result is saved under `output/encoded_video`.

### Decode

1. Open the **Decode** workspace.
2. Select a BitStream video.
3. Select **Verify & Extract**. Recovered files are written to `output/extracted_files`.

The decoder identifies normal versus steganographic mode from the embedded header; the current settings toggle does not need to match the mode used to encode.

## Container format v1

The payload begins with a 50-byte header:

| Field | Size |
|---|---:|
| Magic (`BSTREAM1`) | 8 bytes |
| Version | 1 byte |
| Mode (0 normal, 1 LSB) | 1 byte |
| ZIP payload length | 8 bytes, big-endian |
| SHA-256 of ZIP payload | 32 bytes |

Normal mode writes these bytes directly to frame channels. LSB mode writes one payload bit per frame channel. Unused capacity is padding and is not included in the recovered payload.

## Tests

Run the format and extraction safety tests with:

```bash
python -m unittest discover -s tests -v
```

These tests cover header parsing, truncation, checksums and ZIP path traversal. They do not replace real codec round-trip tests on each supported operating system.

## Limitations

- FFV1 availability depends on the installed OpenCV/FFmpeg build.
- Steganography capacity is limited by the number of cover-video frames and their dimensions.
- LSB embedding changes pixel values and is not robust to lossy transcoding, resizing, frame-rate conversion or platform video processing.
- A video re-encoded by a social platform or ordinary lossy editor may no longer be recoverable.
- This is not encryption. Anyone who knows the format can extract the embedded data. Encrypt sensitive archives separately before encoding.
- The extraction safety limit is currently 20 GiB of uncompressed ZIP contents.

## License

The repository currently includes an MIT `LICENSE` file. Documentation is also covered by that repository license unless a separate documentation license is added.
