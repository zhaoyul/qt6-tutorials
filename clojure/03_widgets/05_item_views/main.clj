#!/usr/bin/env clojure -M
;; PySide6 模型/视图示例 (Clojure + libpython-clj)
;; 注意：macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py])

(py/initialize!)

(defn -main
  [& args]
  (println "=== PySide6 模型/视图示例 (Clojure) ===")

  (py/run-simple-string "
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QTreeWidget, QTreeWidgetItem, QListView, QLineEdit, QLabel, QWidget, QStyle,
    QHeaderView
)
from PySide6.QtCore import Qt, QSize, QStringListModel, QSortFilterProxyModel
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
import sys

def create_list_widget_demo():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    list_widget = QListWidget()

    list_widget.addItem('普通项目 1')
    list_widget.addItem('普通项目 2')

    icon_item = QListWidgetItem(
        QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon),
        '带图标的项目'
    )
    list_widget.addItem(icon_item)

    check_item = QListWidgetItem('可选中项目')
    check_item.setFlags(check_item.flags() | Qt.ItemIsUserCheckable)
    check_item.setCheckState(Qt.Unchecked)
    list_widget.addItem(check_item)

    color_item = QListWidgetItem('彩色项目')
    color_item.setForeground(Qt.blue)
    color_item.setBackground(QColor(255, 255, 200))
    list_widget.addItem(color_item)

    list_widget.setSelectionMode(QListWidget.ExtendedSelection)
    list_widget.itemClicked.connect(lambda item: print(f'点击: {item.text()}'))

    layout.addWidget(QLabel('QListWidget - 便捷列表控件'))
    layout.addWidget(list_widget)

    btn_layout = QHBoxLayout()
    add_btn = QPushButton('添加')
    remove_btn = QPushButton('删除选中')
    add_btn.clicked.connect(lambda: list_widget.addItem(f'新项目 {list_widget.count() + 1}'))
    remove_btn.clicked.connect(lambda: [list_widget.takeItem(list_widget.row(item))
                                        for item in list_widget.selectedItems()])
    btn_layout.addWidget(add_btn)
    btn_layout.addWidget(remove_btn)
    layout.addLayout(btn_layout)

    return widget

def create_table_widget_demo():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    table_widget = QTableWidget(5, 4)

    table_widget.setHorizontalHeaderLabels(['姓名', '年龄', '城市', '职业'])
    names = ['张三', '李四', '王五', '赵六', '钱七']
    ages = ['25', '30', '28', '35', '22']
    cities = ['北京', '上海', '广州', '深圳', '杭州']
    jobs = ['工程师', '设计师', '产品经理', '数据分析', '运营']

    for row in range(5):
        table_widget.setItem(row, 0, QTableWidgetItem(names[row]))
        table_widget.setItem(row, 1, QTableWidgetItem(ages[row]))
        table_widget.setItem(row, 2, QTableWidgetItem(cities[row]))
        table_widget.setItem(row, 3, QTableWidgetItem(jobs[row]))

    table_widget.horizontalHeader().setStretchLastSection(True)
    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
    table_widget.setSortingEnabled(True)
    table_widget.setAlternatingRowColors(True)
    table_widget.setSelectionBehavior(QTableWidget.SelectRows)

    layout.addWidget(QLabel('QTableWidget - 便捷表格控件'))
    layout.addWidget(table_widget)
    return widget

def create_tree_widget_demo():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    tree_widget = QTreeWidget()
    tree_widget.setHeaderLabels(['名称', '类型', '大小'])
    tree_widget.setColumnCount(3)

    root1 = QTreeWidgetItem(tree_widget, ['项目A', '文件夹', ''])
    root2 = QTreeWidgetItem(tree_widget, ['项目B', '文件夹', ''])

    QTreeWidgetItem(root1, ['main.cpp', 'C++ 源文件', '10 KB'])
    QTreeWidgetItem(root1, ['main.h', 'C++ 头文件', '2 KB'])
    sub_folder = QTreeWidgetItem(root1, ['src', '文件夹', ''])
    QTreeWidgetItem(sub_folder, ['utils.cpp', 'C++ 源文件', '5 KB'])
    QTreeWidgetItem(sub_folder, ['utils.h', 'C++ 头文件', '1 KB'])
    QTreeWidgetItem(root2, ['readme.md', 'Markdown', '3 KB'])
    QTreeWidgetItem(root2, ['config.json', 'JSON', '1 KB'])

    tree_widget.expandAll()
    tree_widget.header().setSectionResizeMode(0, QHeaderView.Stretch)

    layout.addWidget(QLabel('QTreeWidget - 便捷树形控件'))
    layout.addWidget(tree_widget)
    return widget

def create_model_view_demo():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(QLabel('Model/View 分离 - 一个模型，多个视图'))

    model = QStandardItemModel(widget)
    for item_text in ['苹果', '香蕉', '橙子', '葡萄', '西瓜']:
        std_item = QStandardItem(item_text)
        std_item.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        model.appendRow(std_item)

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
    layout.addWidget(QLabel('两个视图共享同一个模型，修改会同步'))
    return widget

def create_proxy_model_demo():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    search_edit = QLineEdit()
    search_edit.setPlaceholderText('输入搜索关键词...')
    layout.addWidget(search_edit)

    source_model = QStringListModel(widget)
    source_model.setStringList([
        'Apple', 'Apricot', 'Banana', 'Blueberry', 'Cherry',
        'Date', 'Fig', 'Grape', 'Kiwi', 'Lemon',
        'Mango', 'Orange', 'Peach', 'Pear', 'Plum'
    ])

    proxy_model = QSortFilterProxyModel(widget)
    proxy_model.setSourceModel(source_model)
    proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
    search_edit.textChanged.connect(proxy_model.setFilterRegularExpression)

    list_view = QListView()
    list_view.setModel(proxy_model)
    layout.addWidget(QLabel('QSortFilterProxyModel - 过滤和排序'))
    layout.addWidget(list_view)
    return widget

app = QApplication(sys.argv)
print('=== PySide6 模型/视图示例 ===\\n')

main_window = QMainWindow()
main_window.setWindowTitle('PySide6 Model/View Demo')
main_window.resize(700, 500)

tab_widget = QTabWidget()
tab_widget.addTab(create_list_widget_demo(), 'ListWidget')
tab_widget.addTab(create_table_widget_demo(), 'TableWidget')
tab_widget.addTab(create_tree_widget_demo(), 'TreeWidget')
tab_widget.addTab(create_model_view_demo(), 'Model/View')
tab_widget.addTab(create_proxy_model_demo(), 'ProxyModel')

main_window.setCentralWidget(tab_widget)
main_window.show()
app.exec()
")

  (println "\n=== 完成 ==="))

(-main)
