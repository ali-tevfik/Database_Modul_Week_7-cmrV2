import sys
from PyQt6 import QtWidgets, uic
import requests
from Base.base_window import BaseWindow

# 🧭 PyQt6 Arayüzü
class Mentor(BaseWindow):
    
    def __init__(self,):
        super().__init__()
        uic.loadUi(r".\ui\mentor.ui", self)  # senin UI dosyanın adı

        #tableWidget ismi senin UI'daki tabloyla aynı olmalı!
        self.load_table_data()

        self.btn_search.clicked.connect(self.search_records)
        self.pushButton.clicked.connect(self.show_all_records)   # Tüm görüşmeler butonu
        self.pushButton_3.clicked.connect(self.go_to_preferences)

         # ComboBox seçim değiştiğinde filtre uygula
        self.comboBox.currentIndexChanged.connect(self.filter_by_combobox)

        self.pushButton_2.clicked.connect(self.confirm_exit)  # Kapat butonu

    def send_request(self,url):
        
        try:
            data = None
            resp = requests.get(url, timeout=8)
            data = resp.json()
            self.update_table(data)
            if resp.status_code == 200:
                return data
            else:
                print("Data received from backend:", data)

        except Exception as e:
                print("Request failed:", e)
                return None


    def load_table_data(self):
        url = "http://127.0.0.1:8000/mentor"
        data =  self.send_request(url)
        print("data burda ",data)
        if not data:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Google Sheet'ten veri alınamadı.")
            return
        self.df_all = data
        # satır ve sütun sayısı
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))  # ilk elemandaki anahtar sayısı

        # Başlıklar
        self.tableWidget.setHorizontalHeaderLabels(list(data[0].keys()))

        # Tablonun doldurulması
        for row, row_data in enumerate(data):
            for col, key in enumerate(row_data):
                val = str(row_data[key]) if row_data[key] is not None else ""
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))

        self.tableWidget.resizeColumnsToContents()
        
        # ComboBox doldurma (6. sütun = index 5)
        self.comboBox.clear()
        #unique_values = sorted({row[list(row.keys())[5]] for row in data if row[list(row.keys())[5]] is not None})
        # 'full_name' sütunundaki benzersiz değerleri al
        unique_values = sorted({row["opinion"] for row in data if "opinion" in row and row["opinion"]})

        self.comboBox.addItems((unique_values))

    def show_all_records(self):
        self.update_table(self.df_all)
   
    def search_records(self):
        search_text = self.lineEdit_search.text().strip().lower()
        url = "http://127.0.0.1:8000/mentor/findName/" + search_text 
        
        self.send_request(url)
    

        
    def update_table(self,findData):
            # Tabloyu ilk baasta temizle ve yeni veriyi ekle
            #temizleme
            self.tableWidget.setRowCount(0)  # Tabloyu temizle
            #yeni veriyi ekleme
            self.tableWidget.setRowCount(len(findData))  # Yeni satır sayısını ayarla
            
            for row, row_data in enumerate(findData):
                for col, key in enumerate(row_data):
                    val = str(row_data[key]) if row_data[key] is not None else ""
                    self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))

            # Sütun genişliklerini içeriğe göre ayarla
            self.tableWidget.resizeColumnsToContents()

    def filter_by_combobox(self):
        selected_value = self.comboBox.currentText()
        if not selected_value:
            self.fill_table(self.df_all)
            return
        url = "http://127.0.0.1:8000/mentor/comboBoxValuesFilter/" + selected_value
        self.send_request(url)
       


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mentor()
    window.show()
    sys.exit(app.exec())


# class MyWindow(QtWidgets.QMainWindow):
#     def _init_(self):
#         super(MyWindow, self)._init_()
#         uic.loadUi(r".\ui\admin.ui", self)  # .ui dosyasını yükler
#         self.pushButton.clicked.connect(self.butonTiklandi)

#     def butonTiklandi(self):
#         print("Butona tıklandı!")

# app = QtWidgets.QApplication(sys.argv)
# window = MyWindow()
# window.show()
# sys.exit(app.exec())  # PyQt6 tarzı

