#!/usr/bin/env clojure -M
;; PySide6 WebSocket 客户端示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "06_network/04_websocket"
                '[embedded :as py-embedded :bind-ns :reload])

(defn- create-websocket-client
  "创建 WebSocket 客户端"
  []
  (py/call-attr py-embedded "run_block_1")
  nil)

(defn- get-client
  "获取 Python 客户端对象"
  []
  (py/get-attr py-embedded "client"))

(defn -main
  [& args]
  (println "=== PySide6 WebSocket 客户端示例 (Clojure) ===\n")
  
  ;; 创建客户端
  (create-websocket-client)
  
  ;; 获取服务器 URL
  (let [server-url (if (seq args)
                     (first args)
                     "wss://echo.websocket.org/")]
    
    (println (str "使用服务器: " server-url))
    (println "可以通过命令行参数指定其他服务器，例如:")
    (println "  clojure -M:run 06_network/04_websocket/main.clj ws://localhost:8080\n")
    
    ;; 设置服务器 URL 并连接
    (py/call-attr py-embedded "run_block_5" server-url)
    
    ;; 启动事件循环
    (py/call-attr py-embedded "run_block_4")))

(-main)
