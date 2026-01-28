#!/usr/bin/env clojure -M
;; PySide6 对话框示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py])

(py/initialize!)

;; 导入模块
(def QtWidgets (py/import-module "PySide6.QtWidgets"))
(def QtCore (py/get-attr QtWidgets "Qt"))

;; 初始化 QApplication
(py/run-simple-string "
from PySide6.QtWidgets import QApplication
import sys
if not QApplication.instance():
    _app = QApplication(sys.argv)
")

(defn demonstrate-message-box
  "消息对话框"
  []
  (println "\n=== 消息对话框 ===")
  
  (let [QMessageBox (py/get-attr QtWidgets "QMessageBox")]
    ;; 信息框
    (println "信息框: 显示信息消息")
    ;; (py/call-attr QMessageBox "information" nil "标题" "这是一条信息")
    
    ;; 询问框
    (println "询问框: 需要用户确认")
    ;; (py/call-attr QMessageBox "question" nil "确认" "确定要删除吗?")
    
    ;; 警告框
    (println "警告框: 显示警告")
    ;; (py/call-attr QMessageBox "warning" nil "警告" "操作有风险")
    
    ;; 错误框
    (println "错误框: 显示错误")
    ;; (py/call-attr QMessageBox "critical" nil "错误" "操作失败")
    
    (println "消息对话框类型: Information, Question, Warning, Critical")))

(defn demonstrate-input-dialog
  "输入对话框"
  []
  (println "\n=== 输入对话框 ===")
  
  (let [QInputDialog (py/get-attr QtWidgets "QInputDialog")]
    (println "文本输入: 获取字符串")
    (println "整数输入: 获取整数")
    (println "双精度输入: 获取浮点数")
    (println "选项输入: 从列表选择")
    
    ;; 示例代码（注释）
    ;; (py/call-attr QInputDialog "getText" nil "输入" "请输入名字:")
    ;; (py/call-attr QInputDialog "getInt" nil "输入" "请输入年龄:")
    ;; (py/call-attr QInputDialog "getDouble" nil "输入" "请输入价格:")
    ;; (py/call-attr QInputDialog "getItem" nil "选择" "请选择:" ["A" "B" "C"])
    ))

(defn demonstrate-file-dialog
  "文件对话框"
  []
  (println "\n=== 文件对话框 ===")
  
  (let [QFileDialog (py/get-attr QtWidgets "QFileDialog")]
    (println "打开文件: getOpenFileName")
    (println "保存文件: getSaveFileName")
    (println "选择目录: getExistingDirectory")
    (println "打开多个文件: getOpenFileNames")
    
    ;; 示例
    (let [file-name (py/call-attr QFileDialog "getOpenFileName" 
                                   nil "选择文件" "/home"
                                   "所有文件 (*);;文本文件 (*.txt)")]
      (println (str "选择的文件: " file-name)))))

(defn demonstrate-progress-dialog
  "进度对话框"
  []
  (println "\n=== 进度对话框 ===")
  
  (py/run-simple-string "
from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt

# 创建进度对话框
progress = QProgressDialog('正在处理...', '取消', 0, 100)
progress.setWindowTitle('请稍候')
progress.setWindowModality(Qt.WindowModal)

# 模拟进度
for i in range(101):
    progress.setValue(i)
    if progress.wasCanceled():
        print('用户取消')
        break

progress.setValue(100)
print('进度完成')
")
  
  (println "进度对话框演示完成"))

(defn demonstrate-custom-dialog
  "自定义对话框"
  []
  (println "\n=== 自定义对话框 ===")
  
  (py/run-simple-string "
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                               QLabel, QLineEdit, QPushButton)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('登录')
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout(self)
        
        # 用户名
        layout.addWidget(QLabel('用户名:'))
        self.username = QLineEdit()
        layout.addWidget(self.username)
        
        # 密码
        layout.addWidget(QLabel('密码:'))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        # 按钮
        btn_layout = QHBoxLayout()
        login_btn = QPushButton('登录')
        cancel_btn = QPushButton('取消')
        
        login_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

# 显示对话框
dialog = LoginDialog()
result = dialog.exec()

if result == QDialog.Accepted:
    print(f'登录: {dialog.username.text()}')
else:
    print('取消登录')
")
  
  (println "自定义对话框演示完成"))

(defn -main
  [& args]
  (println "=== PySide6 对话框示例 (Clojure) ===")
  
  (demonstrate-message-box)
  (demonstrate-input-dialog)
  (demonstrate-file-dialog)
  ;; (demonstrate-progress-dialog)  ;; GUI 模式
  ;; (demonstrate-custom-dialog)    ;; GUI 模式
  
  (println "\n=== 完成 ==="))

(-main)
