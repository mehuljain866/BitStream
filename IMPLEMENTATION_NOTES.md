# BitStream PySide6 UI redesign bundle

This bundle replaces the Tkinter/CustomTkinter front end with a PySide6 desktop interface while retaining `index.py` as the existing encoding/extraction backend.

## Files to replace

- `main.py`
- `requirements.txt`
- `README.md`
- `.github/workflows/build-executables.yml`
- `run_bitstream.bat`

`index.py` is intentionally unchanged. The backend is imported by the new UI and its `encode`, `extract`, settings, and storage-directory interfaces are retained.

## Install and run

```bash
python -m pip install -r requirements.txt
python main.py
```

## Notes

- The interface requires a graphical desktop session.
- The existing backend still imports `tkinter.filedialog` at module import time, so Linux environments and build runners need the Tk system package (`python3-tk`) even though the new UI itself is PySide6.
- The CI workflow now runs the existing regression tests before packaging. These tests do not yet constitute real FFV1 codec round-trip tests.
- The workflow publishes release assets only for version tags (`v*`), rather than creating or overwriting a release on every push to `main`.
- PySide6 packaging is configured through PyInstaller collection flags; platform-specific runtime validation is still required.
