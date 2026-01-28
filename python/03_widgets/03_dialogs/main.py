#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 对话框示例

标准对话框：
- QMessageBox: 消息框
- QFileDialog: 文件对话框
- QColorDialog: 颜色对话框
- QFontDialog: 字体对话框
- QInputDialog: 输入对话框
- QProgressDialog: 进度对话框

自定义对话框：
- 继承 QDialog
- 模态 vs 非模态

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QMessageBox, QFileDialog, QColorDialog, QFontDialog,
    QInputDialog, QProgressDialog, QDialog, QDialogButtonBox,
    QLineEdit, QFormLayout
)
from PySide6.QtCore import Qt, QDir, QThread
from PySide6.QtGui import QColor, QFont


class CustomDialog(QDialog):
    """自定义对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("自定义对话框")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # 表单内容
        form = QFormLayout()
        self._name_edit = QLineEdit(self)
        self._email_edit = QLineEdit(self)
        form.addRow("姓名:", self._name_edit)
        form.addRow("邮箱:", self._email_edit)
        layout.addLayout(form)
        
        # 标准按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def name(self):
        return self._name_edit.text()
    
    def email(self):
        return self._email_edit.text()


class DialogsDemo(QWidget):
    """对话框演示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 Dialogs Demo")
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        self._result_label = QLabel("结果将显示在这里", self)
        self._result_label.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        self._result_label.setWordWrap(True)
        layout.addWidget(self._result_label)
        
        # 消息框按钮
        layout.addWidget(self._create_button("信息框", self._show_info_dialog))
        layout.addWidget(self._create_button("警告框", self._show_warning_dialog))
        layout.addWidget(self._create_button("错误框", self._show_error_dialog))
        layout.addWidget(self._create_button("确认框", self._show_question_dialog))
        
        # 选择对话框
        layout.addWidget(self._create_button("打开文件", self._show_file_open_dialog))
        layout.addWidget(self._create_button("保存文件", self._show_file_save_dialog))
        layout.addWidget(self._create_button("选择目录", self._show_directory_dialog))
        layout.addWidget(self._create_button("选择颜色", self._show_color_dialog))
        layout.addWidget(self._create_button("选择字体", self._show_font_dialog))
        
        # 输入对话框
        layout.addWidget(self._create_button("输入文本", self._show_text_input_dialog))
        layout.addWidget(self._create_button("输入数字", self._show_int_input_dialog))
        layout.addWidget(self._create_button("选择项目", self._show_item_input_dialog))
        
        # 进度对话框
        layout.addWidget(self._create_button("进度对话框", self._show_progress_dialog))
        
        # 自定义对话框
        layout.addWidget(self._create_button("自定义对话框", self._show_custom_dialog))
        
        layout.addStretch()
    
    def _create_button(self, text, callback):
        """创建按钮"""
        btn = QPushButton(text, self)
        btn.clicked.connect(callback)
        return btn
    
    def _show_info_dialog(self):
        QMessageBox.information(self, "信息", "这是一条信息消息。")
        self._result_label.setText("显示了信息框")
    
    def _show_warning_dialog(self):
        QMessageBox.warning(self, "警告", "这是一条警告消息！")
        self._result_label.setText("显示了警告框")
    
    def _show_error_dialog(self):
        QMessageBox.critical(self, "错误", "发生了一个错误！")
        self._result_label.setText("显示了错误框")
    
    def _show_question_dialog(self):
        result = QMessageBox.question(
            self, "确认",
            "你确定要继续吗？",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.No  # 默认按钮
        )
        
        text_map = {
            QMessageBox.Yes: "选择了: Yes",
            QMessageBox.No: "选择了: No",
            QMessageBox.Cancel: "选择了: Cancel"
        }
        self._result_label.setText(text_map.get(result, "未知"))
    
    def _show_file_open_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "打开文件",
            QDir.homePath(),
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if file_name:
            self._result_label.setText(f"选择的文件: {file_name}")
        else:
            self._result_label.setText("取消选择")
    
    def _show_file_save_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存文件",
            QDir.homePath() + "/untitled.txt",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if file_name:
            self._result_label.setText(f"保存到: {file_name}")
    
    def _show_directory_dialog(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择目录",
            QDir.homePath()
        )
        
        if dir_path:
            self._result_label.setText(f"选择的目录: {dir_path}")
    
    def _show_color_dialog(self):
        color = QColorDialog.getColor(
            Qt.white, self, "选择颜色"
        )
        
        if color.isValid():
            self._result_label.setText(f"选择的颜色: {color.name()}")
            self._result_label.setStyleSheet(
                f"background-color: {color.name()}; padding: 10px;"
            )
    
    def _show_font_dialog(self):
        ok, font = QFontDialog.getFont(self.font(), self, "选择字体")
        
        if ok:
            self._result_label.setFont(font)
            self._result_label.setText(f"选择的字体: {font.family()}, {font.pointSize()}pt")
    
    def _show_text_input_dialog(self):
        text, ok = QInputDialog.getText(
            self, "输入文本",
            "请输入你的名字:",
            QLineEdit.Normal,
            "默认值"
        )
        
        if ok and text:
            self._result_label.setText(f"输入的文本: {text}")
    
    def _show_int_input_dialog(self):
        value, ok = QInputDialog.getInt(
            self, "输入数字",
            "请输入年龄:",
            25,     # 默认值
            0,      # 最小值
            150,    # 最大值
            1       # 步长
        )
        
        if ok:
            self._result_label.setText(f"输入的数字: {value}")
    
    def _show_item_input_dialog(self):
        items = ["选项一", "选项二", "选项三", "选项四"]
        item, ok = QInputDialog.getItem(
            self, "选择项目",
            "请选择:",
            items,
            0,      # 默认选中
            False   # 不可编辑
        )
        
        if ok and item:
            self._result_label.setText(f"选择的项目: {item}")
    
    def _show_progress_dialog(self):
        progress = QProgressDialog("正在处理...", "取消", 0, 100, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)  # 立即显示
        
        for i in range(101):
            progress.setValue(i)
            QApplication.processEvents()
            
            if progress.wasCanceled():
                self._result_label.setText("进度被取消")
                return
            
            QThread.msleep(30)  # 模拟工作
        
        self._result_label.setText("进度完成!")
    
    def _show_custom_dialog(self):
        dialog = CustomDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            self._result_label.setText(f"姓名: {dialog.name()}\n邮箱: {dialog.email()}")
        else:
            self._result_label.setText("对话框被取消")


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 对话框示例 ===\n")
    
    demo = DialogsDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
