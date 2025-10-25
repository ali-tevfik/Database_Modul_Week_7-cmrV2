import sys
import pandas as pd
from PyQt6 import QtWidgets, uic
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
from dotenv import load_dotenv
import os
from Base.base_window import BaseWindow
import requests
from PyQt6.QtWidgets import QTableWidgetItem


load_dotenv()




# -------------------- PyQt6 Uygulaması --------------------
class Applications(BaseWindow):
    BASEURL="http://127.0.0.1:8000/applications"

    def __init__(self):
        super().__init__()
        uic.loadUi(r".\ui\application.ui", self)
        self.resize(800, 600)
        
        # Aktif filtre başlığı
        self.current_filter_title = "Tüm Başvurular"
        self.send_request("")
        # ----------------- Buton Bağlantıları -----------------
        self.search_button.clicked.connect(self.search_records)
        self.all_application_button.clicked.connect(self.show_all_records)
        self.assigned_mentor_interviews_button.clicked.connect(self.show_mentor_assigned)
        self.unassigned_mentor_interviews_button.clicked.connect(self.show_mentor_unassigned)
        self.exit_button.clicked.connect(self.confirm_exit)
        self.preferences_button.clicked.connect(self.go_to_preferences)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)
        self.dublicate_application_button.clicked.connect(self.show_duplicate_records)
        self.fltered_applications_button.clicked.connect(self.show_filtered_applications)
        self.prev_vit_check_button.clicked.connect(self.show_previous_vit)
        self.differen_registration_button.clicked.connect(self.show_unique_vit_records)
        self.print_buttton.clicked.connect(lambda: self.print_table(self.current_filter_title))



    def send_request(self,url):
        allURL=self.BASEURL+url
        try:
            resp = requests.get(allURL, timeout=8)
            data = resp.json()
            self.load_table_data(data)
        except Exception as e:
            print(str(e)) 
               
    # ----------------- Tabloyu Yükleme -----------------
    def load_table_data(self, data):
        headers = list(data[0].keys())
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        self.alldata = data
        self.tableWidget.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, key in enumerate(headers):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item.get(key, ""))))

    # ----------------- Arama ve Filtreler -----------------
    def search_records(self):
        query = self.search_edit.text().strip()
        self.send_request("/searchName/"+ query)

    def show_all_records(self):
        self.send_request("/getAll")

    def show_mentor_assigned(self):
        self.send_request("/showmentor")

    def show_mentor_unassigned(self):
        self.send_request("/ushowmentor")

    def show_duplicate_records(self):
        self.send_request("/dublicate")

    def show_filtered_applications(self):
        self.send_request("/fltered")

    def show_previous_vit(self):
        self.send_request("/prevvitcheck")

    def show_unique_vit_records(self):
        self.send_request("/differenreg")

    # ----------------- Yazdırma -----------------
    def print_table(self, title=""):
        html = f"<h2>{title}</h2><table border='1' cellspacing='0' cellpadding='2'>"
        html += "<tr>"
        for col in range(self.tableWidget.columnCount()):
            html += f"<th>{self.tableWidget.horizontalHeaderItem(col).text()}</th>"
        html += "</tr>"

        for row in range(self.tableWidget.rowCount()):
            html += "<tr>"
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"
        html += "</table>"

        doc = QTextDocument()
        doc.setHtml(html)
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            doc.print(printer)

# ----------------- Uygulama Başlat -----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Applications()
    window.show()
    sys.exit(app.exec())