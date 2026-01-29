#!/usr/bin/env clojure -M
;; PySide6 QML 与 Python 集成示例 (Clojure + libpython-clj)
;; 对应 C++ 的 04_cpp_integration 示例

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))
(def QtGui (py/import-module "PySide6.QtGui"))
(def QtQml (py/import-module "PySide6.QtQml"))

;; 获取类
(def QGuiApplication (py/get-attr QtGui "QGuiApplication"))
(def QQmlApplicationEngine (py/get-attr QtQml "QQmlApplicationEngine"))
(def QQmlContext (py/get-attr QtQml "QQmlContext"))
(def qmlRegisterType (py/get-attr QtQml "qmlRegisterType"))
(def QObject (py/get-attr QtCore "QObject"))
(def Property (py/get-attr QtCore "Property"))
(def Signal (py/get-attr QtCore "Signal"))
(def Slot (py/get-attr QtCore "Slot"))

;; 定义 Counter 类
(def Counter
  (py/create-class
    "Counter"
    [QObject]
    {"__init__"
     (py/fn [self & [parent]]
       (py/call-attr-super-keywords self "__init__" [] {:parent parent})
       (py/set-attr! self "_value" 0)
       (py/set-attr! self "_step" 1)
       (py/set-attr! self "_min_value" 0)
       (py/set-attr! self "_max_value" 100)
       nil)
     
     ;; 信号
     "valueChanged" (Signal)
     "stepChanged" (Signal)
     "limitReached" (Signal str)
     
     ;; value 属性 getter
     "get_value"
     (py/fn [self]
       (py/get-attr self "_value"))
     
     ;; value 属性 setter
     "set_value"
     (py/fn [self val]
       (let [current (py/get-attr self "_value")
             min-val (py/get-attr self "_min_value")
             max-val (py/get-attr self "_max_value")]
         (when (not= current val)
           (let [bounded-val (max min-val (min val max-val))]
             (py/set-attr! self "_value" bounded-val)
             (py/call-attr self "valueChanged.emit")
             ;; 检查边界
             (cond
               (= bounded-val max-val)
               (py/call-attr self "limitReached.emit" "已达到最大值!")
               (= bounded-val min-val)
               (py/call-attr self "limitReached.emit" "已达到最小值!"))))))
     
     ;; step 属性 getter
     "get_step"
     (py/fn [self]
       (py/get-attr self "_step"))
     
     ;; step 属性 setter
     "set_step"
     (py/fn [self s]
       (when (not= (py/get-attr self "_step") s)
         (py/set-attr! self "_step" s)
         (py/call-attr self "stepChanged.emit")))
     
     ;; displayText 只读属性
     "get_displayText"
     (py/fn [self]
       (str "当前值: " (py/get-attr self "_value")))
     
     ;; increment 方法
     "increment"
     (py/fn [self]
       (println "[Clojure/Python] increment() 被调用")
       (let [current (py/get-attr self "_value")
             step (py/get-attr self "_step")]
         (py/call-attr self "set_value" (+ current step))))
     
     ;; decrement 方法
     "decrement"
     (py/fn [self]
       (println "[Clojure/Python] decrement() 被调用")
       (let [current (py/get-attr self "_value")
             step (py/get-attr self "_step")]
         (py/call-attr self "set_value" (- current step))))
     
     ;; reset 方法
     "reset"
     (py/fn [self]
       (println "[Clojure/Python] reset() 被调用")
       (py/call-attr self "set_value" 0))
     
     ;; formatValue 方法
     "formatValue"
     (py/fn [self prefix]
       (str prefix ": " (py/get-attr self "_value")))}))

;; 添加 Property 装饰器
(py/call-attr Counter "value" 
              (Property int :fget (py/get-attr Counter "get_value")
                              :fset (py/get-attr Counter "set_value")
                              :notify (py/get-attr Counter "valueChanged")))

(py/call-attr Counter "step"
              (Property int :fget (py/get-attr Counter "get_step")
                              :fset (py/get-attr Counter "set_step")
                              :notify (py/get-attr Counter "stepChanged")))

(py/call-attr Counter "displayText"
              (Property str :fget (py/get-attr Counter "get_displayText")
                             :notify (py/get-attr Counter "valueChanged")))

(defn -main
  "主函数"
  [& args]
  (println "=== PySide6 QML 与 Python 集成示例 (Clojure) ===\n")
  
  (let [app (QGuiApplication (make-array String 0))]
    
    ;; 注册 Counter 类型到 QML
    (qmlRegisterType Counter "QmlClojureIntegration" 1 0 "Counter")
    
    (let [engine (QQmlApplicationEngine)]
      
      ;; 创建全局 Counter 实例并设置上下文属性
      (let [global-counter (Counter engine)]
        (py/call-attr global-counter "set_value" 50)
        (py/call-attr engine "rootContext.setContextProperty" 
                     "globalCounter" global-counter))
      
      ;; 设置简单上下文属性
      (py/call-attr engine "rootContext.setContextProperty"
                   "appVersion" "1.0.0")
      (py/call-attr engine "rootContext.setContextProperty"
                   "debugMode" true)
      
      ;; 加载 QML 文件
      (let [qml-path (str (System/getProperty "user.dir") 
                         "/clojure/04_qml/02_cpp_integration/Main.qml")]
        (py/call-attr engine "load" qml-path))
      
      ;; 检查加载是否成功
      (if (empty? (py/get-attr engine "rootObjects"))
        (println "错误: QML 加载失败")
        (do
          (println "QML 加载成功")
          (py/call-attr app "exec"))))))

(-main)
