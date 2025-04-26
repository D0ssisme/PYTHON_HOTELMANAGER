
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QMessageBox

import pyodbc

class DataBase:
    def __init__(self):
        self.connection = None
        self.connect()



    def connect(self):
        try:
            server = r"DESKTOP-3FTCGLC\SQLSERVER2022"
            database = "hotel"
            username = "manhdung"
            password = "29052005"

            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            print("Kết nối SQL Server thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi kết nối SQL: {e}")
            raise


    def checklogin(self, username, password):

            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT [mat khau] FROM login WHERE [tai khoan] = ?",
                (username,)
            )
            result = cursor.fetchone()


            if result and result[0] == password:
                return True
            return False

    def close(self):
        if self.connection:
            self.connection.close()


class loginui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 458)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(460, 300, 291, 41))
        self.login_button.setStyleSheet("QPushButton {\n"
"    border-radius: 15px;  /* Độ tròn của góc - có thể điều chỉnh */\n"
"    background-color: #2980b9;  /* Màu nền */\n"
"    color: white;  /* Màu chữ */\n"
"    padding: 3px;  /* Khoảng cách giữa viền và nội dung */\n"
"    border: 2px solid #4CAF50;  /* Viền button */\n"
"}\n"
"\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2c82c9;  /* Màu khi nhấn */\n"
"}")
        self.login_button.setObjectName("login_button")
        self.login_label = QtWidgets.QLabel(self.centralwidget)
        self.login_label.setGeometry(QtCore.QRect(460, 100, 47, 13))
        self.login_label.setObjectName("login_label")
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(460, 190, 47, 13))
        self.password_label.setObjectName("password_label")
        self.login_input = QtWidgets.QLineEdit(self.centralwidget)
        self.login_input.setGeometry(QtCore.QRect(460, 120, 291, 31))
        self.login_input.setObjectName("login_input")
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(QtCore.QRect(460, 210, 291, 31))
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setObjectName("password_input")
        self.tittlelogin_label = QtWidgets.QLabel(self.centralwidget)
        self.tittlelogin_label.setGeometry(QtCore.QRect(460, 40, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tittlelogin_label.setFont(font)
        self.tittlelogin_label.setTextFormat(QtCore.Qt.AutoText)
        self.tittlelogin_label.setObjectName("tittlelogin_label")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(-10, 40, 441, 361))
        self.image_label.setText("")
        self.image_label.setPixmap(QtGui.QPixmap("image/hotel-icon.png"))
        self.image_label.setObjectName("image_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




    def handle_login(self, MainWindow):
        from homepage import mainui
        username = self.login_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(MainWindow, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Thêm đoạn kiểm tra đăng nhập nếu muốn
        db = DataBase()
        if db.checklogin(username, password):
            QMessageBox.information(MainWindow, "Thành công", "Đăng nhập thành công!")
            MainWindow.hide()
            self.main_ui = mainui()  # Tạo cửa sổ giao diện chính
            self.main_ui.show()

        else:
            QMessageBox.critical(MainWindow, "Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("ĐĂNG NHÂP  ")
        self.login_button.setText(_translate("MainWindow", "Đăng Nhập"))
        self.login_label.setText(_translate("MainWindow", "Tải Khoản "))
        self.password_label.setText(_translate("MainWindow", "Mật Khẩu"))
        self.tittlelogin_label.setText(_translate("MainWindow", "ĐĂNG NHẬP QUẢN LÍ KHÁCH SẠN "))
        self.login_button.clicked.connect(lambda: self.handle_login(MainWindow))

class MainUIApp(QtWidgets.QMainWindow):
    def __init__(self):
        from homepage import mainui
        super().__init__()
        self.ui = mainui()
        self.ui.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = loginui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
