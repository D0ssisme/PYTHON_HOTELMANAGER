from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QHeaderView
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from database import DataBase

from PyQt5 import QtWidgets




class mainui(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('homepage.ui', self)  # Load trực tiếp file .ui

        # Gọi các hàm xử lý hoặc style sau khi load UI
        self.applyStylesheet()
        self.db = DataBase()
        self.db.connection = None
        self.db.connect()

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
        self.loaddata_tablecustomer()
        self.customer_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.customer_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.refresh_button.clicked.connect(self.search_tablecustomer)


        self.selectoption_combobox.addItems(["Tất Cả", "mã khách hàng"])
        self.deletecustomer_button.clicked.connect(self.open_deletecustomer)





    def search_tablecustomer(self):

        if  self.selectoption_combobox.currentText()=="Tất Cả":
            self.loaddata_tablecustomer()



    def loaddata_tablecustomer(self):

        customers = self.db.get_customers()

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

    def open_deletecustomer(self):

        selected_indexes = self.customer_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            first_cell_index = self.customer_table.model().index(selected_index.row(), 0)
            value = first_cell_index.data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn xóa !")
            return


        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa khách hàng  {value}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db.delete_customer(value):
                self.loaddata_tablecustomer()
                QMessageBox.information(self, "Thành công", "Đã xóa khách hàng thành công!")


            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa khách hàng")


    def open_addcustomer_dialog(self):
        try:
            from QLKH.addcustomer_dialog import addcustomer_dialog
            dialog = addcustomer_dialog()
            dialog.exec_()
            self.loaddata_tablecustomer()
        except Exception as e:
            print("Lỗi khi mở dialog thêm khách hàng:", e)




    def open_editcustomer_dialog(self):
        from QLKH.editcustomer_dialog import editcustomer_dialog
        selected_indexes = self.customer_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            makh = self.customer_table.model().index(selected_index.row(), 0)
            hoten = self.customer_table.model().index(selected_index.row(), 1)
            gioitinh = self.customer_table.model().index(selected_index.row(), 2)
            quoctich = self.customer_table.model().index(selected_index.row(), 3)
            cccd = self.customer_table.model().index(selected_index.row(), 4)
            sdt = self.customer_table.model().index(selected_index.row(), 5)
            diachi = self.customer_table.model().index(selected_index.row(), 6)
            maphong = self.customer_table.model().index(selected_index.row(), 7)
            ngaynhan = self.customer_table.model().index(selected_index.row(), 8)
            ngaytra = self.customer_table.model().index(selected_index.row(), 9)



            value = makh.data()
            value1=hoten.data()
            value2=gioitinh.data()
            value3=quoctich.data()
            value4=cccd.data()
            value5=sdt.data()
            value6=diachi.data()
            value7=maphong.data()
            value8=ngaynhan.data()
            value9=ngaytra.data()

            dialog = editcustomer_dialog(value,value1,value2,value3,value4,value5,value6,value7,value8,value9)
            dialog.exec_()
            self.loaddata_tablecustomer()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn xóa !")
            return








    def open_edituserdialog(self):
        from QLKH.dialog_edituser import dialog_edituser
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

        with open('QLKH/style.qss', 'r') as f:
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
