#!/usr/bin/env clojure -M
;; PySide6 Qt3D Basics Demo (Clojure + libpython-clj)
;;
;; Shows a simple 3D scene with:
;; - A rotating sphere with Phong material
;; - Orbit camera controller
;; - Point light
;; - Property animation

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; Import Python modules
(require-python '[PySide6.QtGui :as QtGui :bind-ns])
(require-python :from "11_3d/01_basics"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

;; Get classes
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QColor (py/get-attr QtGui "QColor"))
(def QVector3D (py/get-attr QtGui "QVector3D"))
(def QQuaternion (py/get-attr QtGui "QQuaternion"))
(def QPropertyAnimation (py/get-attr QtCore "QPropertyAnimation"))

(defn- import-qt3d-module
  [module-name]
  (try
    (py/import-module module-name)
    (catch Exception exc
      (println (str module-name " 模块不可用: " (.getMessage exc)))
      nil)))

(defn -main
  [& args]
  (println "=== PySide6 Qt3D Basics Demo (Clojure) ===")
  (let [qt3d-extras (import-qt3d-module "PySide6.Qt3DExtras")
        qt3d-core (import-qt3d-module "PySide6.Qt3DCore")
        qt3d-render (import-qt3d-module "PySide6.Qt3DRender")]
    (when (and qt3d-extras qt3d-core qt3d-render)
      ;; Initialize application
      (py/call-attr py-embedded "run_block_1")
      
      (let [Qt3DWindow (py/get-attr qt3d-extras "Qt3DWindow")
            QSphereMesh (py/get-attr qt3d-extras "QSphereMesh")
            QPhongMaterial (py/get-attr qt3d-extras "QPhongMaterial")
            QOrbitCameraController (py/get-attr qt3d-extras "QOrbitCameraController")
            QEntity (py/get-attr qt3d-core "QEntity")
            QTransform (py/get-attr qt3d-core "QTransform")
            QPointLight (py/get-attr qt3d-render "QPointLight")
            ; Create 3D window
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
        (py/call-attr (py/get-attr py-embedded "app") "exec")))))

(-main)
