from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtCore import QDateTime
import pycountry
import os
from QLKH.database import DataBase
class detailcustomer_dialog(QtWidgets.QDialog):
    def __init__(self,makh,hoten,gioitinh,quoctich,cccd,sdt,diachi,maphong,ngaynhan,ngaytra):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "detailcustomer_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("THÊM KHÁCH HÀNG")
        self.makh_value.setText(makh)  # Đặt giá trị mới cho QLineEdits
        self.makh_value.setReadOnly(True)
        self.hoten_value.setText(hoten)
        self.gioitinh_value.addItems(["Nam", "Nữ"])
        self.gioitinh_value.setCurrentText(gioitinh)
        self.country_value.setEditable(True)
        self.country_value.addItem("")
        countries = [country.name for country in pycountry.countries]
        self.country_value.addItems(countries)
        self.country_value.setCurrentText(quoctich)
        self.cccd_value.setText(cccd)
        self.sdt_value.setText(sdt)
        self.diachi_value.setText(diachi)
        self.maphong_value.setText(maphong)
        ngaynhan_datetime = QDateTime.fromString(ngaynhan, "yyyy-MM-dd HH:mm:ss")
        ngaytra_datetime=QDateTime.fromString(ngaytra,"yyyy-MM-dd HH:mm:ss")
        self.ngaynhan_value.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaynhan_value.setCalendarPopup(True)
        self.ngaynhan_value.setDateTime(ngaynhan_datetime)
        self.ngaytra_value.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaytra_value.setCalendarPopup(True)
        self.ngaytra_value.setDateTime(ngaytra_datetime)
        self.cancel_button.clicked.connect(self.close)
        self.makh_value.setReadOnly(True)
        self.cccd_value.setReadOnly(True)
        self.country_value.setEnabled(False)
        self.diachi_value.setReadOnly(True)
        self.gioitinh_value.setEnabled(False)

        self.hoten_value.setReadOnly(True)
        self.maphong_value.setReadOnly(True)
        self.ngaynhan_value.setReadOnly(True)
        self.ngaytra_value.setReadOnly(True)
        self.sdt_value.setReadOnly(True)


        self.db = DataBase()
        self.db.connection = None
        self.db.connect()





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = detailcustomer_dialog(
        "KH001",              # Mã khách hàng
        "Nguyễn Văn A",       # Họ tên
        "Nam",                # Giới tính
        "Vietnam",            # Quốc tịch
        "123456789",          # CCCD
        "0901234567",         # Số điện thoại
        "123 Đường ABC",      # Địa chỉ
        "101",                # Mã phòng
        "2025-04-05 12:00:00",# Ngày nhận
        "2025-04-10 12:00:00" # Ngày trả
    )
    dialog.exec_()
