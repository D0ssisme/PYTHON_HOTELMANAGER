from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate

from QLNV.database_staff import DataBaseStaff

import os

class addstaff_dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "addstaff_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("THÊM NHÂN VIÊN")

        # Kết nối các nút
        self.addnv_agreebutton.clicked.connect(self.check_addstaff)
        self.cancelnv_button.clicked.connect(self.close)

        # Thiết lập dữ liệu cho ComboBox
        self.role_combobox.addItems(["Lễ tân", "Quản lý", "Bảo vệ", "Tạp vụ"])  # thêm nếu cần
        self.shift_combobox.addItems(["Ca sáng", "Ca chiều", "Ca tối","Hành chính"])

        # Kết nối database
        self.db = DataBaseStaff()
        self.db.connection = None
        self.db.connect()

    def check_addstaff(self):
        manv = self.manv_input.text()
        hoten = self.namenv_input.text()
        chucvu = self.role_combobox.currentText()
        calam = self.shift_combobox.currentText()
        sdt = self.sdtnv_input.text()

        if not hoten or not sdt:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")
            return

        # Nếu để trống mã NV, sẽ tự động tạo
        if not manv:
            manv = "NV" + str(self.db.get_next_staff_id())  # Bạn cần tạo hàm này trong database_customer.py

        staff_data = (manv, hoten, chucvu, sdt, calam)
        success = self.db.add_staff(staff_data)

        if success:
            QMessageBox.information(self, "Thành công", "Đã thêm nhân viên thành công!")
            self.accept()
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể thêm nhân viên.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = addstaff_dialog()
    dialog.exec_()
