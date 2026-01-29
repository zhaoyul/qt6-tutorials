#!/usr/bin/env clojure -M
;; Qt6 Multimedia Camera Demo
;;
;; Shows basic camera device information.

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn position-to-string
  "Convert camera position to string."
  [pos]
  (cond
    (= pos 1) "Front"    ; QCameraDevice.Position.FrontFace
    (= pos 2) "Back"     ; QCameraDevice.Position.BackFace
    :else "Unspecified"))

(defn show-camera-info
  "Shows basic camera device information."
  []
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices, QCameraDevice

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
"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Camera Demo ===\n")
  
  (show-camera-info)
  
  (println "\n=== Done ==="))

(-main)
