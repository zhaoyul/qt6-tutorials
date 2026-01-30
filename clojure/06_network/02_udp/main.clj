#!/usr/bin/env clojure -M
;; PySide6 UDP 通信示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "06_network/02_udp"
                '[embedded :as py-embedded :bind-ns :reload])

(defn -main
  [& args]
  (println "=== PySide6 UDP 通信示例 (Clojure) ===")

  (py/call-attr py-embedded "run_block_1")

  (println "\n=== 完成 ==="))

(-main)
