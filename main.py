from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import  QMessageBox
from pyodbc import connect
from login import loginui

from PyQt5 import QtWidgets




class mainui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Trangchu.ui', self)  # Load trực tiếp file .ui

        # Gọi các hàm xử lý hoặc style sau khi load UI
        self.applyStylesheet()

        self.main_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.main))
        self.room_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.room))
        self.report_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.report))
        self.staff_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.staff))
        self.customer_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.customer))
        self.bill_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.bill))
        self.main_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.main))
        self.room_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.room))
        self.report_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.report))
        self.staff_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.staff))
        self.customer_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.customer))
        self.bill_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.bill))
        self.logout_btn2.clicked.connect(self.logout)
        self.logout_btn.clicked.connect(self.logout)

    def logout(self):
        from login import loginui
        reply = QMessageBox.question(
            self, "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Thông báo")
            msg_box.setText("Bạn đã đăng xuất thành công.")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()

            # Ẩn cửa sổ chính và có thể hiện lại Login ở đây
            self.hide()

            self.login_window = QtWidgets.QMainWindow()
            self.login_ui = loginui()
            self.login_ui.setupUi(self.login_window)
            self.login_window.show()

    def applyStylesheet(self):

        with open('style.qss', 'r') as f:
            self.setStyleSheet(f.read())

            self.change_btn.click()

            self.widget_2.setStyleSheet("""
            background-color: #E0E0E0;
            """)
            self.widget.setStyleSheet("""
            background-color: #E0E0E0;
            """)

            self.change_btn.setStyleSheet("""
                                  QPushButton {
                                      background-color: white;
                                      border: none;
                                      text-align: left;
                                      padding: 10px;
                                       border-radius:10px;
                                  }
                                  QPushButton:hover {
                                      background-color: #E0E0E0; /* xanh nhạt */
                                  }
                              """)
            self.logout_btn.setStyleSheet("""
                                      QPushButton {
                                  background-color: #E0E0E0;
                                  border: none;
                                  padding:px;
                                  border-radius:10px;
                              }

                              QPushButton:hover {
                                  background-color: 		#aad4f2;
                                      border-radius:10px;
                              }

                              QPushButton:focus {
                                  outline: none;
                                  border: none;
                                  background-color: 	#aad4f2;
                                      border-radius:10px;
                              }
                              QPushButton:checked {
                              background-color: #aad4f2;
                              }
                                """)
            self.logout_btn2.setStyleSheet("""
                                              QPushButton {
                                          background-color: #E0E0E0;
                                          border: none;
                                          padding:px;
                                          border-radius:10px;
                                      }

                                      QPushButton:hover {
                                          background-color: 		#aad4f2;
                                              border-radius:10px;
                                      }

                                      QPushButton:focus {
                                          outline: none;
                                          border: none;
                                          background-color: 	#aad4f2;
                                              border-radius:10px;
                                      }
                                      QPushButton:checked {
                                      background-color: #aad4f2;
                                      }
                                        """)

            self.user_btn3.setStyleSheet(""" 

                                """)

            style = """
                              QPushButton {
                                  background-color: #E0E0E0;
                                  border: none;
                                  padding:px;
                                  border-radius:10px;
                              }

                              QPushButton:hover {
                                  background-color: 		#D5D5D5;
                                      border-radius:10px;
                              }

                              QPushButton:focus {
                                  outline: none;
                                  border: none;
                                  background-color: 	#D5D5D5;
                                      border-radius:10px;
                              }
                              QPushButton:checked {
                              background-color: #D5D5D5;
                              }

                              """

            # Cặp nút: [(nút to, nút nhỏ), ...]
            self.menu_pairs = [
                (self.main_btn, self.main_btn2),
                (self.room_btn, self.room_btn2),
                (self.customer_btn, self.customer_btn2),
                (self.staff_btn, self.staff_btn2),
                (self.report_btn, self.report_btn2),
                (self.bill_btn, self.bill_btn2)
            ]

            # Gán style và setCheckable
            for btn1, btn2 in self.menu_pairs:
                btn1.setCheckable(True)
                btn2.setCheckable(True)
                btn1.setStyleSheet(style)
                btn2.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication([])
    window = mainui()
    window.show()
    app.exec_()
