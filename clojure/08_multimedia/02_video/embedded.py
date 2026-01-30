def run_block_1():
    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtMultimedia import QMediaDevices
    except Exception as exc:
        print(f"[Video] QtMultimedia unavailable: {exc}")
        return

    app = QCoreApplication([])
    cameras = QMediaDevices.videoInputs()
    if not cameras:
        print('No video devices found.')
    else:
        for camera in cameras:
            print(f' - {camera.description()}')
