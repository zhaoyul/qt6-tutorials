#!/usr/bin/env clojure -M
;; PySide6 布局管理示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtWidgets (py/import-module "PySide6.QtWidgets"))
(def QtCore (py/import-module "PySide6.QtCore"))

;; 获取类
(def QWidget (py/get-attr QtWidgets "QWidget"))
(def QApplication (py/get-attr QtWidgets "QApplication"))
(def QVBoxLayout (py/get-attr QtWidgets "QVBoxLayout"))
(def QHBoxLayout (py/get-attr QtWidgets "QHBoxLayout"))
(def QGridLayout (py/get-attr QtWidgets "QGridLayout"))
(def QFormLayout (py/get-attr QtWidgets "QFormLayout"))
(def QLabel (py/get-attr QtWidgets "QLabel"))
(def QPushButton (py/get-attr QtWidgets "QPushButton"))
(def QLineEdit (py/get-attr QtWidgets "QLineEdit"))
(def QFrame (py/get-attr QtWidgets "QFrame"))

(defn create-vbox-demo
  "垂直布局示例"
  []
  (println "\n=== 垂直布局 (QVBoxLayout) ===")

  ;; 创建窗口和布局
  (let [window (QWidget)
        layout (QVBoxLayout window)]

    ;; 添加控件
    (py/call-attr layout "addWidget" (QLabel "标签 1"))
    (py/call-attr layout "addWidget" (QLabel "标签 2"))
    (py/call-attr layout "addWidget" (QPushButton "按钮"))

    ;; 设置边距
    (py/call-attr layout "setContentsMargins" 10 10 10 10)
    (py/call-attr layout "setSpacing" 10)

    (println "垂直布局创建完成")
    window))

(defn create-hbox-demo
  "水平布局示例"
  []
  (println "\n=== 水平布局 (QHBoxLayout) ===")

  (let [window (QWidget)
        layout (QHBoxLayout window)]

    (py/call-attr layout "addWidget" (QPushButton "左"))
    (py/call-attr layout "addWidget" (QPushButton "中"))
    (py/call-attr layout "addWidget" (QPushButton "右"))

    ;; 添加伸缩因子
    (py/call-attr layout "addStretch")

    (println "水平布局创建完成")
    window))

(defn create-grid-demo
  "网格布局示例"
  []
  (println "\n=== 网格布局 (QGridLayout) ===")

  (let [window (QWidget)
        layout (QGridLayout window)]

    ;; 添加控件到网格
    (py/call-attr layout "addWidget" (QLabel "姓名:") 0 0)
    (py/call-attr layout "addWidget" (QLineEdit) 0 1)

    (py/call-attr layout "addWidget" (QLabel "年龄:") 1 0)
    (py/call-attr layout "addWidget" (QLineEdit) 1 1)

    (py/call-attr layout "addWidget" (QPushButton "提交") 2 0 1 2)  ;; 跨越2列

    (println "网格布局创建完成")
    window))

(defn create-form-demo
  "表单布局示例"
  []
  (println "\n=== 表单布局 (QFormLayout) ===")

  (let [window (QWidget)
        layout (QFormLayout window)]

    ;; 添加表单项
    (py/call-attr layout "addRow" "用户名:" (QLineEdit))
    (py/call-attr layout "addRow" "密码:" (QLineEdit))
    (py/call-attr layout "addRow" "邮箱:" (QLineEdit))
    (py/call-attr layout "addRow" "" (QPushButton "登录"))

    (println "表单布局创建完成")
    window))

(defn demonstrate-nested-layouts
  "嵌套布局示例"
  []
  (println "\n=== 嵌套布局 ===")

  (let [main-window (QWidget)
        main-layout (QVBoxLayout main-window)

        ;; 顶部水平布局
        top-layout (QHBoxLayout)
        _ (do
            (py/call-attr top-layout "addWidget" (QPushButton "文件"))
            (py/call-attr top-layout "addWidget" (QPushButton "编辑"))
            (py/call-attr top-layout "addStretch"))

        ;; 中间网格布局
        middle-widget (QWidget)
        middle-layout (QGridLayout middle-widget)]

    (py/call-attr middle-layout "addWidget" (QFrame) 0 0)
    (py/call-attr middle-layout "addWidget" (QFrame) 0 1)
    (py/call-attr middle-layout "addWidget" (QFrame) 1 0)
    (py/call-attr middle-layout "addWidget" (QFrame) 1 1)

    ;; 底部水平布局
    (let [bottom-layout (QHBoxLayout)]
      (py/call-attr bottom-layout "addStretch")
      (py/call-attr bottom-layout "addWidget" (QPushButton "确定"))
      (py/call-attr bottom-layout "addWidget" (QPushButton "取消")))

    ;; 组合到主布局
    (py/call-attr main-layout "addLayout" top-layout)
    (py/call-attr main-layout "addWidget" middle-widget)
    ;; 底部布局添加省略...

    (println "嵌套布局创建完成")))

(defn -main
  [& args]
  (println "=== PySide6 布局管理示例 (Clojure) ===")

  ;; 初始化 QApplication
  (py/run-simple-string "
from PySide6.QtWidgets import QApplication
import sys
if not QApplication.instance():
    _app = QApplication(sys.argv)
")

  (create-vbox-demo)
  (create-hbox-demo)
  (create-grid-demo)
  (create-form-demo)
  (demonstrate-nested-layouts)

  (println "\n=== 完成 ==="))

(-main)
