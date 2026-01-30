#!/usr/bin/env clojure -M
;; Qt6 Multimedia Video Demo
;;
;; Lists available video input devices.

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "08_multimedia/02_video"
                '[embedded :as py-embedded :bind-ns :reload])

(defn list-video-devices
  "Lists available video input devices."
  []
  (println "=== Video Inputs ===")
  (py/call-attr py-embedded "run_block_1"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Video Demo ===\n")
  
  (list-video-devices)
  
  (println "\n=== Done ==="))

(-main)
