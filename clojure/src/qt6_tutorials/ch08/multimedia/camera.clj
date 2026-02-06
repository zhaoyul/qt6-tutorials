;; Qt6 Multimedia Camera Demo
;;
;; Shows basic camera device information.

(ns qt6_tutorials.ch08.multimedia.camera)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "08_multimedia/03_camera"
                '[embedded :as py-embedded :bind-ns :reload])

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
  (py/call-attr py-embedded "run_block_1"))

(defn -main
  [& args]
  (println "=== Qt6 Multimedia Camera Demo ===\n")

  (show-camera-info)

  (println "\n=== Done ==="))
