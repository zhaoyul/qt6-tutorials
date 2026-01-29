#!/usr/bin/env clojure -M
;; PySide6 QML Types Demo (Clojure + libpython-clj)
;;
;; Shows basic QML property types and bindings.

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtGui (py/import-module "PySide6.QtGui"))
(def QtQml (py/import-module "PySide6.QtQml"))

;; 获取类
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QQmlApplicationEngine (py/get-attr QtQml "QQmlApplicationEngine"))

(defn -main
  [& args]
  (println "=== QML Types Demo (Clojure) ===")
  
  (let [app (QGuiApplication (make-array String 0))
        engine (QQmlApplicationEngine)]
    
    ;; 加载 QML 文件
    (let [qml-path (str (System/getProperty "user.dir") 
                        "/clojure/04_qml/02_types/Main.qml")]
      (py/call-attr engine "load" qml-path))
    
    ;; 检查是否有根对象
    (if (empty? (py/get-attr engine "rootObjects"))
      (println "错误: 无法加载 QML")
      (do
        (println "QML 加载成功")
        (py/call-attr app "exec")))))

(-main)
