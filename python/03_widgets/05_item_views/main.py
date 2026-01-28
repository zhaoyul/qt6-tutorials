#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 模型/视图示例

Qt 的模型/视图架构分离数据和表示：
- Model: 数据 (QAbstractItemModel 及其子类)
- View: 显示 (QListView, QTableView, QTreeView)
- Delegate: 渲染和编辑 (QStyledItemDelegate)

便捷类 (包含内置模型):
- QListWidget
- QTableWidget
- QTreeWidget

官方文档: https://doc.qt.io/qtforpython/PySide6/QtWidgets/index.html
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QListView, QTableView, QTreeView,
    QHeaderView, QLineEdit, QLabel, QWidget, QStyle
)
from PySide6.QtCore import Qt, QSize, QStringListModel, QSortFilterProxyModel
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem


def create_list_widget_demo():
    """QListWidget 示例 (便捷类)"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    list_widget = QListWidget()
    
    # 添加项目
    list_widget.addItem("普通项目 1")
    list_widget.addItem("普通项目 2")
    
    # 带图标的项目
    icon_item = QListWidgetItem(
        QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon),
        "带图标的项目"
    )
    list_widget.addItem(icon_item)
    
    # 可选中项目
    check_item = QListWidgetItem("可选中项目")
    check_item.setFlags(check_item.flags() | Qt.ItemIsUserCheckable)
    check_item.setCheckState(Qt.Unchecked)
    list_widget.addItem(check_item)
    
    # 不同颜色
    color_item = QListWidgetItem("彩色项目")
    color_item.setForeground(Qt.blue)
    color_item.setBackground(QColor(255, 255, 200))
    list_widget.addItem(color_item)
    
    # 设置选择模式
    list_widget.setSelectionMode(QListWidget.ExtendedSelection)
    
    # 信号连接
    list_widget.itemClicked.connect(lambda item: print(f"点击: {item.text()}"))
    
    layout.addWidget(QLabel("QListWidget - 便捷列表控件"))
    layout.addWidget(list_widget)
    
    # 操作按钮
    btn_layout = QHBoxLayout()
    add_btn = QPushButton("添加")
    remove_btn = QPushButton("删除选中")
    
    add_btn.clicked.connect(lambda: list_widget.addItem(f"新项目 {list_widget.count() + 1}"))
    remove_btn.clicked.connect(lambda: [list_widget.takeItem(list_widget.row(item)) 
                                        for item in list_widget.selectedItems()])
    
    btn_layout.addWidget(add_btn)
    btn_layout.addWidget(remove_btn)
    layout.addLayout(btn_layout)
    
    return widget


def create_table_widget_demo():
    """QTableWidget 示例 (便捷类)"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    table_widget = QTableWidget(5, 4)
    
    # 设置表头
    table_widget.setHorizontalHeaderLabels(["姓名", "年龄", "城市", "职业"])
    
    # 填充数据
    names = ["张三", "李四", "王五", "赵六", "钱七"]
    ages = ["25", "30", "28", "35", "22"]
    cities = ["北京", "上海", "广州", "深圳", "杭州"]
    jobs = ["工程师", "设计师", "产品经理", "数据分析", "运营"]
    
    for row in range(5):
        table_widget.setItem(row, 0, QTableWidgetItem(names[row]))
        table_widget.setItem(row, 1, QTableWidgetItem(ages[row]))
        table_widget.setItem(row, 2, QTableWidgetItem(cities[row]))
        table_widget.setItem(row, 3, QTableWidgetItem(jobs[row]))
    
    # 设置列宽
    table_widget.horizontalHeader().setStretchLastSection(True)
    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
    
    # 启用排序
    table_widget.setSortingEnabled(True)
    
    # 交替行颜色
    table_widget.setAlternatingRowColors(True)
    
    # 选择整行
    table_widget.setSelectionBehavior(QTableWidget.SelectRows)
    
    layout.addWidget(QLabel("QTableWidget - 便捷表格控件"))
    layout.addWidget(table_widget)
    
    return widget


def create_tree_widget_demo():
    """QTreeWidget 示例 (便捷类)"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    tree_widget = QTreeWidget()
    tree_widget.setHeaderLabels(["名称", "类型", "大小"])
    tree_widget.setColumnCount(3)
    
    # 根节点
    root1 = QTreeWidgetItem(tree_widget, ["项目A", "文件夹", ""])
    root2 = QTreeWidgetItem(tree_widget, ["项目B", "文件夹", ""])
    
    # 子节点
    QTreeWidgetItem(root1, ["main.cpp", "C++ 源文件", "10 KB"])
    QTreeWidgetItem(root1, ["main.h", "C++ 头文件", "2 KB"])
    
    sub_folder = QTreeWidgetItem(root1, ["src", "文件夹", ""])
    QTreeWidgetItem(sub_folder, ["utils.cpp", "C++ 源文件", "5 KB"])
    QTreeWidgetItem(sub_folder, ["utils.h", "C++ 头文件", "1 KB"])
    
    QTreeWidgetItem(root2, ["readme.md", "Markdown", "3 KB"])
    QTreeWidgetItem(root2, ["config.json", "JSON", "1 KB"])
    
    # 展开所有
    tree_widget.expandAll()
    
    # 调整列宽
    tree_widget.header().setSectionResizeMode(0, QHeaderView.Stretch)
    
    layout.addWidget(QLabel("QTreeWidget - 便捷树形控件"))
    layout.addWidget(tree_widget)
    
    return widget


def create_model_view_demo():
    """模型/视图分离示例"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    layout.addWidget(QLabel("Model/View 分离 - 一个模型，多个视图"))
    
    # 创建共享模型
    model = QStandardItemModel(widget)
    
    # 填充数据
    items = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
    for item_text in items:
        std_item = QStandardItem(item_text)
        std_item.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        model.appendRow(std_item)
    
    # 创建视图
    view_layout = QHBoxLayout()
    
    list_view = QListView()
    list_view.setModel(model)
    
    icon_view = QListView()
    icon_view.setModel(model)
    icon_view.setViewMode(QListView.IconMode)
    icon_view.setGridSize(QSize(80, 80))
    
    view_layout.addWidget(list_view)
    view_layout.addWidget(icon_view)
    
    layout.addLayout(view_layout)
    
    # 说明
    layout.addWidget(QLabel("两个视图共享同一个模型，修改会同步"))
    
    return widget


def create_proxy_model_demo():
    """代理排序/过滤示例"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # 搜索框
    search_edit = QLineEdit()
    search_edit.setPlaceholderText("输入搜索关键词...")
    layout.addWidget(search_edit)
    
    # 源模型
    source_model = QStringListModel(widget)
    source_model.setStringList([
        "Apple", "Apricot", "Banana", "Blueberry", "Cherry",
        "Date", "Fig", "Grape", "Kiwi", "Lemon",
        "Mango", "Orange", "Peach", "Pear", "Plum"
    ])
    
    # 代理模型 (用于过滤和排序)
    proxy_model = QSortFilterProxyModel(widget)
    proxy_model.setSourceModel(source_model)
    proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
    
    # 连接搜索框
    search_edit.textChanged.connect(proxy_model.setFilterRegularExpression)
    
    # 视图
    list_view = QListView()
    list_view.setModel(proxy_model)
    
    layout.addWidget(QLabel("QSortFilterProxyModel - 过滤和排序"))
    layout.addWidget(list_view)
    
    return widget


def main():
    app = QApplication(sys.argv)
    
    print("=== PySide6 模型/视图示例 ===\n")
    
    main_window = QMainWindow()
    main_window.setWindowTitle("PySide6 Model/View Demo")
    main_window.resize(700, 500)
    
    tab_widget = QTabWidget()
    tab_widget.addTab(create_list_widget_demo(), "ListWidget")
    tab_widget.addTab(create_table_widget_demo(), "TableWidget")
    tab_widget.addTab(create_tree_widget_demo(), "TreeWidget")
    tab_widget.addTab(create_model_view_demo(), "Model/View")
    tab_widget.addTab(create_proxy_model_demo(), "ProxyModel")
    
    main_window.setCentralWidget(tab_widget)
    main_window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
