#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Multimedia Audio Demo

Lists available audio input and output devices.

Main classes:
- QMediaDevices: Access to audio device information
- QAudioDevice: Information about an audio device

Official documentation: https://doc.qt.io/qtforpython/PySide6/QtMultimedia/QMediaDevices.html
"""

import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices, QAudioDevice


def main():
    """主函数"""
    app = QCoreApplication(sys.argv)

    print("=== Audio Outputs ===")
    outputs = QMediaDevices.audioOutputs()
    for device in outputs:
        print(f" - {device.description()}")

    print("\n=== Audio Inputs ===")
    inputs = QMediaDevices.audioInputs()
    for device in inputs:
        print(f" - {device.description()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
