from PyQt6 import  QtWidgets, uic
from page.application import Applications
from page.mentor import Mentor
from page.Interviews import Interviews
from utils.session import Session
from Base.base_window import BaseWindow
from page.etkinlik import CalendarApp
import os


class PreferenceWindow(BaseWindow):
    def __init__(self):
        super().__init__()

        # ✅ UI dosyasının tam yolu (frontend/ui/preferenceadmin.ui)
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "preferenceadmin.ui")
        uic.loadUi(os.path.abspath(ui_path), self)        
        session = Session()

        # Role bazlı admin buton görünürlüğü
        if session.role == "admin":
            self.admin_menu.show()
            self.label_2 = "CRM - Preference Admin Menu"
        else:
            self.admin_menu.hide()
            self.label_2 = "CRM - Preference Menu"
        
      

        # Butonların click olaylarını bağla
        self.applications.clicked.connect(self.btn_application)
        self.interviews.clicked.connect(self.btn_interviews)
        self.mentor_meet.clicked.connect(self.btn_mentor)
        self.exit.clicked.connect(self.btn_exit)
        self.main_menu.clicked.connect(self.btn_main)
        self.admin_menu.clicked.connect(self.btn_admin)

    # Buton metodları
    def btn_application(self):
        self.open_menu(Applications)

    def btn_interviews(self):
        self.open_menu(Interviews)

    def btn_mentor(self):
        self.open_menu(Mentor)

    def btn_exit(self):
        self.confirm_exit()

    def btn_main(self):
       self.open_menu(PreferenceWindow)

    def btn_admin(self):
        self.open_menu(CalendarApp)


# Test için çalıştırılabilir
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # role="admin" veya "user" deneyebilirsin
    window = PreferenceWindow(role="admin")
    window.show()
    sys.exit(app.exec())
