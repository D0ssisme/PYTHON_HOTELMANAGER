from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import QDateTime
import pycountry
from QLKH.database import DataBase
class editcustomer_dialog(QtWidgets.QDialog):
    def __init__(self,makh,hoten,gioitinh,quoctich,cccd,sdt,diachi,maphong,ngaynhan,ngaytra):
        super().__init__()
        uic.loadUi("editcustomer_dialog.ui", self)  # Load file .ui
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
        self.agree_button.clicked.connect(self.check_editcustomer)
        self.db = DataBase()
        self.db.connection = None
        self.db.connect()




    def check_editcustomer(self):
        makh = self.makh_value.text()
        hovaten = self.hoten_value.text()
        gioitinh = self.gioitinh_value.currentText()  # Lấy giá trị đã chọn
        quoctich = self.country_value.currentText()
        cccd = self.cccd_value.text()
        sdt = self.sdt_value.text()
        diachi = self.diachi_value.text()
        maphong = self.maphong_value.text()
        ngaynhan = self.ngaynhan_value.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        ngaytra = self.ngaytra_value.dateTime().toString("yyyy-MM-dd HH:mm:ss")

        customer_data = (makh, hovaten, gioitinh, quoctich, cccd, sdt, diachi, maphong, ngaynhan, ngaytra)
        if not hovaten or not cccd or not sdt:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ Họ tên, CCCD và Số điện thoại!")
            return


        if self.db.update_customer(customer_data):
            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin khách hàng!")
            self.accept();
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể cập nhật thông tin khách hàng")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = editcustomer_dialog(
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
