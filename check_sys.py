import sys
import os
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget, QTableView, QHBoxLayout, QPushButton, QSplitter, QHeaderView, QCheckBox, QAbstractItemView, QFontDialog, QLineEdit, QDialog, QFormLayout
from PyQt5.QtGui import QPixmap, QImage, QColor, QBrush, QFont
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
import sys, os
import urllib.request

class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self.selected_rows = set()
        self.check_states = [False] * self._data.shape[0]

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1] + 1

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return QVariant()
                else:
                    return str(self._data.iloc[index.row(), index.column() - 1])
            elif role == Qt.CheckStateRole and index.column() == 0:
                return Qt.Checked if self.check_states[index.row()] else Qt.Unchecked
            elif role == Qt.BackgroundRole and index.row() in self.selected_rows:
                return QBrush(QColor("#ADD8E6"))
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.CheckStateRole and index.column() == 0:
            self.check_states[index.row()] = bool(value)
            self.layoutChanged.emit()
            return True
        return False

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Выбрать"
                else:
                    return str(self._data.columns[section - 1])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

    def get_checked_images(self):
        return [i for i, checked in enumerate(self.check_states) if checked]

    def set_selected_row(self, row_index):
        self.selected_rows = {row_index}
        self.layoutChanged.emit()


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.font = 'Arial'
        self.font_size = 30
        self.path = ""
        self.initUI()

    def initUI(self):
        layout = QFormLayout(self)

        # Поле для выбора шрифта
        self.font_button = QPushButton("Выбрать шрифт")
        self.font_button.clicked.connect(self.select_font)
        layout.addRow("Шрифт:", self.font_button)

        # Поле для выбора пути сохранения
        self.path_edit = QLineEdit(self)
        layout.addRow("Путь для сохранения:", self.path_edit)

        # Кнопка подтверждения
        self.confirm_button = QPushButton("Сохранить")
        self.confirm_button.clicked.connect(self.accept)
        layout.addWidget(self.confirm_button)

    def select_font(self):
        font, ok = QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font

    def get_settings(self):
        return self.font, self.path_edit.text()


class ImageEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.images = []
        self.current_image_index = 0
        self.file_data = None
        self.model = None
        self.font = QFont("Arial", 10)
        self.save_path = ""
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("Файл")

        loadFileAction = QAction("Загрузить файл (Excel, CSV, ODS)", self)
        loadFileAction.triggered.connect(self.load_file)
        fileMenu.addAction(loadFileAction)

        settingsAction = QAction("Настройки", self)
        settingsAction.triggered.connect(self.open_settings)
        fileMenu.addAction(settingsAction)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        table_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.select_all_button = QPushButton("Выбрать все")
        self.select_all_button.clicked.connect(self.select_all_images)
        button_layout.addWidget(self.select_all_button)

        self.process_button = QPushButton("Обработать выбранные изображения")
        self.process_button.clicked.connect(self.process_selected_images)
        button_layout.addWidget(self.process_button)
        button_layout.addStretch()

        self.table_view = QTableView()
        self.table_view.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_view.doubleClicked.connect(self.on_table_double_click)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_layout.addLayout(button_layout)
        table_layout.addWidget(self.table_view)

        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addLayout(table_layout)
        main_splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.image_label_before = QLabel("Изображение до обработки")
        self.image_label_before.setFixedSize(300, 300)
        self.image_label_before.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.image_label_before)

        self.prev_button = QPushButton("Предыдущее изображение")
        self.prev_button.clicked.connect(self.show_previous_image)
        right_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Следующее изображение")
        self.next_button.clicked.connect(self.show_next_image)
        right_layout.addWidget(self.next_button)

        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([400, 400])

    def load_file(self):
        filetypes = "All files (*.xls *.xlsx *.csv *.ods);;Excel (*.xls *.xlsx);;CSV (*.csv);;ODS (*.ods)"
        filepath, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", filetypes)
        
        if filepath:
            try:
                ext = os.path.splitext(filepath)[1]
                if ext in ['.xls', '.xlsx', '.ods']:
                    self.file_data = pd.read_excel(filepath)
                elif ext == '.csv':
                    self.file_data = pd.read_csv(filepath)
                self.display_table(self.file_data)
                self.load_all_images()
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")

    def display_table(self, data):
        self.model = PandasModel(data)
        self.table_view.setModel(self.model)

    def load_all_images(self):
        if self.file_data is not None and "Ссылка на фото" in self.file_data.columns:
            for index, row in self.file_data.iterrows():
                image_url = row["Ссылка на фото"]
                if pd.notna(image_url):
                    self.images.append(image_url)

            if self.images:
                self.current_image_index = 0
                self.show_image(self.images[self.current_image_index], self.image_label_before)
                self.highlight_current_row()

    def show_image(self, image_url, label):
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            qimage = QImage(image.tobytes(), image.width, image.height, image.width * 3, QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(qimage).scaled(label.width(), label.height(), Qt.KeepAspectRatio))
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")

    def show_next_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_image(self.images[self.current_image_index], self.image_label_before)
            self.highlight_current_row()

    def show_previous_image(self):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_image(self.images[self.current_image_index], self.image_label_before)
            self.highlight_current_row()

    def highlight_current_row(self):
        self.model.set_selected_row(self.current_image_index)

    def on_table_double_click(self, index: QModelIndex):
        row = index.row()
        if "Ссылка на фото" in self.file_data.columns and row < len(self.images):
            self.current_image_index = row
            image_url = self.images[self.current_image_index]
            self.show_image(image_url, self.image_label_before)
            self.highlight_current_row()

    def select_all_images(self):
        for row in range(self.model.rowCount()):
            self.model.check_states[row] = True
        self.model.layoutChanged.emit()

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.font, self.save_path = dialog.get_settings()
            print(f"Выбранный шрифт: {self.font.family()} {self.font.pointSize()}pt")
            print(f"Путь для сохранения: {self.save_path}")

    def download_url(url, output_filename):
        # Скачиваем файл с указанного URL
        response = urllib.request.urlopen(url)
        data = response.read()

        # Сохраняем файл под указанным именем
        with open(output_filename, 'wb') as f:
            f.write(data)
        
        print(f"Файл сохранен как: {output_filename}")

    def process_selected_images(self):
        selected_indices = self.model.get_checked_images()
        for i in selected_indices:
            image_url = self.images[i]
            image_name = os.path.basename(image_url)
            text_layers = [
                str(self.file_data.iloc[i][col])
                for col in self.file_data.columns if (col.startswith("Слой_") and pd.notna(self.file_data.iloc[i][col]))
            ]
            print(f"Обработка изображения: {image_name}")
            print(f"URL: {image_url}")
            print(f"Текстовые слои: {text_layers}")
            # Здесь добавить логику обработки изображения с использованием self.font и self.save_path

            tmp_path = 'tmp/'
            try:
                full_tmp_path = tmp_path + image_name
                self.download_url(image_url, full_tmp_path)
            except Exception as e:
                print(f"Ошибка загрузки url картинки: {e}")

            # парсим в строку
            text = ' | '.join(text_layers)
            os.system(f'C:\\"Program Files\"\\"GIMP 2\"\\bin\gimp-2.10.exe --batch-interpreter python-fu-eval -b "import sys;sys.path=[\'.\']+sys.path;import test;test.run(image_path=\'{full_tmp_path}\', text=\'{text}\', font=\'{font}\', font_size=\'{font_size}\', text_x=\'{text_x}\', text_y=\'{text_y}\')"')




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditorApp()
    window.show()
    sys.exit(app.exec_())
