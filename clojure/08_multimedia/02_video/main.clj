#!/usr/bin/env clojure -M
;; Qt6 Multimedia Video Demo
;;
;; Lists available video input devices.

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn list-video-devices
  "Lists available video input devices."
  []
  (println "=== Video Inputs ===")
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices

app = QCoreApplication([])

cameras = QMediaDevices.videoInputs()
if not cameras:
    print('No video devices found.')
else:
    for camera in cameras:
        print(f' - {camera.description()}')
"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Video Demo ===\n")
  
  (list-video-devices)
  
  (println "\n=== Done ==="))

(-main)
