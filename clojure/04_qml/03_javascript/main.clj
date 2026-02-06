#!/usr/bin/env clojure -M
;; PySide6 QML JavaScript Integration Demo (Clojure + libpython-clj)
;;
;; Shows how to use JavaScript functions in QML, including:
;; - Importing external JavaScript files
;; - Inline JavaScript functions
;; - Timer-based JavaScript execution

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtGui :as QtGui :bind-ns])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python '[PySide6.QtQml :as QtQml :bind-ns])

;; 获取类
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QQmlApplicationEngine (py/get-attr QtQml "QQmlApplicationEngine"))
(def QTimer (py/get-attr QtCore "QTimer"))

(defn -main
  [& args]
  (println "=== QML JavaScript Integration Demo (Clojure) ===")

  (let [app (QGuiApplication (py/->py-list []))
        engine (QQmlApplicationEngine)]

    ;; 加载 QML 文件
    (let [qml-path (str (System/getProperty "user.dir")
                        "/04_qml/03_javascript/Main.qml")]
      (py/call-attr engine "load" qml-path))

    ;; 检查是否有根对象
    (if (empty? (py/call-attr engine "rootObjects"))
      (println "错误: 无法加载 QML")
      (do
        (println "QML 加载成功")
        (when-let [auto-ms (System/getenv "QT6_TUTORIAL_AUTOQUIT")]
          (py/call-attr QTimer "singleShot"
                        (Integer/parseInt auto-ms)
                        (py/get-attr app "quit")))
        (py/call-attr app "exec")
        (when (System/getenv "QT6_TUTORIAL_AUTOQUIT")
          (System/exit 0))))))

(-main)
