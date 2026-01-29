#!/usr/bin/env clojure -M
;; PySide6 Qt3D Basics Demo (Clojure + libpython-clj)
;;
;; Shows a simple 3D scene with:
;; - A rotating sphere with Phong material
;; - Orbit camera controller
;; - Point light
;; - Property animation

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; Import Python modules
(def QtGui (py/import-module "PySide6.QtGui"))
(def QtCore (py/import-module "PySide6.QtCore"))
(def Qt3DExtras (py/import-module "PySide6.Qt3DExtras"))
(def Qt3DCore (py/import-module "PySide6.Qt3DCore"))
(def Qt3DRender (py/import-module "PySide6.Qt3DRender"))

;; Get classes
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QColor (py/get-attr QtGui "QColor"))
(def QVector3D (py/get-attr QtGui "QVector3D"))
(def QQuaternion (py/get-attr QtGui "QQuaternion"))
(def Qt3DWindow (py/get-attr Qt3DExtras "Qt3DWindow"))
(def QSphereMesh (py/get-attr Qt3DExtras "QSphereMesh"))
(def QPhongMaterial (py/get-attr Qt3DExtras "QPhongMaterial"))
(def QOrbitCameraController (py/get-attr Qt3DExtras "QOrbitCameraController"))
(def QEntity (py/get-attr Qt3DCore "QEntity"))
(def QTransform (py/get-attr Qt3DCore "QTransform"))
(def QPointLight (py/get-attr Qt3DRender "QPointLight"))
(def QPropertyAnimation (py/get-attr QtCore "QPropertyAnimation"))

(defn -main
  [& args]
  (println "=== PySide6 Qt3D Basics Demo (Clojure) ===")
  
  ;; Initialize application
  (py/run-simple-string "
import sys
from PySide6.QtGui import QGuiApplication
app = QGuiApplication(sys.argv)
")
  
  (let [; Create 3D window
        view (Qt3DWindow)
        _ (py/call-attr view "setTitle" "Qt 3D Basics")
        _ (py/call-attr (py/call-attr view "defaultFrameGraph") "setClearColor" (QColor 30 30 40))
        
        ; Root entity
        root (QEntity)
        
        ; Camera setup
        camera (py/call-attr view "camera")
        _ (py/call-attr (py/call-attr camera "lens") "setPerspectiveProjection" 45.0 (/ 16.0 9.0) 0.1 1000.0)
        _ (py/call-attr camera "setPosition" (QVector3D 0.0 0.0 10.0))
        _ (py/call-attr camera "setViewCenter" (QVector3D 0.0 0.0 0.0))
        
        ; Camera controller
        cam-controller (QOrbitCameraController root)
        _ (py/call-attr cam-controller "setCamera" camera)
        
        ; Sphere entity
        sphere (QEntity root)
        
        ; Sphere mesh
        mesh (QSphereMesh)
        _ (py/call-attr mesh "setRadius" 1.5)
        
        ; Phong material
        material (QPhongMaterial)
        _ (py/call-attr material "setDiffuse" (QColor 0 170 255))
        _ (py/call-attr material "setSpecular" (QColor 255 255 255))
        _ (py/call-attr material "setShininess" 80.0)
        
        ; Transform for sphere
        transform (QTransform)
        
        ; Add components to sphere
        _ (py/call-attr sphere "addComponent" mesh)
        _ (py/call-attr sphere "addComponent" material)
        _ (py/call-attr sphere "addComponent" transform)
        
        ; Light entity
        light-entity (QEntity root)
        light (QPointLight light-entity)
        _ (py/call-attr light "setColor" (QColor 255 255 255))
        _ (py/call-attr light "setIntensity" 1.0)
        light-transform (QTransform light-entity)
        _ (py/call-attr light-transform "setTranslation" (QVector3D 6.0 6.0 6.0))
        _ (py/call-attr light-entity "addComponent" light)
        _ (py/call-attr light-entity "addComponent" light-transform)
        
        ; Rotation animation
        spin (QPropertyAnimation transform "rotation")
        _ (py/call-attr spin "setStartValue" (py/call-attr QQuaternion "fromAxisAndAngle" (QVector3D 0.0 1.0 0.0) 0.0))
        _ (py/call-attr spin "setEndValue" (py/call-attr QQuaternion "fromAxisAndAngle" (QVector3D 0.0 1.0 0.0) 360.0))
        _ (py/call-attr spin "setDuration" 6000)
        _ (py/call-attr spin "setLoopCount" -1)
        _ (py/call-attr spin "start")]
    
    ; Set root entity and show window
    (py/call-attr view "setRootEntity" root)
    (py/call-attr view "resize" 800 600)
    (py/call-attr view "show")
    
    (println "3D scene loaded. Close window to exit.")
    
    ; Execute application
    (py/call-attr (py/run-simple-string "app") "exec")))

(-main)
