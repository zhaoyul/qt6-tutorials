#!/usr/bin/env clojure -M
;; PySide6 窗口系统示例 (Clojure + libpython-clj)
;; 注意：macOS GUI 必须在主线程运行，这里使用控制台演示窗口属性

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
(require-python :from "02_gui/05_window"
                '[embedded :as py-embedded :bind-ns :reload])

;; 获取类
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
(def QSize (py/get-attr QtCore "QSize"))
(def QRect (py/get-attr QtCore "QRect"))

;; 初始化 QCoreApplication
(py/call-attr py-embedded "run_block_1")

(defn demonstrate-qt-constants
  "Qt 常量演示"
  []
  (println "\n=== Qt 窗口常量 ===")
  
  (let [Qt (py/get-attr QtCore "Qt")]
    (println "\n窗口类型:")
    (println "  Qt.Window - 独立窗口")
    (println "  Qt.Dialog - 对话框")
    (println "  Qt.Popup - 弹出菜单")
    (println "  Qt.Tool - 工具窗口")
    
    (println "\n窗口标志:")
    (println "  Qt.FramelessWindowHint - 无边框")
    (println "  Qt.WindowStaysOnTopHint - 置顶")
    (println "  Qt.WindowStaysOnBottomHint - 置底")
    (println "  Qt.WindowCloseButtonHint - 关闭按钮")
    
    (println "\n窗口状态:")
    (println "  Qt.WindowNoState - 正常")
    (println "  Qt.WindowMinimized - 最小化")
    (println "  Qt.WindowMaximized - 最大化")
    (println "  Qt.WindowFullScreen - 全屏")))

(defn demonstrate-geometry
  "几何类演示"
  []
  (println "\n=== 几何类 ===")
  
  ;; QSize
  (let [size (QSize 800 600)]
    (println (str "QSize: " (py/call-attr size "width") "x" (py/call-attr size "height")))
    (py/call-attr size "setWidth" 1024)
    (println (str "修改后宽度: " (py/call-attr size "width"))))
  
  ;; QRect
  (let [rect (QRect 10 20 300 200)]
    (println (str "\nQRect: x=" (py/call-attr rect "x") 
                  " y=" (py/call-attr rect "y")
                  " width=" (py/call-attr rect "width")
                  " height=" (py/call-attr rect "height")))
    (println (str "左上角: " (py/call-attr rect "topLeft")))
    (println (str "右下角: " (py/call-attr rect "bottomRight")))))

(defn demonstrate-screen-info
  "屏幕信息"
  []
  (println "\n=== 屏幕信息 ===")
  
  ;; 使用 Python 代码获取屏幕信息
  (py/call-attr py-embedded "run_block_2")
  
  (println "屏幕信息代码示例已输出"))

(defn -main
  [& args]
  (println "=== PySide6 窗口系统示例 (Clojure) ===")
  (println "注意: macOS GUI 必须在主线程运行，这里演示窗口属性")
  
  (demonstrate-qt-constants)
  (demonstrate-geometry)
  (demonstrate-screen-info)
  
  (println "\n=== 窗口要点 ===")
  (println "1. QWindow: 底层窗口类")
  (println "2. WindowFlags: 窗口标志控制外观")
  (println "3. WindowState: 窗口状态管理")
  (println "4. 几何: QRect, QSize, QPoint")
  (println "5. 屏幕: QScreen 提供显示信息")
  
  (println "\n=== 完成 ==="))

(-main)
