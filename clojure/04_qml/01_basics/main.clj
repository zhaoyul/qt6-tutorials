#!/usr/bin/env clojure -M
;; PySide6 QML 基础示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtCore (py/import-module "PySide6.QtCore"))
(def QtWidgets (py/import-module "PySide6.QtWidgets"))
(def QtQml (py/import-module "PySide6.QtQml"))
(def QtQuick (py/import-module "PySide6.QtQuick"))

;; 获取类
(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QQmlApplicationEngine (py/get-attr QtQml "QQmlApplicationEngine"))
(def QQmlComponent (py/get-attr QtQml "QQmlComponent"))
(def QUrl (py/get-attr QtCore "QUrl"))

;; 内联 QML
(def hello-qml
  "import QtQuick
import QtQuick.Controls

Window {
    width: 400
    height: 300
    visible: true
    title: 'Hello from Clojure!'
    
    Column {
        anchors.centerIn: parent
        spacing: 20
        
        Label {
            id: helloLabel
            text: 'Hello QML!'
            font.pixelSize: 24
            anchors.horizontalCenter: parent.horizontalCenter
        }
        
        Button {
            text: '点击我'
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                helloLabel.text = '你好，Clojure!'
                console.log('按钮被点击')
            }
        }
        
        TextField {
            id: inputField
            placeholderText: '输入一些文字...'
            anchors.horizontalCenter: parent.horizontalCenter
        }
        
        Label {
            text: '你输入了: ' + inputField.text
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}")

(def property-binding-qml
  "import QtQuick
import QtQuick.Controls

Window {
    width: 400
    height: 300
    visible: true
    title: '属性绑定示例'
    
    property int clickCount: 0
    
    Column {
        anchors.centerIn: parent
        spacing: 20
        
        Label {
            text: '点击次数: ' + clickCount
            font.pixelSize: 20
        }
        
        Button {
            text: '增加'
            onClicked: clickCount++
        }
        
        Slider {
            id: slider
            width: 200
            from: 0
            to: 100
            value: 50
        }
        
        Label {
            text: '滑块值: ' + Math.round(slider.value)
        }
        
        ProgressBar {
            width: 200
            value: slider.value / 100
        }
    }
}")

(defn create-qml-file
  "创建临时 QML 文件"
  [content filename]
  (let [file (java.io.File. filename)]
    (spit file content)
    (.getAbsolutePath file)))

(defn run-basic-qml
  "运行基本 QML 示例"
  []
  (println "\n=== 基本 QML 示例 ===")
  
  (let [app (QApplication (make-array String 0))
        engine (QQmlApplicationEngine)]
    
    ;; 创建临时 QML 文件
    (let [qml-path (create-qml-file hello-qml "/tmp/hello_clojure.qml")]
      (py/call-attr engine "load" qml-path))
    
    ;; 检查是否有根对象
    (if (empty? (py/get-attr engine "rootObjects"))
      (println "错误: 无法加载 QML")
      (do
        (println "QML 加载成功")
        (py/call-attr app "exec")))))

(defn run-property-binding
  "运行属性绑定示例"
  []
  (println "\n=== 属性绑定示例 ===")
  
  (let [app (QApplication (make-array String 0))
        engine (QQmlApplicationEngine)]
    
    (let [qml-path (create-qml-file property-binding-qml "/tmp/property_binding.qml")]
      (py/call-attr engine "load" qml-path))
    
    (if (empty? (py/get-attr engine "rootObjects"))
      (println "错误: 无法加载 QML")
      (py/call-attr app "exec"))))

(defn run-from-url
  "演示从 URL/字符串加载"
  []
  (println "\n=== 从内存加载 QML ===")
  
  (let [app (QApplication (make-array String 0))
        engine (QQmlApplicationEngine)
        component (QQmlComponent engine)]
    
    ;; 从字符串设置数据
    (py/call-attr component "setData"
                  (.getBytes hello-qml)
                  (QUrl. ""))
    
    ;; 创建对象
    (let [obj (py/call-attr component "create")]
      (if obj
        (do
          (println "对象创建成功")
          (py/call-attr obj "show")
          (py/call-attr app "exec"))
        (println (str "错误: " (py/call-attr component "errorString")))))))

(defn -main
  [& args]
  (println "=== PySide6 QML 基础示例 (Clojure) ===")
  
  ;; 运行基本示例
  (run-basic-qml)
  
  ;; 清理临时文件
  (doseq [f ["/tmp/hello_clojure.qml" "/tmp/property_binding.qml"]]
    (let [file (java.io.File. f)]
      (when (.exists file)
        (.delete file))))
  
  (println "\n=== 完成 ==="))

(-main)
