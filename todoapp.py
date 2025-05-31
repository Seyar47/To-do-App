import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QListWidget, QComboBox, QMessageBox,
    QFileDialog, QFrame, QListWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.init_ui_components()
        self.setup_ui()
        self.apply_styles()
        
    def init_ui_components(self):
        self.header_label = QLabel("✓ Todo List")
        self.header_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("✍ What needs to be done?")
        self.text_input.setMinimumHeight(45)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["🏠 Personal", "💼 Work", "🔥 Urgent"])
        self.category_combo.setMinimumHeight(45)
        
        # Filter section
        self.filter_label = QLabel("Filter by:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["📋 All Tasks", "🏠 Personal", "💼 Work", "🔥 Urgent"])
        self.filter_combo.setMinimumHeight(35)
        
        self.add_task_button = QPushButton("Add Task", self)
        self.remove_task_button = QPushButton("Remove Task", self)
        self.save_task_button = QPushButton("Save List", self)
        self.load_task_button = QPushButton("Load List", self)
        
        for button in [self.add_task_button, self.remove_task_button, 
                      self.save_task_button, self.load_task_button]:
            button.setMinimumHeight(40)
        
        self.tasks_list = QListWidget()
        self.tasks_list.setSpacing(2)
        self.tasks_list.setMinimumHeight(300)
        
        self.add_task_button.clicked.connect(self.add_task)
        self.remove_task_button.clicked.connect(self.remove_task)
        self.save_task_button.clicked.connect(self.save_tasks)
        self.load_task_button.clicked.connect(self.load_tasks)
        self.filter_combo.currentIndexChanged.connect(self.filter_by_category)
        self.text_input.returnPressed.connect(self.add_task)

    def setup_ui(self):
        self.setWindowTitle("Modern Todo App")
        self.resize(500, 700)
        
        # Create layouts
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        main_layout.addWidget(self.header_label)
        
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setSpacing(10)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.category_combo)
        main_layout.addWidget(input_frame)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_task_button)
        button_layout.addWidget(self.remove_task_button)
        main_layout.addLayout(button_layout)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.filter_label)
        filter_layout.addWidget(self.filter_combo, stretch=1)
        main_layout.addLayout(filter_layout)
        
        main_layout.addWidget(self.tasks_list)
        
        save_load_layout = QHBoxLayout()
        save_load_layout.addWidget(self.save_task_button)
        save_load_layout.addWidget(self.load_task_button)
        main_layout.addLayout(save_load_layout)
        
        self.setLayout(main_layout)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f2f5;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            
            QLabel {
                color: #1a1a1a;
                font-weight: 500;
            }
            
            #inputFrame {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #e1e4e8;
            }
            
            QLineEdit {
                padding: 12px;
                border: 2px solid #e1e4e8;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1a1a1a;
                font-size: 15px;
            }
            
            QLineEdit:focus {
                border-color: #0366d6;
            }
            
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
                padding: 10px;
                outline: none;
            }
            
            QListWidget::item {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 10px;
                margin: 2px 0px;
            }
            
            QListWidget::item:selected {
                background-color: #f1f8ff;
                border-color: #0366d6;
                color: #1a1a1a;
            }
            
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #e1e4e8;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1a1a1a;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                background-color: #0366d6;
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
            
            QPushButton:hover {
                background-color: #0256b9;
            }
            
            QPushButton:pressed {
                background-color: #014795;
            }
            
            #remove_task_button {
                background-color: #dc3545;
            }
            
            #remove_task_button:hover {
                background-color: #c82333;
            }
            
            QMessageBox {
                background-color: #ffffff;
            }
        """)

    def add_task(self):
        task = self.text_input.text().strip()
        if not task:
            return
            
        category = self.category_combo.currentText()
        display_text = f"{task} {category}"
        
        item = QListWidgetItem(display_text)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        
        if "Personal" in category:
            item.setBackground(QColor("#e3f2fd"))
        elif "Work" in category:
            item.setBackground(QColor("#f3e5f5"))
        elif "Urgent" in category:
            item.setBackground(QColor("#ffebee"))
            
        self.tasks_list.addItem(item)
        self.tasks.append((task, category))
        self.text_input.clear()

    def remove_task(self):
        current_row = self.tasks_list.currentRow()
        if current_row == -1:
            QMessageBox.information(self, "Selection Error", 
                                  "Please select a task to remove!")
            return
            
        self.tasks_list.takeItem(current_row)
        del self.tasks[current_row]

    def filter_by_category(self):
        selected_filter = self.filter_combo.currentText().replace("📋 ", "")
        self.tasks_list.clear()
        
        for task, category in self.tasks:
            if selected_filter == "All Tasks" or category == selected_filter:
                display_text = f"{task} {category}"
                item = QListWidgetItem(display_text)
                
                if "Personal" in category:
                    item.setBackground(QColor("#e3f2fd"))
                elif "Work" in category:
                    item.setBackground(QColor("#f3e5f5"))
                elif "Urgent" in category:
                    item.setBackground(QColor("#ffebee"))
                    
                self.tasks_list.addItem(item)

    def save_tasks(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Tasks", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w", encoding='utf-8') as file:
                    for task, category in self.tasks:
                        file.write(f"{task}|{category}\n")
                QMessageBox.information(self, "Success", "Tasks saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save tasks: {str(e)}")

    def load_tasks(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Load Tasks", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "r", encoding='utf-8') as file:
                    self.tasks_list.clear()
                    self.tasks = []
                    for line in file:
                        task_text, category = line.strip().split("|")
                        self.tasks.append((task_text, category))
                        display_text = f"{task_text} {category}"
                        item = QListWidgetItem(display_text)
                        
                        if "Personal" in category:
                            item.setBackground(QColor("#e3f2fd"))
                        elif "Work" in category:
                            item.setBackground(QColor("#f3e5f5"))
                        elif "Urgent" in category:
                            item.setBackground(QColor("#ffebee"))
                            
                        self.tasks_list.addItem(item)
                QMessageBox.information(self, "Success", "Tasks loaded successfully!")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "File not found!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tasks: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    todo_app = ToDoApp()
    todo_app.show()
    sys.exit(app.exec_())