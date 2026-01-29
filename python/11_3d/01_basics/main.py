#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Qt3D Basics Demo

Shows a simple 3D scene with:
- A rotating sphere with Phong material
- Orbit camera controller
- Point light
- Property animation

官方文档: https://doc.qt.io/qtforpython/PySide6/Qt3DCore/QEntity.html
"""

import sys
from PySide6.QtGui import (
    QGuiApplication,
    QColor,
    QVector3D,
    QQuaternion
)
from PySide6.Qt3DExtras import (
    Qt3DWindow,
    QSphereMesh,
    QPhongMaterial,
    QOrbitCameraController
)
from PySide6.Qt3DCore import QEntity, QTransform
from PySide6.Qt3DRender import QPointLight
from PySide6.QtCore import QPropertyAnimation, Property


def main():
    """主函数"""
    app = QGuiApplication(sys.argv)

    # Create 3D window
    view = Qt3DWindow()
    view.setTitle("Qt 3D Basics")
    view.defaultFrameGraph().setClearColor(QColor(30, 30, 40))

    # Root entity
    root = QEntity()

    # Camera setup
    camera = view.camera()
    camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
    camera.setPosition(QVector3D(0.0, 0.0, 10.0))
    camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

    # Camera controller
    cam_controller = QOrbitCameraController(root)
    cam_controller.setCamera(camera)

    # Sphere entity
    sphere = QEntity(root)
    
    # Sphere mesh
    mesh = QSphereMesh()
    mesh.setRadius(1.5)

    # Phong material
    material = QPhongMaterial()
    material.setDiffuse(QColor(0, 170, 255))
    material.setSpecular(QColor(255, 255, 255))
    material.setShininess(80.0)

    # Transform for sphere
    transform = QTransform()

    sphere.addComponent(mesh)
    sphere.addComponent(material)
    sphere.addComponent(transform)

    # Light entity
    light_entity = QEntity(root)
    light = QPointLight(light_entity)
    light.setColor(QColor(255, 255, 255))
    light.setIntensity(1.0)
    light_transform = QTransform(light_entity)
    light_transform.setTranslation(QVector3D(6.0, 6.0, 6.0))
    light_entity.addComponent(light)
    light_entity.addComponent(light_transform)

    # Rotation animation
    spin = QPropertyAnimation(transform, b"rotation")
    spin.setStartValue(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 0.0))
    spin.setEndValue(QQuaternion.fromAxisAndAngle(QVector3D(0.0, 1.0, 0.0), 360.0))
    spin.setDuration(6000)
    spin.setLoopCount(-1)
    spin.start()

    view.setRootEntity(root)
    view.resize(800, 600)
    view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
