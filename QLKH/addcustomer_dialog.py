from PyQt5 import QtWidgets, uic
import sys
import pycountry
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import  QMessageBox
from QLKH.database import DataBase
import os
class addcustomer_dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "addcustomer_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("THÊM KHÁCH HÀNG")
        self.gender_combobox.addItems(["Nam", "Nữ"])
        self.country_combobox.setEditable(True)
        self.country_combobox.addItem("")  # Thêm dòng trống ở đầu
        # Thêm danh sách các quốc gia
        countries = [country.name for country in pycountry.countries]
        self.country_combobox.addItems(countries)


        self.ngaynhan_datetime.setDateTime(QDateTime.currentDateTime())  # Mặc định là thời gian hiện tại
        self.ngaynhan_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaynhan_datetime.setCalendarPopup(True)  # Cho phép hiển thị popup lịch
        self.ngaytra_datetime.setDateTime(QDateTime.currentDateTime())  # Mặc định là thời gian hiện tại
        self.ngaytra_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaytra_datetime.setCalendarPopup(True)
        self.add_agreebutton.clicked.connect(self.check_addcustomer)
        self.cancel_button.clicked.connect(self.closedialog)

        self.db = DataBase()
        self.db.connection =None
        self.db.connect()
    def closedialog(self):
        self.close()

    def check_addcustomer(self):

            makh = self.makh_input.text()
            hovaten = self.name_input.text()
            gioitinh = self.gender_combobox.currentText()  # Lấy giá trị đã chọn
            quoctich = self.country_combobox.currentText()

            cccd = self.cccd_input.text()
            sdt = self.sdt_input.text()
            diachi = self.diachi_input.text()
            maphong = self.maphong_input.text()
            ngaynhan = self.ngaynhan_datatime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            ngaytra = self.ngaytra_datatime.dateTime().toString("yyyy-MM-dd HH:mm:ss")

            # Tạo một tuple chứa dữ liệu
            customer_data = (makh, hovaten, gioitinh, quoctich, cccd, sdt, diachi, maphong, ngaynhan, ngaytra)
            if not hovaten or not cccd or not sdt:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ Họ tên, CCCD và Số điện thoại!")
                return

            if (not makh):
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập mã khách hàng !")
                return

            # Gọi hàm thêm khách hàng vào database
            success = self.db.add_customer(customer_data)

            if success:
                QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin khách hàng!")
                self.accept();
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể cập nhật thông tin khách hàng")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = addcustomer_dialog()
    dialog.exec_()  # Dùng exec_() để hiển thị dialog dạng modal (chặn)
