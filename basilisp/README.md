# PySide6 Qt6 Tutorials - Basilisp

This folder provides Basilisp rewrites that mirror the Python examples.

## Requirements

- Python 3.9+
- PySide6 (`pip install pyside6`)
- Basilisp (`pip install basilisp`)

## Run an example

From the repo root:

```bash
PYTHONPYCACHEPREFIX=/tmp/pycache conda run -n qt6-py python -m basilisp.cli run basilisp/01_core/01_meta_object/main.lpy
```

Or from the example directory:

```bash
cd basilisp/01_core/01_meta_object
PYTHONPYCACHEPREFIX=/tmp/pycache conda run -n qt6-py python -m basilisp.cli run main.lpy
```

Notes:
- The Basilisp examples are written directly against PySide6 (no `runpy`).
- QML/Quick demos load QML files from the `python/` tree, so run them from the
  repo root to keep relative paths consistent.

## Structure

The directory layout matches `python/` one-to-one:

```
basilisp/
├── 01_core/
├── 02_gui/
├── 03_widgets/
├── 04_qml/
├── 05_quick/
├── 06_network/
├── 07_sql/
├── 09_test/
└── 10_concurrent/
```
