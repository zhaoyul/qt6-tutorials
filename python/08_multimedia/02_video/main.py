#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Multimedia Video Demo

Lists available video input devices.

Main classes:
- QMediaDevices: Access to multimedia device information
- QCameraDevice: Information about a camera device

Official documentation: https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QMediaDevices.html
"""

import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices, QCameraDevice


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)

    print("=== Video Inputs ===")
    cameras = QMediaDevices.videoInputs()
    if not cameras:
        print("No video devices found.")
        return 0

    for camera in cameras:
        print(f" - {camera.description()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
