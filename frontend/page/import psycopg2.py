import psycopg2
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from Base.base_window import BaseWindow

class Application(BaseWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\application.ui", self)  # Application UI dosyanız

        # UI widget'larını al
        self.button = self.findChild(QtWidgets.QPushButton, "search_button")
        self.search_edit = self.findChild(QtWidgets.QLineEdit, "search_edit")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")

        # Örnek buton bağlantısı
        self.button.clicked.connect(self.search_basvuru)

        # PostgreSQL bağlantısı
        self.conn = psycopg2.connect(
            dbname="database",
            user="postgres",
            password="19Ekim88",
            host="localhost",
            port="5432"
        )

    def search_basvuru(self):
        search_text = self.search_edit.text().strip()
        if not search_text:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Arama metni boş olamaz!")
            return

        query = '''
        SELECT t.full_name, t.email, t.phone_number, a.*
        FROM applications a
        JOIN trainees t ON a.trainee_id = t.trainee_id
        WHERE t.full_name ILIKE %s
        '''
        df = pd.read_sql(query, self.conn, params=(f"{search_text}%",))

        self.table.clear()
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(str(df.iat[row, col])))

    # Diğer metodlar (show_all_applications, show_assigned_mentor_interviews vb.) aynı şekilde bırakılabilir

    def open_preferences(self):
        self.preferences_window = QtWidgets.QMainWindow()
        uic.loadUi("preferences.ui", self.preferences_window)
        self.preferences_window.show()
        self.close()

    def open_main_menu(self):
        self.main_menu_window = QtWidgets.QMainWindow()
        uic.loadUi("mainmenu.ui", self.main_menu_window)
        self.main_menu_window.show()
        self.close()
