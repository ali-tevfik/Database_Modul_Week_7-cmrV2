from PyQt6 import QtWidgets, uic
import psycopg2
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Base.base_window import BaseWindow



class Mentor(BaseWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "mentor.ui")
        uic.loadUi(os.path.abspath(ui_path), self)

        # PostgreSQL bağlantı bilgileri
        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="crm_db",  
            user="postgres",          
            password="Ness07*"      
        )

        # Başlangıçta tabloyu doldur
        self.load_table_data()

        # Buton bağlantıları
        self.btn_search.clicked.connect(self.search_records)
        self.pushButton.clicked.connect(self.show_all_records)
        self.pushButton_3.clicked.connect(self.go_to_preferences)
        self.comboBox.currentIndexChanged.connect(self.filter_by_combobox)
        self.pushButton_2.clicked.connect(self.confirm_exit)
    
    def go_to_preferences(self):
        from page.preference import PreferenceWindow
        self.open_menu(PreferenceWindow)

    # ✅ Tüm mentor verilerini çeker
    def load_table_data(self):
        query = "SELECT * FROM mentors;"
        data = self.run_query(query)
        if not data:
            QtWidgets.QMessageBox.warning(self, "Uyarı", "Veritabanından veri alınamadı.")
            return

        self.df_all = data
        self.fill_table(data)

        # ComboBox doldur
        self.comboBox.clear()
        opinions = sorted({row["opinion"] for row in data if "opinion" in row and row["opinion"]})
        self.comboBox.addItems(opinions)

    # ✅ SQL sorgusu çalıştırır ve sonuçları list[dict] döner
    def run_query(self, query, params=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                return data
        except Exception as e:
            print("SQL Hatası:", e)
            return None

    # ✅ Tabloda göster
    def fill_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setHorizontalHeaderLabels(list(data[0].keys()))

        for row, row_data in enumerate(data):
            for col, key in enumerate(row_data):
                val = str(row_data[key]) if row_data[key] is not None else ""
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(val))
        self.tableWidget.resizeColumnsToContents()

    # ✅ "Show All" butonu
    def show_all_records(self):
        self.fill_table(self.df_all)

    # ✅ Arama (isimle)
    def search_records(self):
        search_text = self.lineEdit_search.text().strip().lower()
        query = """
            SELECT * FROM mentors
            WHERE LOWER(full_name) LIKE %s;
        """
        data = self.run_query(query, (f"%{search_text}%",))
        if data:
            self.fill_table(data)
        else:
            QtWidgets.QMessageBox.information(self, "Bilgi", "Eşleşen kayıt bulunamadı.")

    # ✅ ComboBox filtreleme (opinion sütununa göre)
    def filter_by_combobox(self):
        selected_value = self.comboBox.currentText()
        if not selected_value:
            self.fill_table(self.df_all)
            return
        query = "SELECT * FROM mentors WHERE opinion = %s;"
        data = self.run_query(query, (selected_value,))
        self.fill_table(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mentor()
    window.show()
    sys.exit(app.exec())
