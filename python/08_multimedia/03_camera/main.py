#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Multimedia Camera Demo

Shows basic camera device information.

Main classes:
- QMediaDevices: Access to multimedia device information
- QCameraDevice: Information about a camera device
- QCameraDevice.Position: Camera position (FrontFace, BackFace, Unspecified)

Official documentation: https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QCameraDevice.html
"""

import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices, QCameraDevice


def position_to_string(pos: QCameraDevice.Position) -> str:
    """Convert camera position enum to string representation."""
    if pos == QCameraDevice.Position.FrontFace:
        return "Front"
    elif pos == QCameraDevice.Position.BackFace:
        return "Back"
    else:
        return "Unspecified"


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)

    cameras = QMediaDevices.videoInputs()
    if not cameras:
        print("No camera devices found.")
        return 0

    camera = cameras[0]
    print(f"Default camera: {camera.description()}")
    print(f"Position: {position_to_string(camera.position())}")
    print(f"Supports photo resolutions: {len(camera.photoResolutions())}")
    print(f"Supports video formats: {len(camera.videoFormats())}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
