def run_block_1():
    exec(r"""
from PySide6.QtWidgets import QApplication
import sys
if not QApplication.instance():
    _app = QApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
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
""", globals())

def run_block_3():
    exec(r"""
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
""", globals())
