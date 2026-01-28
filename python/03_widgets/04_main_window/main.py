#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 主窗口示例

QMainWindow 提供完整的应用程序框架：
- 菜单栏 (QMenuBar)
- 工具栏 (QToolBar)
- 状态栏 (QStatusBar)
- 停靠窗口 (QDockWidget)
- 中央部件 (Central Widget)

QAction 用于定义可重用的用户操作。

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/QMainWindow.html
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QToolBar,
    QStatusBar, QDockWidget, QTextEdit, QLabel, QFileDialog,
    QMessageBox, QStyle
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction, QKeySequence


class MainWindowDemo(QMainWindow):
    """主窗口演示"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PySide6 MainWindow Demo")
        self.resize(800, 600)
        
        self._text_edit = None
        self._current_file = ""
        self._view_menu = None
        
        self._new_action = None
        self._open_action = None
        self._save_action = None
        self._save_as_action = None
        self._exit_action = None
        self._cut_action = None
        self._copy_action = None
        self._paste_action = None
        self._about_action = None
        self._about_qt_action = None
        
        self._create_actions()
        self._create_menus()
        self._create_tool_bars()
        self._create_status_bar()
        self._create_dock_windows()
        self._create_central_widget()
        
        # 恢复窗口状态
        self._read_settings()
    
    def closeEvent(self, event):
        """关闭事件处理"""
        if self._maybe_save():
            self._write_settings()
            event.accept()
        else:
            event.ignore()
    
    def _new_file(self):
        """新建文件"""
        if self._maybe_save():
            self._text_edit.clear()
            self._set_current_file("")
            self.statusBar().showMessage("新建文件", 2000)
    
    def _open(self):
        """打开文件"""
        if self._maybe_save():
            file_name, _ = QFileDialog.getOpenFileName(self)
            if file_name:
                self._load_file(file_name)
    
    def _save(self):
        """保存文件"""
        if not self._current_file:
            return self._save_as()
        return self._save_file(self._current_file)
    
    def _save_as(self):
        """另存为"""
        file_name, _ = QFileDialog.getSaveFileName(self)
        if file_name:
            return self._save_file(file_name)
        return False
    
    def _about(self):
        """关于对话框"""
        QMessageBox.about(self, "关于",
            "PySide6 MainWindow 示例\n\n"
            "演示 QMainWindow 的主要功能：\n"
            "• 菜单栏和工具栏\n"
            "• 状态栏\n"
            "• 停靠窗口\n"
            "• 文件操作")
    
    def _document_was_modified(self):
        """文档被修改"""
        self.setWindowModified(self._text_edit.document().isModified())
    
    def _create_actions(self):
        """创建动作"""
        # 文件操作
        self._new_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon),
            "新建(&N)", self)
        self._new_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.New))
        self._new_action.setStatusTip("创建新文件")
        self._new_action.triggered.connect(self._new_file)
        
        self._open_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
            "打开(&O)", self)
        self._open_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Open))
        self._open_action.setStatusTip("打开文件")
        self._open_action.triggered.connect(self._open)
        
        self._save_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            "保存(&S)", self)
        self._save_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Save))
        self._save_action.setStatusTip("保存文件")
        self._save_action.triggered.connect(self._save)
        
        self._save_as_action = QAction("另存为(&A)...", self)
        self._save_as_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.SaveAs))
        self._save_as_action.triggered.connect(self._save_as)
        
        self._exit_action = QAction("退出(&X)", self)
        self._exit_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Quit))
        self._exit_action.triggered.connect(self.close)
        
        # 编辑操作
        self._cut_action = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton),
            "剪切(&T)", self)
        self._cut_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Cut))
        
        self._copy_action = QAction("复制(&C)", self)
        self._copy_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Copy))
        
        self._paste_action = QAction("粘贴(&P)", self)
        self._paste_action.setShortcuts(QKeySequence(QKeySequence.StandardKey.Paste))
        
        # 关于
        self._about_action = QAction("关于(&A)", self)
        self._about_action.triggered.connect(self._about)
        
        self._about_qt_action = QAction("关于 Qt", self)
        self._about_qt_action.triggered.connect(QApplication.aboutQt)
    
    def _create_menus(self):
        """创建菜单"""
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件(&F)")
        file_menu.addAction(self._new_action)
        file_menu.addAction(self._open_action)
        file_menu.addAction(self._save_action)
        file_menu.addAction(self._save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self._exit_action)
        
        # 编辑菜单
        edit_menu = self.menuBar().addMenu("编辑(&E)")
        edit_menu.addAction(self._cut_action)
        edit_menu.addAction(self._copy_action)
        edit_menu.addAction(self._paste_action)
        
        # 视图菜单 (用于控制停靠窗口)
        self._view_menu = self.menuBar().addMenu("视图(&V)")
        
        # 帮助菜单
        self.menuBar().addSeparator()
        help_menu = self.menuBar().addMenu("帮助(&H)")
        help_menu.addAction(self._about_action)
        help_menu.addAction(self._about_qt_action)
    
    def _create_tool_bars(self):
        """创建工具栏"""
        # 文件工具栏
        file_tool_bar = self.addToolBar("文件")
        file_tool_bar.setObjectName("fileToolBar")
        file_tool_bar.addAction(self._new_action)
        file_tool_bar.addAction(self._open_action)
        file_tool_bar.addAction(self._save_action)
        
        # 编辑工具栏
        edit_tool_bar = self.addToolBar("编辑")
        edit_tool_bar.setObjectName("editToolBar")
        edit_tool_bar.addAction(self._cut_action)
        edit_tool_bar.addAction(self._copy_action)
        edit_tool_bar.addAction(self._paste_action)
        
        # 添加到视图菜单
        self._view_menu.addAction(file_tool_bar.toggleViewAction())
        self._view_menu.addAction(edit_tool_bar.toggleViewAction())
    
    def _create_status_bar(self):
        """创建状态栏"""
        # 主状态消息
        self.statusBar().showMessage("就绪")
        
        # 永久部件
        permanent_label = QLabel("PySide6 Demo")
        self.statusBar().addPermanentWidget(permanent_label)
    
    def _create_dock_windows(self):
        """创建停靠窗口"""
        # 左侧停靠窗口
        left_dock = QDockWidget("导航", self)
        left_dock.setObjectName("leftDock")
        left_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        nav_edit = QTextEdit("导航面板\n\n这是一个停靠窗口")
        nav_edit.setReadOnly(True)
        left_dock.setWidget(nav_edit)
        self.addDockWidget(Qt.LeftDockWidgetArea, left_dock)
        
        # 右侧停靠窗口
        right_dock = QDockWidget("属性", self)
        right_dock.setObjectName("rightDock")
        right_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        prop_edit = QTextEdit("属性面板\n\n可以拖动到不同位置")
        prop_edit.setReadOnly(True)
        right_dock.setWidget(prop_edit)
        self.addDockWidget(Qt.RightDockWidgetArea, right_dock)
        
        # 底部停靠窗口
        bottom_dock = QDockWidget("输出", self)
        bottom_dock.setObjectName("bottomDock")
        bottom_dock.setAllowedAreas(Qt.BottomDockWidgetArea | Qt.TopDockWidgetArea)
        output_edit = QTextEdit("输出面板\n\n停靠窗口可以浮动或关闭")
        output_edit.setReadOnly(True)
        bottom_dock.setWidget(output_edit)
        self.addDockWidget(Qt.BottomDockWidgetArea, bottom_dock)
        
        # 添加到视图菜单
        self._view_menu.addSeparator()
        self._view_menu.addAction(left_dock.toggleViewAction())
        self._view_menu.addAction(right_dock.toggleViewAction())
        self._view_menu.addAction(bottom_dock.toggleViewAction())
    
    def _create_central_widget(self):
        """创建中央部件"""
        self._text_edit = QTextEdit(self)
        self._text_edit.setPlaceholderText("在此输入内容...\n\n这是中央部件 (Central Widget)")
        self.setCentralWidget(self._text_edit)
        
        self._text_edit.document().contentsChanged.connect(self._document_was_modified)
        
        # 连接编辑操作
        self._cut_action.triggered.connect(self._text_edit.cut)
        self._copy_action.triggered.connect(self._text_edit.copy)
        self._paste_action.triggered.connect(self._text_edit.paste)
    
    def _read_settings(self):
        """读取设置"""
        settings = QSettings("QtDemo", "MainWindow")
        self.restoreGeometry(settings.value("geometry", b""))
        self.restoreState(settings.value("windowState", b""))
    
    def _write_settings(self):
        """写入设置"""
        settings = QSettings("QtDemo", "MainWindow")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
    
    def _maybe_save(self):
        """询问是否保存"""
        if not self._text_edit.document().isModified():
            return True
        
        ret = QMessageBox.warning(self, "保存更改?",
            "文档已修改。\n是否保存更改?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        
        if ret == QMessageBox.Save:
            return self._save()
        if ret == QMessageBox.Cancel:
            return False
        return True
    
    def _load_file(self, file_name):
        """加载文件"""
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                self._text_edit.setPlainText(f.read())
            self._set_current_file(file_name)
            self.statusBar().showMessage("文件已加载", 2000)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法读取文件:\n{e}")
    
    def _save_file(self, file_name):
        """保存文件"""
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self._text_edit.toPlainText())
            self._set_current_file(file_name)
            self.statusBar().showMessage("文件已保存", 2000)
            return True
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法保存文件:\n{e}")
            return False
    
    def _set_current_file(self, file_name):
        """设置当前文件"""
        self._current_file = file_name
        self._text_edit.document().setModified(False)
        self.setWindowModified(False)
        
        title = "未命名" if not file_name else file_name.split('/')[-1]
        self.setWindowTitle(f"{title}[*] - MainWindow Demo")


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 主窗口示例 ===\n")
    print("功能:")
    print("- 菜单栏: 文件、编辑、视图、帮助")
    print("- 工具栏: 可拖动、隐藏")
    print("- 停靠窗口: 可拖动、浮动、关闭")
    print("- 状态栏: 显示消息")
    print("- 窗口状态: 自动保存和恢复\n")
    
    main_window = MainWindowDemo()
    main_window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
