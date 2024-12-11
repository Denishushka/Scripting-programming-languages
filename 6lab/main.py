import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QLineEdit, QWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns


class DataAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Analysis App")
        self.setGeometry(100, 100, 1200,600)
        
        self.data = None  # Для хранения загруженных данных
        self.file_path = None 
        
        # Основной виджет и компоновка
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Кнопка загрузки данных
        self.load_button = QPushButton("Load CSV")
        self.load_button.clicked.connect(self.load_data)
        main_layout.addWidget(self.load_button)
        
        # Поле для отображения статистики
        self.stats_label = QLabel("Statistics will appear here.")
        main_layout.addWidget(self.stats_label)
        
        # Выбор типа графика
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(["Line Chart", "Histogram", "Pie Chart"])
        self.chart_type_combo.currentIndexChanged.connect(self.plot_data)  # Сигнал для смены графика
        main_layout.addWidget(self.chart_type_combo)
        
        # Поле для ввода данных
        self.manual_input_layout = QVBoxLayout()

        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Enter Date ")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Enter Category")

        self.value1_input = QLineEdit()
        self.value1_input.setPlaceholderText("Enter Value1")

        self.value2_input = QLineEdit()
        self.value2_input.setPlaceholderText("Enter Value2")

        self.boolean_flag_input = QLineEdit()
        self.boolean_flag_input.setPlaceholderText("Enter BooleanFlag")

        # Добавляем поля для ввода в компоновку
        # self.manual_input_layout.addWidget(self.date_input)
        # self.manual_input_layout.addWidget(self.category_input)
        # self.manual_input_layout.addWidget(self.value1_input)
        # self.manual_input_layout.addWidget(self.value2_input)
        # self.manual_input_layout.addWidget(self.boolean_flag_input)
        
        # Кнопка для добавления данных
        # self.add_data_button = QPushButton("Add Data")
        # self.add_data_button.clicked.connect(self.add_data)
        # self.manual_input_layout.addWidget(self.add_data_button)

        main_layout.addLayout(self.manual_input_layout)
        
        # Поле для отображения графика
        self.figure = plt.figure(figsize=(10, 4))  # Устанавливаем размеры графика
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(1200, 600)  # Фиксированный размер канваса
        main_layout.addWidget(self.canvas)
    
    def load_data(self):
        # Выбор файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_path:
            # Сохраняем путь к файлу
            self.file_path = file_path
            self.data = pd.read_csv(file_path)
            self.update_stats()

    def get_file_path(self):
        # Метод для получения пути к файлу
        return self.file_path if self.file_path else None
    
    def update_stats(self):
        if self.data is not None:
            # Количество строк и столбцов
            num_rows, num_cols = self.data.shape
            stats = f"<b>Rows:</b> {num_rows} <br> <b>Columns:</b> {num_cols}<br><br>"

            # Описательная статистика
            describe_table = self.data.describe(include='all').transpose()
            describe_html = describe_table.to_html(classes="stats-table", border=0, justify='left')
            stats += describe_html

            # Установка HTML-формата для QLabel
            self.stats_label.setText(stats)
            self.stats_label.setStyleSheet("font-family: Arial; font-size: 12px;")
            self.plot_data()  # Обновить график
    
    def plot_data(self):
        if self.data is not None:
            chart_type = self.chart_type_combo.currentText()
            self.figure.clear()

            ax = self.figure.add_subplot(111)

            if chart_type == "Line Chart":
                if "Date" in self.data.columns and "Value1" in self.data.columns:
                    self.data.plot(x="Date", y="Value1", ax=ax, kind='line')
                    ax.set_title("Line Chart of Value1 by Date")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Value1")

                    # Отображение только каждой второй даты
                    dates = self.data["Date"]
                    ax.set_xticks(range(0, len(dates), 2))  # Каждая вторая дата
                    ax.set_xticklabels(dates[::2], rotation=75, ha='right')  # Уменьшаем угол и выравнивание

            elif chart_type == "Histogram":
                if "Date" in self.data.columns and "Value2" in self.data.columns:
                    sns.barplot(x="Date", y="Value2", data=self.data, ax=ax)
                    ax.set_title("Bar Chart of Value2 by Date")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Value2")

                    # Отображение только каждой второй даты
                    dates = self.data["Date"]
                    ax.set_xticks(range(0, len(dates), 2))  # Каждая вторая дата
                    ax.set_xticklabels(dates[::2], rotation=90, ha='right')  # Поворот на 90 градусов

            elif chart_type == "Pie Chart":
                if "Category" in self.data.columns:
                    self.data["Category"].value_counts().plot.pie(ax=ax, autopct='%1.1f%%')
                    ax.set_title("Pie Chart of Categories")

            # Используем tight_layout для автоматического подстраивания
            self.figure.tight_layout()

            # Отображаем график
            self.canvas.draw()

    def add_data(self):
        if self.data is not None:
            try:
                # Считываем данные из полей ввода
                new_data = {
                    "Date": self.date_input.text(),
                    "Category": self.category_input.text(),
                    "Value1": float(self.value1_input.text()),
                    "Value2": float(self.value2_input.text()),
                    "BooleanFlag": self.boolean_flag_input.text() == "True"  # Преобразуем в булево значение
                }

                # Преобразуем новую строку в DataFrame и добавляем с помощью pd.concat
                new_row = pd.DataFrame([new_data])
                self.data = pd.concat([self.data, new_row], ignore_index=True)

                # Обновляем статистику и график
                self.update_stats()

                # Очистка полей ввода
                self.date_input.clear()
                self.category_input.clear()
                self.value1_input.clear()
                self.value2_input.clear()
                self.boolean_flag_input.clear()

                # Сохранение обновленных данных обратно в файл
                file_path = self.get_file_path()
                if file_path:
                    self.data.to_csv(file_path, index=False)  # Записываем данные обратно в файл

            except ValueError as e:
                self.stats_label.setText(f"Error adding data: {e}")
        else:
            self.stats_label.setText("Load data before adding new entries.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalysisApp()
    window.show()
    sys.exit(app.exec())
