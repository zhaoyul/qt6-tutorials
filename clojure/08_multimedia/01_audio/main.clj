#!/usr/bin/env clojure -M
;; Qt6 Multimedia Audio Demo
;;
;; Lists available audio input and output devices.

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "08_multimedia/01_audio"
                '[embedded :as py-embedded :bind-ns :reload])

(defn list-audio-devices
  "Lists available audio input and output devices."
  []
  (println "=== Audio Outputs ===")
  (py/call-attr py-embedded "run_block_1")

  (println "\n=== Audio Inputs ===")
  (py/call-attr py-embedded "run_block_2"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Audio Demo ===\n")
  
  (list-audio-devices)
  
  (println "\n=== Done ==="))

(-main)
