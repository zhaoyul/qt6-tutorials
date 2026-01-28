#!/usr/bin/env clojure -M
;; PySide6 IO 系统示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn demonstrate-io
  "IO 操作演示"
  []
  (println "\n=== PySide6 IO 系统 ===")
  
  ;; 使用 Python 代码演示
  (py/run-simple-string "
from PySide6.QtCore import QCoreApplication, QFileInfo, QDir
import sys

# 初始化应用
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)

# 文件信息
print('=== 文件信息 ===')
fi = QFileInfo('/etc/hosts')
print(f'文件名: {fi.fileName()}')
print(f'路径: {fi.path()}')
print(f'大小: {fi.size()} bytes')
print(f'存在: {fi.exists()}')
print(f'可读: {fi.isReadable()}')
print(f'可写: {fi.isWritable()}')

# 目录操作
print('\\n=== 目录操作 ===')
d = QDir('/tmp')
print(f'当前路径: {d.path()}')
print(f'绝对路径: {d.absolutePath()}')

# 路径操作
print('\\n=== 路径操作 ===')
print(f'主目录: {QDir.homePath()}')
print(f'临时目录: {QDir.tempPath()}')
print(f'根目录: {QDir.rootPath()}')
")
  
  (println "\nIO 演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 IO 系统示例 (Clojure) ===")
  
  (demonstrate-io)
  
  (println "\n=== 完成 ==="))

(-main)
