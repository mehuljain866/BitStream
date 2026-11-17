# BitStream

BitStream is an experimental desktop application that stores file archives in lossless video frames. It supports direct pixel-byte storage and an LSB steganography mode using a cover video.

**Important:** Treat this as an experimental format, not as your only backup. Test recovery on your own OpenCV/FFmpeg build before relying on it for important data.

## 📦 Downloads (Standalone Executables)

Pre-built, standalone binaries are automatically built and downloadable for all major platforms:

| Platform | Download | Format | Description |
|---|---|---|---|
| **Windows** | [Download BitStream-Windows.exe](https://github.com/mehuljain866/BitStream/releases/latest) | Standalone `.exe` | No Python required. Double-click to run. |
| **macOS** | [Download BitStream-macOS.zip](https://github.com/mehuljain866/BitStream/releases/latest) | App Bundle / Binary | Unzip and run on macOS (Apple Silicon / Intel). |
| **Linux** | [Download BitStream-Linux](https://github.com/mehuljain866/BitStream/releases/latest) | Linux Binary | `chmod +x BitStream-Linux && ./BitStream-Linux` |

> *You can also download the latest automated build artifacts directly from the [GitHub Actions tab](https://github.com/mehuljain866/BitStream/actions).*

## Features

- File and folder archiving into ZIP.
- Normal mode: stores the container bytes in FFV1 video frame channels.
- Steganography mode: embeds the same container as least-significant bits in cover-video frames.
- Versioned container header with payload length and SHA-256 verification.
- ZIP CRC checks and guarded extraction paths.
- Optional post-extraction file sorting.
- Progress updates from the encoding/decoding worker.

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

## Use

1. Open **Files** and select files or a folder.
2. In Settings, select resolution/FPS and choose normal or steganography mode.
3. For steganography, upload a readable cover video.
4. Press the upper **convert** button to encode.
5. Output videos are saved under `output/encoded_video`.
6. Press the lower **convert** button and select a BitStream video to recover its contents into `output/extracted_files`.

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
- A video that has been re-encoded by a social platform or ordinary lossy editor may no longer be recoverable.
- This is not encryption. Anyone who knows the format can extract the embedded data. Encrypt sensitive archives separately before encoding.
- The extraction safety limit is currently 20 GiB of uncompressed ZIP contents.

## License

The repository currently includes an MIT `LICENSE` file. Documentation is also covered by that repository license unless a separate documentation license is added.
