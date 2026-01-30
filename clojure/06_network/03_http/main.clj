#!/usr/bin/env clojure -M
;; PySide6 HTTP 网络请求示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "06_network/03_http"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtNetwork :as QtNetwork :bind-ns])

;; 获取类
(def QNetworkAccessManager (py/get-attr QtNetwork "QNetworkAccessManager"))
(def QNetworkRequest (py/get-attr QtNetwork "QNetworkRequest"))
(def QNetworkReply (py/get-attr QtNetwork "QNetworkReply"))
(def QUrl (py/get-attr QtCore "QUrl"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn demonstrate-http-get
  "HTTP GET 请求"
  []
  (println "\n=== HTTP GET 请求 ===")
  
  (py/call-attr py-embedded "run_block_2")
  
  (println "GET 请求完成"))

(defn demonstrate-http-post
  "HTTP POST 请求"
  []
  (println "\n=== HTTP POST 请求 ===")
  
  (py/call-attr py-embedded "run_block_3")
  
  (println "POST 请求完成"))

(defn demonstrate-async-http
  "异步 HTTP 请求"
  []
  (println "\n=== 异步 HTTP 请求 ===")
  
  (py/call-attr py-embedded "run_block_4")
  
  (println "异步请求已发送"))

(defn demonstrate-headers
  "自定义 HTTP 头"
  []
  (println "\n=== 自定义 HTTP 头 ===")
  
  (py/call-attr py-embedded "run_block_5")
  
  (println "自定义头请求完成"))

(defn -main
  [& args]
  (println "=== PySide6 HTTP 网络请求示例 (Clojure) ===")
  
  ;; 网络请求在命令行模式下可能有延迟，简化演示
  (println "\nHTTP 功能说明:")
  (println "- QNetworkAccessManager: HTTP 请求管理器")
  (println "- QNetworkRequest: 请求配置")
  (println "- QNetworkReply: 响应数据")
  (println "- 支持 GET, POST, PUT, DELETE 等方法")
  (println "- 支持自定义 Headers")
  (println "- 支持异步回调")
  
  (println "\n=== 完成 ==="))

(-main)
