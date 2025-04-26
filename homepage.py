from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QHeaderView
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from QLKH.database import DataBase
from QLNV.database_staff import DataBaseStaff

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAbstractItemView



class mainui(QMainWindow):
    def __init__(self,username,password):
        super().__init__()

        uic.loadUi('homepage.ui', self)  # Load trực tiếp file .ui

        # Gọi các hàm xử lý hoặc style sau khi load UI
        self.applyStylesheet()
        self.db = DataBase()
        self.db_staff = DataBaseStaff()
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
        self.username=username
        self.password=password

        self.user_btn2.clicked.connect(lambda: self.open_edituserdialog(self.username, self.password))
        self.user_btn1.clicked.connect(lambda: self.open_edituserdialog(self.username,self.password))
        self.user_btn3.clicked.connect(lambda: self.open_edituserdialog(self.username,self.password))

        self.addcustomer_button.clicked.connect(self.open_addcustomer_dialog)
        self.editcustomer_button.clicked.connect(self.open_editcustomer_dialog)
        self.loaddata_tablecustomer()

        self.customer_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.customer_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.refresh_button.clicked.connect(self.search_tablecustomer)
        self.username_input.setText(username)
        self.checkcustomer_button.clicked.connect(self.open_detailcustomerdialog)
        self.selectoption_combobox.addItems(["Tất Cả", "mã khách hàng"])
        self.deletecustomer_button.clicked.connect(self.open_deletecustomer)
        self.customer_table.verticalHeader().setVisible(False)
        self.customer_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        ######################################
        # Nhân viên
        self.load_staff_data()
        self.addstaff_button.clicked.connect(self.open_addstaff_dialog)
        self.editstaff_button.clicked.connect(self.open_editstaff_dialog)
        self.deletestaff_button.clicked.connect(self.open_deletestaff)



    def open_detailcustomerdialog(self):
        from QLKH.detailcustomer_dialog import detailcustomer_dialog
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
            value1 = hoten.data()
            value2 = gioitinh.data()
            value3 = quoctich.data()
            value4 = cccd.data()
            value5 = sdt.data()
            value6 = diachi.data()
            value7 = maphong.data()
            value8 = ngaynhan.data()
            value9 = ngaytra.data()

            dialog = detailcustomer_dialog(value, value1, value2, value3, value4, value5, value6, value7, value8, value9)
            dialog.exec_()



    def search_tablecustomer(self):

        if  self.selectoption_combobox.currentText()=="Tất Cả":
            self.loaddata_tablecustomer()
        else :
            self.close_table()
            makh=self.loc_input.text()
            customers = self.db.find_customer(makh)
            for row in customers:
                row_items = [QStandardItem(str(cell)) for cell in row]
                self.model.appendRow(row_items)
            if(makh==""):
                self.close_table()



    def close_table(self):
        self.model.removeRows(0, self.model.rowCount())

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
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn sửa !")
            return

    def open_edituserdialog(self, username, password):
        try:

            from QLKH.dialog_edituser import dialog_edituser
            dlg = dialog_edituser(username, password)
            dlg.update_completed.connect(self.logout_fast)


            dlg.exec_()  # Mở dialog sửa user
        except Exception as e:
            print("Lỗi khi mở dialog sửa user:", e)




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

    def logout_fast(self):
        from login import loginui
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


 #########################################################################################
                                    #NHÂN VIÊN


    def load_staff_data(self):
        # 1. Kết nối và lấy dữ liệu
        staffs = self.db_staff.get_staff()

        # 2. Tạo model với số cột phù hợp
        self.staff_model = QStandardItemModel()
        self.staff_model.setHorizontalHeaderLabels([
            "Mã NV", "Họ Tên", "Chức Vụ", "SĐT", "Ca Làm"
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in staffs:
            row_items = [QStandardItem(str(cell)) for cell in row]
            self.staff_model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.staff_table.setModel(self.staff_model)
        self.staff_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.staff_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.staff_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.staff_table.verticalHeader().setVisible(False)

        # 5. Căn chỉnh cột cho đẹp
        header = self.staff_table.horizontalHeader()
        for column in range(self.staff_model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def open_addstaff_dialog(self):
        try:
            from QLNV.addstaff_dialog import addstaff_dialog  # Điều chỉnh theo đúng thư mục bạn lưu file .py
            dialog = addstaff_dialog()
            dialog.exec_()
            self.load_staff_data()  # Hàm này bạn cần có để load lại bảng nhân viên
        except Exception as e:
            print("Lỗi khi mở dialog thêm nhân viên:", e)

    def open_editstaff_dialog(self):
        from QLNV.editstaff_dialog import editstaff_dialog

        selected_rows = self.staff_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            model = self.staff_table.model()

            manv = model.index(row, 0).data()
            hoten = model.index(row, 1).data()
            chucvu = model.index(row, 2).data()
            sdt = model.index(row, 3).data()
            calam = model.index(row, 4).data()

            print(f"manv: {manv}, hoten: {hoten}, chucvu: {chucvu}, sdt: {sdt}, calam: {calam}")

            dialog = editstaff_dialog(manv, hoten, chucvu, calam, sdt)
            dialog.exec_()
            self.load_staff_data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn nhân viên muốn chỉnh sửa!")

    def open_deletestaff(self):
        selected_indexes = self.staff_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            first_cell_index = self.staff_table.model().index(selected_index.row(), 0)
            manv = first_cell_index.data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn nhân viên muốn xóa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa nhân viên {manv}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db_staff.delete_staff(manv):
                self.load_staff_data()
                QMessageBox.information(self, "Thành công", "Đã xóa nhân viên thành công!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa nhân viên.")

if __name__ == '__main__':
    app = QApplication([])
    user="123"
    password="29052005"
    window = mainui(user,password)
    window.show()
    app.exec_()
