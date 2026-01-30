def run_block_1():
    try:
        from PySide6.QtCore import QCoreApplication
        from PySide6.QtMultimedia import QMediaDevices
    except Exception as exc:
        print(f"[Audio] QtMultimedia unavailable: {exc}")
        return

    app = QCoreApplication([])
    outputs = QMediaDevices.audioOutputs()
    for device in outputs:
        print(f' - {device.description()}')

def run_block_2():
    try:
        from PySide6.QtMultimedia import QMediaDevices
    except Exception as exc:
        print(f"[Audio] QtMultimedia unavailable: {exc}")
        return

    inputs = QMediaDevices.audioInputs()
    for device in inputs:
        print(f' - {device.description()}')
