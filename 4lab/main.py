import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QRegExpValidator


class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр базы данных")
        self.setGeometry(300, 300, 800, 600)

        self.setupUI()  # Настройки интерфейса
        self.connect_to_db()  # Подключения к базе данных
        self.load_data()  # Загрузки данных в таблицу
        self.initUI()

    def setupUI(self): 
        self.main_widget = QWidget(self)  # Основной виджет
        self.setCentralWidget(self.main_widget)
        self.search_box = QLineEdit(self)  # Поле для поиска
        self.search_box.setPlaceholderText("Поиск по заголовку...")
        self.search_box.textChanged.connect(self.filter_data)

        # Кнопки и их действия
        self.add_button = QPushButton("Добавить", self)
        self.add_button.clicked.connect(self.add_posts)
        self.delete_button = QPushButton("Удалить", self)
        self.delete_button.clicked.connect(self.delete_record)
        self.refresh_button = QPushButton("Обновить", self)
        self.refresh_button.clicked.connect(self.refresh_data)

        # Макет кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)

        # Основной макет
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.search_box)
        self.table_view = QTableView(self)
        self.table_view.setAlternatingRowColors(True)
        layout.addWidget(self.table_view)
        self.main_widget.setLayout(layout)

    def connect_to_db(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("posts.db")
        if not self.db.open():
            print("Не удалось подключиться к базе данных.")
            return
        self.model = QSqlTableModel(self)
        self.model.setTable("posts")
        self.model.select()
        self.table_view.setModel(self.model)
        self.table_view.verticalHeader().setVisible(False)

    def load_data(self):
        self.model.select()
        QTimer.singleShot(0, self.setwidths)

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setwidths(self):
        total_width = self.table_view.width()
        title_percentage = 30
        body_percentage = 55
        id_percentage = 5
        user_id_percentage = 10
        
        title_width = int((title_percentage / 100) * total_width)
        body_width = int((body_percentage / 100) * total_width)
        id_width = int((id_percentage / 100) * total_width)
        user_id_width = int((user_id_percentage / 100) * total_width)
        self.table_view.setColumnWidth(0, id_width)
        self.table_view.setColumnWidth(1, user_id_width)
        self.table_view.setColumnWidth(2, title_width)
        self.table_view.setColumnWidth(3, body_width)

    def resizeEvent(self, event):
        self.setwidths()
        super().resizeEvent(event)

    def filter_data(self):
        filter_text = self.search_box.text()
        self.model.setFilter(f"title LIKE '%{filter_text}%'")
        self.model.select()

    def add_posts(self):
        dialog = QWidget()
        dialog.setWindowTitle("Добавить запись")
        layout = QFormLayout()

        user_id_input = QLineEdit(dialog)
        reg_exp = QRegExp("^[0-9]*$")
        validator = QRegExpValidator(reg_exp, user_id_input)
        user_id_input.setValidator(validator)

        title_input = QLineEdit(dialog)
        body_input = QLineEdit(dialog)

        layout.addRow("User ID:", user_id_input)
        layout.addRow("Title:", title_input)
        layout.addRow("Body:", body_input)

        add_button = QPushButton("Добавить", dialog)
        add_button.clicked.connect(lambda: self.save_new_posts(user_id_input.text(), title_input.text(), body_input.text(), dialog))
        layout.addWidget(add_button)

        dialog.setLayout(layout)
        dialog.setGeometry(400, 400, 300, 200)
        dialog.show()

    def save_new_posts(self, user_id, title, body, dialog):
        query = QSqlQuery()
        query.prepare("INSERT INTO posts (user_id, title, body) VALUES (?, ?, ?)")
        query.addBindValue(user_id)
        query.addBindValue(title)
        query.addBindValue(body)
        if query.exec_():
            self.load_data()
            dialog.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить запись.")

    def delete_record(self):
        index = self.table_view.currentIndex()
        if index.isValid():
            record_id = self.model.index(index.row(), 0).data()
            reply = QMessageBox.question(self, 'Подтверждение', 'Вы уверены, что хотите удалить эту запись?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                query = QSqlQuery()
                query.prepare("DELETE FROM posts WHERE id = ?")
                query.addBindValue(record_id)
                if query.exec_():
                    self.load_data()
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить запись.")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")

    def refresh_data(self):
        if self.model.isDirty():
            if not self.model.submitAll():
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить изменения.")
                return
        self.model.select()
        QMessageBox.information(self, "Обновление", "Данные успешно обновлены!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseViewer()
    window.show()
    sys.exit(app.exec_())
