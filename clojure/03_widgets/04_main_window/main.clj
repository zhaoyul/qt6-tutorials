#!/usr/bin/env clojure -M
;; PySide6 主窗口示例 (Clojure + libpython-clj)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn -main
  [& args]
  (println "=== PySide6 主窗口示例 (Clojure) ===")

  (py/run-simple-string "
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit,
    QDockWidget, QListWidget
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import sys

app = QApplication(sys.argv)

win = QMainWindow()
win.setWindowTitle('MainWindow Demo')
win.resize(800, 600)

central = QWidget()
layout = QVBoxLayout(central)
layout.addWidget(QLabel('Central Widget'))
editor = QTextEdit()
editor.setPlainText('Edit text here...')
layout.addWidget(editor)
win.setCentralWidget(central)

menu = win.menuBar()
file_menu = menu.addMenu('File')
menu.addMenu('Edit')

open_act = QAction('Open', win)
save_act = QAction('Save', win)
quit_act = QAction('Quit', win)
quit_act.triggered.connect(win.close)

file_menu.addAction(open_act)
file_menu.addAction(save_act)
file_menu.addSeparator()
file_menu.addAction(quit_act)

toolbar = win.addToolBar('Main')
toolbar.addAction(open_act)
toolbar.addAction(save_act)

dock = QDockWidget('Navigation', win)
dock_list = QListWidget()
dock_list.addItems(['Item 1', 'Item 2', 'Item 3'])
dock.setWidget(dock_list)
win.addDockWidget(Qt.LeftDockWidgetArea, dock)

win.statusBar().showMessage('Ready')

win.show()
app.exec()
")

  (println "\n=== 完成 ==="))

(-main)
