#!/usr/bin/env clojure -M
;; PySide6 Todo App Demo (Clojure + libpython-clj)
;; A feature-rich TODO application with priorities, tags, and persistence
;; Note: macOS 需要使用 -XstartOnFirstThread JVM 参数运行

(require '[libpython-clj2.python :as py]
         '[clojure.data.json :as json])

(py/initialize!)

(def FilterMode
  {:ALL 0 :ACTIVE 1 :DONE 2})

(defn data-file-path []
  "Get the path for storing todo data."
  (let [QStandardPaths (py/import-module "PySide6.QtCore")
        pathlib (py/import-module "pathlib")
        os (py/import-module "os")
        data-dir (. QStandardPaths writableLocation 
                    (py/->py-object (.-AppDataLocation QStandardPaths)))]
    (. (py/py. pathlib Path data-dir) mkdir :parents true :exist_ok true)
    (py/py. os path join data-dir "todos.json")))

(defn priority-color [priority]
  "Get color for a given priority."
  (case priority
    "High" "#ef4444"
    "Medium" "#f59e0b"
    "Low" "#10b981"
    "#9ca3af"))

(defn update-item-label [item]
  "Update the display label of an item."
  (let [Qt (py/import-module "PySide6.QtCore")
        base-text (py/py. item data (.-UserRole Qt) 3)
        priority (or (py/py. item data (.-UserRole Qt) 1) "Medium")
        tag (or (py/py. item data (.-UserRole Qt) 2) "")
        base (or base-text "")
        suffix (str " [" priority "]" (if (seq tag) (str " #" tag) ""))]
    (py/py. item setText (str base suffix))
    (py/py. item setForeground (priority-color priority))))

(defn save-tasks [list-widget]
  "Save tasks to JSON file."
  (let [Qt (py/import-module "PySide6.QtCore")
        tasks (atom [])
        count (py/py. list-widget count)]
    (doseq [i (range count)]
      (let [item (py/py. list-widget item i)
            task {:text (py/py. item text)
                  :done (= (py/py. item checkState) (.-Checked Qt))
                  :createdAt (or (py/py. item data (.-UserRole Qt)) "")
                  :priority (or (py/py. item data (.-UserRole Qt) 1) "Medium")
                  :tag (or (py/py. item data (.-UserRole Qt) 2) ""}]
        (swap! tasks conj task)))
    (try
      (spit (data-file-path) (json/write-str @tasks))
      (catch Exception e
        (println "Error saving tasks:" e)))))

(defn load-tasks [list-widget loading-atom]
  "Load tasks from JSON file."
  (let [Qt (py/import-module "PySide6.QtCore")
        QListWidgetItem (py/->py-object 
                         (py/get-attr (py/import-module "PySide6.QtWidgets") 
                                      "QListWidgetItem"))]
    (try
      (let [tasks (json/read-str (slurp (data-file-path)) :key-fn keyword)]
        (doseq [task tasks]
          (let [raw-text (:text task)
                done (:done task false)
                created-at (:createdAt task "")
                priority (:priority task "Medium")
                tag (:tag task "")
                base-text (if (clojure.string/includes? raw-text " [")
                           (first (clojure.string/split raw-text #" \["))
                           raw-text)
                item (py/py. QListWidgetItem)]
            (py/py. item setFlags 
                    (bit-or (py/py. item flags)
                            (.-ItemIsUserCheckable Qt)
                            (.-ItemIsEditable Qt)))
            (py/py. item setCheckState (if done (.-Checked Qt) (.-Unchecked Qt)))
            (py/py. item setData (.-UserRole Qt) created-at)
            (py/py. item setData (.-UserRole Qt) priority 1)
            (py/py. item setData (.-UserRole Qt) tag 2)
            (py/py. item setData (.-UserRole Qt) base-text 3)
            (update-item-label item)
            (py/py. list-widget addItem item))))
      (catch java.io.FileNotFoundException _
        nil)
      (catch Exception e
        (println "Error loading tasks:" e)))))

(defn run-todo-app []
  "Run the Todo application."
  (py/run-simple-string 
   (str 
    "
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel,
    QFrame, QComboBox, QInputDialog, QButtonGroup
)
from PySide6.QtCore import Qt, QStandardPaths
from datetime import datetime
import json
import os
from pathlib import Path

app = QApplication([])
app.setStyle('Fusion')

# Setup palette
palette = app.palette()
palette.setColor(palette.ColorRole.Window, '#f5f7fa')
palette.setColor(palette.ColorRole.Base, '#ffffff')
palette.setColor(palette.ColorRole.Button, '#eef2f6')
palette.setColor(palette.ColorRole.Highlight, '#2f6fed')
palette.setColor(palette.ColorRole.HighlightedText, '#ffffff')
app.setPalette(palette)

def data_file_path():
    data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    return os.path.join(data_dir, 'todos.json')

def priority_color(priority):
    colors = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#10b981'}
    return colors.get(priority, '#9ca3af')

def update_item_label(item):
    base = item.data(Qt.UserRole + 3) or ''
    priority = item.data(Qt.UserRole + 1) or 'Medium'
    tag = item.data(Qt.UserRole + 2) or ''
    suffix = f' [{priority}]'
    if tag:
        suffix += f' #{tag}'
    item.setText(base + suffix)
    item.setForeground(priority_color(priority))

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Todo App')
        self.resize(560, 680)
        self.loading = True
        self.current_filter = 0  # ALL
        self._setup_ui()
        self._setup_styles()
        self._connect_signals()
        self.load_tasks()
        self.loading = False
        self.update_stats()
        self.update_empty_state()
        self.apply_filter()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        self.title = QLabel('Todo App')
        self.title.setObjectName('Title')
        self.subtitle = QLabel('Prioritized and tagged tasks with persistence.')
        self.subtitle.setObjectName('Subtitle')
        
        self.input_card = QFrame()
        self.input_card.setObjectName('Card')
        input_layout = QGridLayout(self.input_card)
        input_layout.setContentsMargins(12, 12, 12, 12)
        input_layout.setHorizontalSpacing(10)
        input_layout.setVerticalSpacing(10)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Add a task...')
        
        self.priority_box = QComboBox()
        self.priority_box.addItems(['High', 'Medium', 'Low'])
        self.priority_box.setCurrentText('Medium')
        
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText('Tag (optional)')
        
        self.add_button = QPushButton('Add')
        self.add_button.setObjectName('Primary')
        self.edit_button = QPushButton('Edit')
        
        input_layout.addWidget(self.input_field, 0, 0, 1, 2)
        input_layout.addWidget(self.priority_box, 0, 2)
        input_layout.addWidget(self.tag_input, 1, 0, 1, 2)
        input_layout.addWidget(self.add_button, 1, 2)
        input_layout.addWidget(self.edit_button, 2, 2)
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setObjectName('TaskList')
        
        self.filter_row = QFrame()
        self.filter_row.setObjectName('Card')
        filter_layout = QHBoxLayout(self.filter_row)
        filter_layout.setContentsMargins(12, 8, 12, 8)
        filter_layout.setSpacing(8)
        
        self.all_button = QPushButton('All')
        self.active_button = QPushButton('Active')
        self.done_button = QPushButton('Done')
        
        for btn in (self.all_button, self.active_button, self.done_button):
            btn.setCheckable(True)
        self.all_button.setChecked(True)
        
        self.filters = QButtonGroup(self)
        self.filters.setExclusive(True)
        self.filters.addButton(self.all_button, 0)
        self.filters.addButton(self.active_button, 1)
        self.filters.addButton(self.done_button, 2)
        
        filter_layout.addWidget(self.all_button)
        filter_layout.addWidget(self.active_button)
        filter_layout.addWidget(self.done_button)
        filter_layout.addStretch()
        
        status_row = QHBoxLayout()
        self.stats_label = QLabel('0 total, 0 active, 0 done')
        self.remove_button = QPushButton('Remove Selected')
        self.clear_button = QPushButton('Clear Completed')
        status_row.addWidget(self.stats_label)
        status_row.addStretch()
        status_row.addWidget(self.remove_button)
        status_row.addWidget(self.clear_button)
        
        self.empty_state = QLabel('No tasks yet. Add one above.')
        self.empty_state.setObjectName('EmptyState')
        self.empty_state.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.input_card)
        layout.addWidget(self.filter_row)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.empty_state)
        layout.addLayout(status_row)
    
    def _setup_styles(self):
        self.setStyleSheet('''
            QLabel#Title { font-size: 24px; font-weight: 600; color: #111827; }
            QLabel#Subtitle { color: #6b7280; }
            QLabel#EmptyState { color: #9ca3af; padding: 18px; }
            QFrame#Card { background: white; border: 1px solid #e5e7eb; border-radius: 10px; }
            QLineEdit { padding: 8px 10px; border: 1px solid #d1d5db; border-radius: 8px; }
            QLineEdit:focus { border-color: #2f6fed; }
            QComboBox { padding: 6px 10px; border: 1px solid #d1d5db; border-radius: 8px; }
            QPushButton { padding: 8px 12px; border-radius: 8px; background: #eef2f6; border: 1px solid #d7dee7; }
            QPushButton:hover { background: #e2e8f0; }
            QPushButton#Primary { background: #2f6fed; color: white; border: none; }
            QPushButton#Primary:hover { background: #255ad0; }
            QPushButton:checked { background: #2f6fed; color: white; border: none; }
            QListWidget#TaskList { background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 6px; }
            QListWidget::item { padding: 6px; }
            QListWidget::item:selected { background: #e5edff; color: #111827; }
        ''')
    
    def _connect_signals(self):
        self.add_button.clicked.connect(self.add_task)
        self.input_field.returnPressed.connect(self.add_button.click)
        self.edit_button.clicked.connect(self.edit_task)
        self.remove_button.clicked.connect(self.remove_selected)
        self.clear_button.clicked.connect(self.clear_completed)
        self.list_widget.itemChanged.connect(self.on_item_changed)
        self.filters.idClicked.connect(self.on_filter_changed)
    
    def save_tasks(self):
        tasks = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tasks.append({
                'text': item.text(),
                'done': item.checkState() == Qt.Checked,
                'createdAt': item.data(Qt.UserRole) or '',
                'priority': item.data(Qt.UserRole + 1) or 'Medium',
                'tag': item.data(Qt.UserRole + 2) or ''
            })
        try:
            with open(data_file_path(), 'w') as f:
                json.dump(tasks, f)
        except Exception as e:
            print(f'Error saving tasks: {e}')
    
    def load_tasks(self):
        try:
            with open(data_file_path(), 'r') as f:
                tasks = json.load(f)
            for task in tasks:
                raw_text = task.get('text', '')
                done = task.get('done', False)
                created_at = task.get('createdAt', '')
                priority = task.get('priority', 'Medium')
                tag = task.get('tag', '')
                base_text = raw_text.split(' [')[0] if ' [' in raw_text else raw_text
                
                item = QListWidgetItem()
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
                item.setCheckState(Qt.Checked if done else Qt.Unchecked)
                item.setData(Qt.UserRole, created_at)
                item.setData(Qt.UserRole + 1, priority)
                item.setData(Qt.UserRole + 2, tag)
                item.setData(Qt.UserRole + 3, base_text)
                update_item_label(item)
                self.list_widget.addItem(item)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f'Error loading tasks: {e}')
    
    def update_empty_state(self):
        is_empty = self.list_widget.count() == 0
        self.empty_state.setVisible(is_empty)
        self.list_widget.setVisible(not is_empty)
    
    def update_stats(self):
        total = self.list_widget.count()
        done = sum(1 for i in range(total) if self.list_widget.item(i).checkState() == Qt.Checked)
        active = total - done
        self.stats_label.setText(f'{total} total, {active} active, {done} done')
    
    def apply_filter(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            done = item.checkState() == Qt.Checked
            if self.current_filter == 1 and done:  # ACTIVE
                item.setHidden(True)
            elif self.current_filter == 2 and not done:  # DONE
                item.setHidden(True)
            else:
                item.setHidden(False)
    
    def add_task(self):
        raw_text = self.input_field.text().strip()
        if not raw_text:
            return
        item = QListWidgetItem()
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        item.setCheckState(Qt.Unchecked)
        item.setData(Qt.UserRole, datetime.now().isoformat())
        item.setData(Qt.UserRole + 1, self.priority_box.currentText())
        item.setData(Qt.UserRole + 2, self.tag_input.text().strip())
        item.setData(Qt.UserRole + 3, raw_text)
        update_item_label(item)
        self.list_widget.addItem(item)
        self.input_field.clear()
        self.tag_input.clear()
        self.input_field.setFocus()
        self.update_stats()
        self.update_empty_state()
        self.apply_filter()
        self.save_tasks()
    
    def edit_task(self):
        item = self.list_widget.currentItem()
        if not item:
            return
        current_text = item.data(Qt.UserRole + 3) or ''
        text, ok = QInputDialog.getText(self, 'Edit Task', 'Task:', QLineEdit.Normal, current_text)
        if ok and text.strip():
            item.setData(Qt.UserRole + 3, text.strip())
            update_item_label(item)
            self.save_tasks()
    
    def remove_selected(self):
        row = self.list_widget.currentRow()
        if row < 0:
            return
        self.list_widget.takeItem(row)
        self.update_stats()
        self.update_empty_state()
        self.save_tasks()
    
    def clear_completed(self):
        for i in range(self.list_widget.count() - 1, -1, -1):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                self.list_widget.takeItem(i)
        self.update_stats()
        self.update_empty_state()
        self.save_tasks()
    
    def on_item_changed(self, item):
        if self.loading:
            return
        if item:
            update_item_label(item)
        self.update_stats()
        self.apply_filter()
        self.save_tasks()
    
    def on_filter_changed(self, filter_id):
        self.current_filter = filter_id
        self.apply_filter()

print('=== PySide6 Todo App (via Clojure) ===')
print('Data is saved to:', data_file_path())

window = TodoApp()
window.show()
app.exec()
")))

(defn -main
  [& args]
  (println "=== PySide6 Todo App (Clojure + libpython-clj) ===")
  (println "注意: macOS 必须使用 -XstartOnFirstThread JVM 参数")
  
  (run-todo-app)
  
  (println "\n=== 完成 ==="))

(-main)
