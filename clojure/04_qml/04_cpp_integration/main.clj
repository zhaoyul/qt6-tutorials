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
(def QTimer (py/get-attr QtCore "QTimer"))
(def QQmlContext (py/get-attr QtQml "QQmlContext"))
(def qmlRegisterType (py/get-attr QtQml "qmlRegisterType"))

;; 定义 Counter 类 (通过 Python 代码注入，避免 py/fn 兼容问题)
(py/run-simple-string "
from PySide6.QtCore import QObject, Property, Signal, Slot

class Counter(QObject):
    valueChanged = Signal()
    stepChanged = Signal()
    limitReached = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._step = 1
        self._min_value = 0
        self._max_value = 100

    @Property(int, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self._value != val:
            self._value = max(self._min_value, min(val, self._max_value))
            self.valueChanged.emit()
            if self._value == self._max_value:
                self.limitReached.emit('已达到最大值!')
            elif self._value == self._min_value:
                self.limitReached.emit('已达到最小值!')

    @Property(int, notify=stepChanged)
    def step(self):
        return self._step

    @step.setter
    def step(self, s):
        if self._step != s:
            self._step = s
            self.stepChanged.emit()

    @Property(str, notify=valueChanged)
    def displayText(self):
        return f'当前值: {self._value}'

    @Slot()
    def increment(self):
        print('[Clojure/Python] increment() 被调用')
        self.value = self._value + self._step

    @Slot()
    def decrement(self):
        print('[Clojure/Python] decrement() 被调用')
        self.value = self._value - self._step

    @Slot()
    def reset(self):
        print('[Clojure/Python] reset() 被调用')
        self.value = 0

    @Slot(str, result=str)
    def formatValue(self, prefix):
        return f'{prefix}: {self._value}'
")

(def MainModule (py/import-module "__main__"))
(def Counter (py/get-attr MainModule "Counter"))

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
