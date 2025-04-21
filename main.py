from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QHeaderView
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from database import DataBase
import pyodbc


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
        self.user_btn2.clicked.connect(self.open_edituserdialog)
        self.user_btn1.clicked.connect(self.open_edituserdialog)
        self.user_btn3.clicked.connect(self.open_edituserdialog)
        self.addcustomer_button.clicked.connect(self.open_addcustomer_dialog)
        self.editcustomer_button.clicked.connect(self.open_editcustomer_dialog)

        # 1. Kết nối và lấy dữ liệu
        db = DataBase()
        customers = db.get_customers()


        # 2. Tạo model với số cột phù hợp
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Mã Khách Hàng", "Họ Tên", "Giới Tính", "Quốc Tịch",
            "CCCD", "SĐT", "Địa Chỉ", "Mã Phòng", "Ngày Nhận", "Ngày Trả"
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in customers:
            row_items = [QStandardItem(str(cell)) for cell in row]
            self.model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.customer_table.setModel(self.model)

        # 5. Căn chỉnh cột cho đẹp
        header = self.customer_table.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def open_addcustomer_dialog(self):
        from addcustomer_dialog import addcustomer_dialog
        dialog=addcustomer_dialog()
        dialog.exec_()
    def open_editcustomer_dialog(self):
        from editcustomer_dialog import editcustomer_dialog
        dialog=editcustomer_dialog()
        dialog.exec_()
    def open_edituserdialog(self):
        from dialog_edituser import dialog_edituser
        dlg = dialog_edituser()
        dlg.exec_()  # Ho



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
