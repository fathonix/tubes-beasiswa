import sys
import json
import os
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# -------TAMPILAN LOGIN-------
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("App. Beasiswa")
        self.setGeometry(200, 100, 800, 600)
 
        self.load_accounts()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Selamat Datang, Silakan Login Terlebih Dahulu")
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 30px;")
        self.layout.addWidget(self.label_title, alignment=Qt.AlignCenter)

        self.label_username = QLabel("Username:")
        self.label_username.setStyleSheet("font-size: 18px;")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("font-size: 16px; padding: 10px;")

        self.label_password = QLabel("Password:")
        self.label_password.setStyleSheet("font-size: 18px;")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("font-size: 16px; padding: 10px;")

        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.input_username)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)

        self.button_login = QPushButton("Login")
        self.button_login.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.button_register = QPushButton("Daftar Akun")
        self.button_register.setStyleSheet("font-size: 18px; padding: 10px; background-color: #2196F3; color: white;")

        self.layout.addWidget(self.button_login)
        self.layout.addWidget(self.button_register)

        self.button_login.clicked.connect(self.handle_login)
        self.button_register.clicked.connect(self.open_register_window)

    def load_accounts(self):
        file_path = "accounts.json"
        if not os.path.exists(file_path):
            self.accounts = []
        with open(file_path, "r") as file:
            try:
                self.accounts = json.load(file)
            except json.JSONDecodeError:
                self.accounts = []

    def handle_login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Login Gagal", "Username dan password tidak boleh kosong.")
            return
        
        self.logged_in = False
        self.user_role = ""
        for account in self.accounts:
            if account["username"] == username and account["password"] == password:
                self.account = account
                break

        if self.account["role"] == "admin":
            self.open_admin_window()
        elif self.account:
            self.open_scholarship_window()
        else:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah.")

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.exec()
        self.load_accounts()

    def open_scholarship_window(self):
        self.scholarship_window = ScholarshipWindow(self.account)
        self.scholarship_window.show()
        self.close()

    def open_admin_window(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()
        self.close()

# -------DAFTAR AKUN-------
class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daftar Akun")
        self.setGeometry(200, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Daftar Akun Baru")
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 30px;")
        self.layout.addWidget(self.label_title, alignment=Qt.AlignCenter)

        self.label_username = QLabel("Username:")
        self.label_username.setStyleSheet("font-size: 18px;")
        self.input_username = QLineEdit()
        self.input_username.setStyleSheet("font-size: 16px; padding: 10px;")

        self.label_password = QLabel("Password:")
        self.label_password.setStyleSheet("font-size: 18px;")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.input_password.setStyleSheet("font-size: 16px; padding: 10px;")

        self.label_confirm_password = QLabel("Konfirmasi Password:")
        self.label_confirm_password.setStyleSheet("font-size: 18px;")
        self.input_confirm_password = QLineEdit()
        self.input_confirm_password.setEchoMode(QLineEdit.Password)
        self.input_confirm_password.setStyleSheet("font-size: 16px; padding: 10px;")

        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.input_username)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)
        self.layout.addWidget(self.label_confirm_password)
        self.layout.addWidget(self.input_confirm_password)

        self.button_register = QPushButton("Daftar")
        self.button_register.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.layout.addWidget(self.button_register)

        self.button_register.clicked.connect(self.handle_register)
        self.setLayout(self.layout)

    def handle_register(self):
        try:
            with open("accounts.json", "r") as file:
                self.accounts = json.load(file)
        except:
            self.accounts = []

        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        confirm_password = self.input_confirm_password.text().strip()
        
        if not (username and password and confirm_password):
            QMessageBox.warning(self, "Pendaftaran Gagal", "Semua kolom harus diisi.")
            return

        if username in map(lambda x: x["username"], self.accounts):
            QMessageBox.warning(self, "Pendaftaran Gagal", "Username sudah terdaftar.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Pendaftaran Gagal", "Password tidak cocok.")
            return

        self.accounts.append({
            "username": username,
            "password": password,
            "role": "user",
            "saved_items": []
        })

        with open("accounts.json", "w") as file:
            try:
                json.dump(self.accounts, file, indent=4)
            except IOError:
                QMessageBox.warning(self, "Pendaftaran Gagal", "Gagal menyimpan akun.")
                return

        QMessageBox.information(self, "Pendaftaran Berhasil", f"Akun {username} berhasil didaftarkan.")
        self.close()

# -------DESKRIPSI BEASISWA-------
class ScholarshipDetailWindow(QMainWindow): 
    def __init__(self, scholarship, account):
        super().__init__()
        self.scholarship = scholarship
        self.account = account
        self.setWindowTitle(scholarship["name"])
        self.setGeometry(200, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label_title = QLabel(scholarship["name"])
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50; margin-bottom: 20px;")
        self.layout.addWidget(self.label_title)

        description_with_line_breaks = scholarship["long_description"].replace("\n", "<br>")

        label_description = QLabel(description_with_line_breaks)
        label_description.setStyleSheet("font-size: 16px; color: #555; line-height: 1.5; padding-top: 20px;")
        label_description.setTextFormat(Qt.RichText)  
        label_description.setWordWrap(True)
        label_description.setOpenExternalLinks(True) 
        self.layout.addWidget(label_description)
        
        self.button_layout = QHBoxLayout()

        button_save = QPushButton()
        if scholarship["id"] in self.account["saved_items"]:
            button_save.setText("Hapus dari Disimpan")
            button_save.setStyleSheet("background-color: red; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        else:
            button_save.setText("Simpan")
            button_save.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        button_save.clicked.connect(self.save_scholarship)
        self.button_layout.addWidget(button_save)

        button_link = QPushButton("Masuk ke Situs Beasiswa")
        button_link.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        button_link.clicked.connect(self.open_webbrowser)
        self.button_layout.addWidget(button_link)

        button_back = QPushButton("Kembali")
        button_back.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        button_back.clicked.connect(self.close)
        self.button_layout.addWidget(button_back)

        self.layout.addLayout(self.button_layout)
    
    def open_webbrowser(self):
        webbrowser.open(self.scholarship["link"])
    
    def save_scholarship(self):
        is_delete = False
        if self.scholarship["id"] in self.account["saved_items"]:
            self.account["saved_items"].remove(self.scholarship["id"])
            is_delete = True
        else:
            self.account["saved_items"].append(self.scholarship["id"])

        with open("accounts.json", "r") as file:
            accounts = json.load(file)

        found = False
        for index, data in enumerate(accounts):
            if data["username"] == self.account["username"]:
                found = True
                accounts[index] = self.account
                break
        
        if not found:
            QMessageBox.warning(self, "Galat", "Gagal menyimpan perubahan.")
            return

        with open("accounts.json", "w") as file:
            json.dump(accounts, file, indent=4)

        if is_delete:
            QMessageBox.information(self, "Sukses", "Beasiswa berhasil dihapus.")
        else:
            QMessageBox.information(self, "Sukses", "Beasiswa berhasil disimpan.")

# -------DAFTAR BEASISWA-------
class ScholarshipWindow(QMainWindow):
    
    def load_scholarships(self):
        with open("scholarships.json", "r") as file:
            self.scholarships = json.load(file)
    
    def __init__(self, account):
        super().__init__()
        self.account = account
        self.setWindowTitle("Daftar Beasiswa")
        self.setGeometry(200, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        
        self.top_layout = QHBoxLayout()

        self.label_title = QLabel("Daftar Beasiswa")
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.top_layout.addWidget(self.label_title)
        
        self.saved_button = QPushButton("Daftar Tersimpan")
        self.saved_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.saved_button.clicked.connect(self.open_saved)
        self.top_layout.addWidget(self.saved_button)
        
        self.logout_button = QPushButton("Keluar")
        self.logout_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: red; color: white;")
        self.logout_button.clicked.connect(self.logout)
        self.top_layout.addWidget(self.logout_button)

        self.layout.addLayout(self.top_layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari Beasiswa...")
        self.search_bar.setStyleSheet("font-size: 16px; padding: 10px;")
        self.layout.addWidget(self.search_bar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)

        try:
            self.load_scholarships()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Galat", "Gagal memuat data beasiswa")

        self.filtered_scholarships = self.scholarships

        self.update_scholarships_display()

        self.layout.addWidget(self.scroll_area)
        self.search_bar.textChanged.connect(self.update_search_results)

    def update_search_results(self):
        search_query = self.search_bar.text().lower()
        self.filtered_scholarships = [scholarship for scholarship in self.scholarships if search_query in scholarship["name"].lower()]
        self.update_scholarships_display()

    def update_scholarships_display(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, scholarship in enumerate(self.filtered_scholarships):
            self.add_scholarship_choice(scholarship, i)

    def add_scholarship_choice(self, scholarship, i):
        card = QWidget()
        card.setStyleSheet("""
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 20px;
        """)
        card_layout = QVBoxLayout(card)

        label_name = QLabel(scholarship["name"])
        label_name.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(label_name)

        label_description = QLabel(scholarship["short_description"])
        label_description.setStyleSheet("font-size: 14px; color: #555;")
        label_description.setWordWrap(True)
        card_layout.addWidget(label_description)

        button = QPushButton("Selengkapnya...")
        button.setStyleSheet("font-size: 17px; padding: 5px;")
        button.clicked.connect(lambda: self.open_scholarship_detail(scholarship, self.account))
        card_layout.addWidget(button)

        self.scroll_layout.addWidget(card)

    def open_scholarship_detail(self, scholarship, account):
        self.detail_window = ScholarshipDetailWindow(scholarship, account)
        self.detail_window.show()

    def open_saved(self):
        self.saved_window = SavedWindow(self.account)
        self.saved_window.show()
    
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# -------DAFTAR BEASISWA TERSIMPAN-------
class SavedWindow(QMainWindow):
    
    def load_scholarships(self):
        with open("scholarships.json", "r") as file:
            data = json.load(file)
            self.scholarships = list(filter(lambda x: x["id"] in self.account["saved_items"], data))
    
    def __init__(self, account):
        super().__init__()
        self.account = account
        self.setWindowTitle("Daftar Beasiswa Tersimpan")
        self.setGeometry(200, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)
        
        self.top_layout = QHBoxLayout()

        self.label_title = QLabel("Daftar Tersimpan")
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.top_layout.addWidget(self.label_title)
        
        self.saved_button = QPushButton("Kembali")
        self.saved_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #2196F3; color: white;")
        self.saved_button.clicked.connect(self.close)
        self.top_layout.addWidget(self.saved_button)
        self.layout.addLayout(self.top_layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari Beasiswa...")
        self.search_bar.setStyleSheet("font-size: 16px; padding: 10px;")
        self.layout.addWidget(self.search_bar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)

        try:
            self.load_scholarships()
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Galat", "Gagal memuat data beasiswa")

        self.filtered_scholarships = self.scholarships

        self.update_scholarships_display()

        self.layout.addWidget(self.scroll_area)
        self.search_bar.textChanged.connect(self.update_search_results)

    def update_search_results(self):
        search_query = self.search_bar.text().lower()
        self.filtered_scholarships = [scholarship for scholarship in self.scholarships if search_query in scholarship["name"].lower()]
        self.update_scholarships_display()

    def update_scholarships_display(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, scholarship in enumerate(self.filtered_scholarships):
            self.add_scholarship_choice(scholarship, i)

    def add_scholarship_choice(self, scholarship, i):
        card = QWidget()
        card.setStyleSheet("""
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 20px;
        """)
        card_layout = QVBoxLayout(card)

        label_name = QLabel(scholarship["name"])
        label_name.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(label_name)

        label_description = QLabel(scholarship["short_description"])
        label_description.setStyleSheet("font-size: 14px; color: #555;")
        label_description.setWordWrap(True)
        card_layout.addWidget(label_description)

        button = QPushButton("Selengkapnya...")
        button.setStyleSheet("font-size: 17px; padding: 5px;")
        button.clicked.connect(lambda: self.open_scholarship_detail())
        card_layout.addWidget(button)

        self.scroll_layout.addWidget(card)

    def open_scholarship_detail(self, scholarship):
        self.detail_window = ScholarshipDetailWindow(scholarship)
        self.detail_window.show()

# -------DESKRIPSI BEASISWA-------
class AdminDetailWindow(QMainWindow): 
    def __init__(self, scholarship):
        super().__init__()
        self.setWindowTitle("Ubah Data " + scholarship["name"])
        self.setGeometry(200, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label_title = QLabel(scholarship["name"])
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2C3E50; margin-bottom: 20px;")
        self.layout.addWidget(self.label_title)

        description_with_line_breaks = scholarship["long_description"].replace("\n", "<br>")

        label_description = QLabel(description_with_line_breaks)
        label_description.setStyleSheet("font-size: 16px; color: #555; line-height: 1.5; padding-top: 20px;")
        label_description.setTextFormat(Qt.RichText)  
        label_description.setWordWrap(True)
        label_description.setOpenExternalLinks(True) 
        self.layout.addWidget(label_description)

        button_back = QPushButton("Kembali")
        button_back.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        button_back.clicked.connect(self.close)
        self.layout.addWidget(button_back, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

# -------DAFTAR BEASISWA-------
class AdminWindow(QMainWindow):
    
    def load_scholarships(self):
        with open("scholarships.json", "r") as file:
            return json.load(file)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Admin")
        self.setGeometry(200, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Manajemen Beasiswa")
        self.label_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.label_title)
        
        self.top_layout = QHBoxLayout()

        self.button_add = QPushButton("Tambah Beasiswa")
        self.button_add.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.button_add.clicked.connect(self.open_add_scholarship_form)
        self.top_layout.addWidget(self.button_add)
        
        self.logout_button = QPushButton("Keluar")
        self.logout_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: red; color: white;")
        self.logout_button.clicked.connect(self.logout)
        self.top_layout.addWidget(self.logout_button)
        
        self.layout.addLayout(self.top_layout)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Cari Beasiswa...")
        self.search_bar.setStyleSheet("font-size: 16px; padding: 10px;")
        self.layout.addWidget(self.search_bar)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)

        try:
            self.scholarships = self.load_scholarships()
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Galat", "Gagal memuat data beasiswa")

        self.filtered_scholarships = self.scholarships  
        self.update_scholarships_display()

        self.layout.addWidget(self.scroll_area)
        self.search_bar.textChanged.connect(self.update_search_results)

    def update_search_results(self):
        search_query = self.search_bar.text().lower()
        self.filtered_scholarships = [scholarship for scholarship in self.scholarships if search_query in scholarship["name"].lower()]
        self.update_scholarships_display()

    def update_scholarships_display(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i, scholarship in enumerate(self.filtered_scholarships):
            self.add_scholarship_choice(scholarship, i)

    def add_scholarship_choice(self, scholarship, i):
        card = QWidget()
        card.setStyleSheet("""
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            padding: 20px;
        """)
        card_layout = QVBoxLayout(card)

        label_name = QLabel(scholarship["name"])
        label_name.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(label_name)

        label_description = QLabel(scholarship["short_description"])
        label_description.setStyleSheet("font-size: 14px; color: #555;")
        label_description.setWordWrap(True)
        card_layout.addWidget(label_description)

        button = QPushButton("Ubah Data")
        button.setStyleSheet("font-size: 17px; padding: 5px;")
        button.clicked.connect(lambda: self.open_add_scholarship_form(scholarship))
        card_layout.addWidget(button)

        self.scroll_layout.addWidget(card)

    def open_add_scholarship_form(self, data):
        self.add_form = AddScholarshipForm(data)
        self.add_form.exec()
        self.load_scholarships()
        self.update_scholarships_display()
    
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

# -------FORM TAMBAH BEASISWA-------
class AddScholarshipForm(QDialog):
    def __init__(self, data):
        super().__init__()

        self.setGeometry(300, 150, 400, 500)
        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nama Beasiswa")
        
        layout.addWidget(QLabel("Nama Beasiswa:"))
        layout.addWidget(self.name_input)

        self.short_description_input = QLineEdit()
        self.short_description_input.setPlaceholderText("Deskripsi Singkat")
        layout.addWidget(QLabel("Deskripsi Singkat:"))
        layout.addWidget(self.short_description_input)

        self.long_description_input = QTextEdit()
        layout.addWidget(QLabel("Deskripsi Lengkap:"))
        layout.addWidget(self.long_description_input)

        self.link_input = QTextEdit()
        layout.addWidget(QLabel("Tautan URL beasiswa:"))
        layout.addWidget(self.link_input)

        self.save_button = QPushButton("Simpan")
        self.save_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white;")
        self.save_button.clicked.connect(self.save_scholarship)
        layout.addWidget(self.save_button)
        
        if data:
            self.new_scholarship = data
            self.setWindowTitle("Ubah Beasiswa " + data["name"])
            self.name_input.setText(data["name"])
            self.short_description_input.setText(data["short_description"])
            self.long_description_input.setText(data["long_description"])
            self.link_input.setText(data["link"])
        else:
            self.new_scholarship = {
                "id": None,
                "name": None,
                "short_description": None,
                "long_description": None,
                "link": None,
            }
            self.setWindowTitle("Tambah Beasiswa Baru")

        self.setLayout(layout)

    def save_scholarship(self):
        name = self.name_input.text()
        short_description = self.short_description_input.text()
        long_description = self.long_description_input.toPlainText()
        link = self.link_input.toPlainText()

        if not all([name, short_description, long_description]):
            QMessageBox.warning(self, "Input Tidak Lengkap", "Harap isi semua kolom.")
            return

        try:
            with open("scholarships.json", "r") as file:
                scholarships = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Galat", "Gagal memuat berkas untuk disimpan.")
            return
        self.new_scholarship["name"] = name
        self.new_scholarship["short_description"] = short_description
        self.new_scholarship["long_description"] = long_description
        self.new_scholarship["link"] = link

        if self.new_scholarship["id"] == None:
            self.new_scholarship["id"] = len(scholarships)
            scholarships.append(self.new_scholarship)
        else:
            found = False
            for index, data in enumerate(scholarships):
                if data["id"] == self.new_scholarship["id"]:
                    found = True
                    scholarships[index] = self.new_scholarship
                    break
            
            if not found:
                QMessageBox.warning(self, "Galat", "Gagal menyimpan perubahan.")
                return

        try:
            with open("scholarships.json", "w") as file:
                json.dump(scholarships, file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Galat", "Gagal menyimpan berkas.")
            return

        QMessageBox.information(self, "Sukses", "Beasiswa berhasil ditambahkan.")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())