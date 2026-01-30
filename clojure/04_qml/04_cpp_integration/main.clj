#!/usr/bin/env clojure -M
;; PySide6 QML 与 Python 集成示例 (Clojure + libpython-clj)
;; 对应 C++ 的 04_cpp_integration 示例

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "04_qml/04_cpp_integration"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtGui :as QtGui :bind-ns])
(require-python '[PySide6.QtQml :as QtQml :bind-ns])

;; 获取类
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QQmlApplicationEngine (py/get-attr QtQml "QQmlApplicationEngine"))
(def QTimer (py/get-attr QtCore "QTimer"))
(def QQmlContext (py/get-attr QtQml "QQmlContext"))
(def qmlRegisterType (py/get-attr QtQml "qmlRegisterType"))

;; 定义 Counter 类 (通过 Python 代码注入，避免 py/fn 兼容问题)
(py/call-attr py-embedded "run_block_1")

(def Counter (py/get-attr py-embedded "Counter"))

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 QML 与 Python 集成示例 (Clojure) ===\n")
  
  (let [app (QGuiApplication (py/->py-list []))]
    
    ;; 注册 Counter 类型到 QML
    (qmlRegisterType Counter "QmlCppIntegration" 1 0 "Counter")
    
    (let [engine (QQmlApplicationEngine)]
      
      ;; 创建全局 Counter 实例并设置上下文属性
      (let [global-counter (Counter engine)
            ctx (py/call-attr engine "rootContext")]
        (py/set-attr! global-counter "value" 50)
        (py/call-attr ctx "setContextProperty"
                      "globalCounter" global-counter)

        ;; 设置简单上下文属性
        (py/call-attr ctx "setContextProperty"
                      "appVersion" "1.0.0")
        (py/call-attr ctx "setContextProperty"
                      "debugMode" true))
      
      ;; 加载 QML 文件
      (let [qml-path (str (System/getProperty "user.dir")
                         "/04_qml/04_cpp_integration/Main.qml")]
        (py/call-attr engine "load" qml-path))
      
      ;; 检查加载是否成功
      (if (empty? (py/call-attr engine "rootObjects"))
        (println "错误: QML 加载失败")
        (do
          (println "QML 加载成功")
          (when-let [auto-ms (System/getenv "QT6_TUTORIAL_AUTOQUIT")]
          (py/call-attr QTimer "singleShot"
                        (Integer/parseInt auto-ms)
                        (py/get-attr app "quit")))
        (py/call-attr app "exec")
        (when (System/getenv "QT6_TUTORIAL_AUTOQUIT")
          (System/exit 0)))))))

(-main)
