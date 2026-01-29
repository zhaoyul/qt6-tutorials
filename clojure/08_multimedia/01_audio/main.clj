#!/usr/bin/env clojure -M
;; Qt6 Multimedia Audio Demo
;;
;; Lists available audio input and output devices.

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn list-audio-devices
  "Lists available audio input and output devices."
  []
  (println "=== Audio Outputs ===")
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication
from PySide6.QtMultimedia import QMediaDevices

app = QCoreApplication([])

outputs = QMediaDevices.audioOutputs()
for device in outputs:
    print(f' - {device.description()}')
")

  (println "\n=== Audio Inputs ===")
  (py/run-simple-string "
from PySide6.QtMultimedia import QMediaDevices

inputs = QMediaDevices.audioInputs()
for device in inputs:
    print(f' - {device.description()}')
"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Audio Demo ===\n")
  
  (list-audio-devices)
  
  (println "\n=== Done ==="))

(-main)
