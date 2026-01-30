def run_block_1():
    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtMultimedia import QMediaDevices, QCameraDevice
    except Exception as exc:
        print(f"[Camera] QtMultimedia unavailable: {exc}")
        return

    app = QCoreApplication([])
    cameras = QMediaDevices.videoInputs()
    if not cameras:
        print('No camera devices found.')
    else:
        camera = cameras[0]
        print(f'Default camera: {camera.description()}')
        position = camera.position()
        position_str = 'Front' if position == QCameraDevice.Position.FrontFace else ('Back' if position == QCameraDevice.Position.BackFace else 'Unspecified')
        print(f'Position: {position_str}')
        print(f'Supports photo resolutions: {len(camera.photoResolutions())}')
        print(f'Supports video formats: {len(camera.videoFormats())}')
