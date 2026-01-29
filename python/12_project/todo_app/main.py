#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PySide6 Todo App Demo

A feature-rich TODO application with:
- Task management with priorities (High, Medium, Low)
- Tags for categorization
- Data persistence using JSON
- Filtering (All, Active, Done)
- Statistics tracking
"""

import sys
import json
import os
from datetime import datetime
from enum import IntEnum
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel,
    QFrame, QComboBox, QInputDialog, QButtonGroup
)
from PySide6.QtCore import Qt, QStandardPaths


class FilterMode(IntEnum):
    ALL = 0
    ACTIVE = 1
    DONE = 2


def data_file_path() -> str:
    """Get the path for storing todo data."""
    data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    return os.path.join(data_dir, "todos.json")


def priority_color(priority: str) -> str:
    """Get color for a given priority."""
    colors = {
        "High": "#ef4444",
        "Medium": "#f59e0b",
        "Low": "#10b981"
    }
    return colors.get(priority, "#9ca3af")


def update_item_label(item: QListWidgetItem):
    """Update the display label of an item."""
    base_text = item.data(Qt.UserRole + 3) or ""
    priority = item.data(Qt.UserRole + 1) or "Medium"
    tag = item.data(Qt.UserRole + 2) or ""
    
    suffix = f" [{priority}]"
    if tag:
        suffix += f" #{tag}"
    
    item.setText(base_text + suffix)
    item.setForeground(priority_color(priority))


class TodoApp(QWidget):
    """Main Todo Application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo App")
        self.resize(560, 680)
        
        self.loading = True
        self.current_filter = FilterMode.ALL
        
        self._setup_ui()
        self._setup_styles()
        self._connect_signals()
        
        self.load_tasks()
        self.loading = False
        
        self.update_stats()
        self.update_empty_state()
        self.apply_filter()
    
    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Title
        self.title = QLabel("Todo App")
        self.title.setObjectName("Title")
        self.subtitle = QLabel("Prioritized and tagged tasks with persistence.")
        self.subtitle.setObjectName("Subtitle")
        
        # Input card
        self.input_card = QFrame()
        self.input_card.setObjectName("Card")
        input_layout = QGridLayout(self.input_card)
        input_layout.setContentsMargins(12, 12, 12, 12)
        input_layout.setHorizontalSpacing(10)
        input_layout.setVerticalSpacing(10)
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Add a task...")
        
        self.priority_box = QComboBox()
        self.priority_box.addItems(["High", "Medium", "Low"])
        self.priority_box.setCurrentText("Medium")
        
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Tag (optional)")
        
        self.add_button = QPushButton("Add")
        self.add_button.setObjectName("Primary")
        self.edit_button = QPushButton("Edit")
        
        input_layout.addWidget(self.input_field, 0, 0, 1, 2)
        input_layout.addWidget(self.priority_box, 0, 2)
        input_layout.addWidget(self.tag_input, 1, 0, 1, 2)
        input_layout.addWidget(self.add_button, 1, 2)
        input_layout.addWidget(self.edit_button, 2, 2)
        
        # Task list
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setObjectName("TaskList")
        
        # Filter row
        self.filter_row = QFrame()
        self.filter_row.setObjectName("Card")
        filter_layout = QHBoxLayout(self.filter_row)
        filter_layout.setContentsMargins(12, 8, 12, 8)
        filter_layout.setSpacing(8)
        
        self.all_button = QPushButton("All")
        self.active_button = QPushButton("Active")
        self.done_button = QPushButton("Done")
        
        for btn in (self.all_button, self.active_button, self.done_button):
            btn.setCheckable(True)
        self.all_button.setChecked(True)
        
        self.filters = QButtonGroup(self)
        self.filters.setExclusive(True)
        self.filters.addButton(self.all_button, FilterMode.ALL)
        self.filters.addButton(self.active_button, FilterMode.ACTIVE)
        self.filters.addButton(self.done_button, FilterMode.DONE)
        
        filter_layout.addWidget(self.all_button)
        filter_layout.addWidget(self.active_button)
        filter_layout.addWidget(self.done_button)
        filter_layout.addStretch()
        
        # Status row
        status_row = QHBoxLayout()
        self.stats_label = QLabel("0 total, 0 active, 0 done")
        self.remove_button = QPushButton("Remove Selected")
        self.clear_button = QPushButton("Clear Completed")
        status_row.addWidget(self.stats_label)
        status_row.addStretch()
        status_row.addWidget(self.remove_button)
        status_row.addWidget(self.clear_button)
        
        # Empty state
        self.empty_state = QLabel("No tasks yet. Add one above.")
        self.empty_state.setObjectName("EmptyState")
        self.empty_state.setAlignment(Qt.AlignCenter)
        
        # Add widgets to main layout
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addWidget(self.input_card)
        layout.addWidget(self.filter_row)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.empty_state)
        layout.addLayout(status_row)
    
    def _setup_styles(self):
        """Setup application styles."""
        self.setStyleSheet("""
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
        """)
    
    def _connect_signals(self):
        """Connect signal handlers."""
        self.add_button.clicked.connect(self.add_task)
        self.input_field.returnPressed.connect(self.add_button.click)
        self.edit_button.clicked.connect(self.edit_task)
        self.remove_button.clicked.connect(self.remove_selected)
        self.clear_button.clicked.connect(self.clear_completed)
        self.list_widget.itemChanged.connect(self.on_item_changed)
        self.filters.idClicked.connect(self.on_filter_changed)
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        tasks = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tasks.append({
                "text": item.text(),
                "done": item.checkState() == Qt.Checked,
                "createdAt": item.data(Qt.UserRole) or "",
                "priority": item.data(Qt.UserRole + 1) or "Medium",
                "tag": item.data(Qt.UserRole + 2) or ""
            })
        
        try:
            with open(data_file_path(), 'w') as f:
                json.dump(tasks, f)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        try:
            with open(data_file_path(), 'r') as f:
                tasks = json.load(f)
            
            for task in tasks:
                raw_text = task.get("text", "")
                done = task.get("done", False)
                created_at = task.get("createdAt", "")
                priority = task.get("priority", "Medium")
                tag = task.get("tag", "")
                
                # Extract base text (remove priority suffix if present)
                if " [" in raw_text:
                    base_text = raw_text.split(" [")[0]
                else:
                    base_text = raw_text
                
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
            print(f"Error loading tasks: {e}")
    
    def update_empty_state(self):
        """Update the visibility of empty state label."""
        is_empty = self.list_widget.count() == 0
        self.empty_state.setVisible(is_empty)
        self.list_widget.setVisible(not is_empty)
    
    def update_stats(self):
        """Update statistics display."""
        total = self.list_widget.count()
        done = sum(1 for i in range(total) 
                   if self.list_widget.item(i).checkState() == Qt.Checked)
        active = total - done
        self.stats_label.setText(f"{total} total, {active} active, {done} done")
    
    def apply_filter(self):
        """Apply current filter to task list."""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            done = item.checkState() == Qt.Checked
            
            if self.current_filter == FilterMode.ACTIVE and done:
                item.setHidden(True)
            elif self.current_filter == FilterMode.DONE and not done:
                item.setHidden(True)
            else:
                item.setHidden(False)
    
    def add_task(self):
        """Add a new task."""
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
        """Edit the selected task."""
        item = self.list_widget.currentItem()
        if not item:
            return
        
        current_text = item.data(Qt.UserRole + 3) or ""
        text, ok = QInputDialog.getText(
            self, "Edit Task", "Task:", 
            QLineEdit.Normal, current_text
        )
        
        if ok and text.strip():
            item.setData(Qt.UserRole + 3, text.strip())
            update_item_label(item)
            self.save_tasks()
    
    def remove_selected(self):
        """Remove the selected task."""
        row = self.list_widget.currentRow()
        if row < 0:
            return
        
        self.list_widget.takeItem(row)
        self.update_stats()
        self.update_empty_state()
        self.save_tasks()
    
    def clear_completed(self):
        """Remove all completed tasks."""
        for i in range(self.list_widget.count() - 1, -1, -1):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                self.list_widget.takeItem(i)
        
        self.update_stats()
        self.update_empty_state()
        self.save_tasks()
    
    def on_item_changed(self, item: QListWidgetItem):
        """Handle item changes (check state, edit)."""
        if self.loading:
            return
        if item:
            update_item_label(item)
        self.update_stats()
        self.apply_filter()
        self.save_tasks()
    
    def on_filter_changed(self, filter_id: int):
        """Handle filter button clicks."""
        self.current_filter = FilterMode(filter_id)
        self.apply_filter()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Setup palette
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, "#f5f7fa")
    palette.setColor(palette.ColorRole.Base, "#ffffff")
    palette.setColor(palette.ColorRole.Button, "#eef2f6")
    palette.setColor(palette.ColorRole.Highlight, "#2f6fed")
    palette.setColor(palette.ColorRole.HighlightedText, "#ffffff")
    app.setPalette(palette)
    
    print("=== PySide6 Todo App ===")
    print("Data is saved to:", data_file_path())
    
    window = TodoApp()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
