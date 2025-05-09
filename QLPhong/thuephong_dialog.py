import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
from QLKH.database import DataBase
import os
import pycountry
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QAbstractItemView




class thuephong_dialog(QDialog):  # ❗ Kế thừa QDialog
    def __init__(self,maphong):

        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "thuephong_dialog.ui")
        uic.loadUi(ui_path, self)
        self.add_btn.clicked.connect(self.add_customer_inform)
        self.delete_btn.clicked.connect(self.delete_customer_inform)
        self.agree_btn.clicked.connect(self.agree_form)
        self.gioitinh_combobox.addItems(["Nam", "Nữ"])
        self.quoctich_combobox.setEditable(True)
        self.quoctich_combobox.addItem("")  # Thêm dòng trống ở đầu
        self.maphong=maphong
        # Thêm danh sách các quốc gia
        countries = [country.name for country in pycountry.countries]
        self.quoctich_combobox.addItems(countries)
        header = self.danhsachkhachthue_tableview.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Sau khi load UI
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Mã KH", "Họ tên", "Giới tính", "Quốc tịch",
            "CCCD", "SĐT", "Địa chỉ","Mã Phòng"
        ])
        self.danhsachkhachthue_tableview.setModel(self.model)
        self.danhsachkhachthue_tableview.setModel(self.model)
        self.danhsachkhachthue_tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.danhsachkhachthue_tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ngaynhan_datetime.setDateTime(QDateTime.currentDateTime())  # Mặc định là thời gian hiện tại
        self.ngaynhan_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaynhan_datetime.setCalendarPopup(True)  # Cho phép hiển thị popup lịch
        self.ngaytra_datetime.setDateTime(QDateTime.currentDateTime())  # Mặc định là thời gian hiện tại
        self.ngaytra_datetime.setDisplayFormat("yyyy-MM-dd HH:mm:ss")  # Hiển thị theo định dạng Ngày - Giờ
        self.ngaytra_datetime.setCalendarPopup(True)

        self.db = DataBase()
        self.db.connection = None
        self.db.connect()

    def agree_form(self):
        row_count = self.model.rowCount()
        if row_count == 0:
            QMessageBox.warning(self, "Cảnh báo", "Chưa có thông tin khách hàng nào được thêm!")
            return


        for row in range(row_count):
            makh = self.model.item(row, 0).text()
            hoten = self.model.item(row, 1).text()
            gioitinh = self.model.item(row, 2).text()
            quoctich = self.model.item(row, 3).text()
            cccd = self.model.item(row, 4).text()
            sdt = self.model.item(row, 5).text()
            diachi = self.model.item(row, 6).text()
            maphong = self.model.item(row, 7).text()

            ngaynhan = self.ngaynhan_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            ngaytra = self.ngaytra_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")

            customer_data = (makh, hoten, gioitinh, quoctich, cccd, sdt, diachi, maphong, ngaynhan, ngaytra)

            # Gọi hàm thêm khách hàng
            success = self.db.add_customer(customer_data)

            if not success:
                QMessageBox.warning(self, "Lỗi", f"Không thể thêm khách hàng có mã {makh}. Dừng quá trình.")
                return


        maphieuthue = self.db.autocreate_maphieuthue()

        # Tạo phiếu thuê
        self.db.create_phieuthue(maphieuthue, self.maphong, ngaynhan, ngaytra, "ĐANG THUÊ")

        # Gắn từng khách vào phiếu thuê
        for row in range(row_count):
            makh = self.model.item(row, 0).text()
            self.db.add_ct_phieuthue(maphieuthue, makh)

        self.db.update_tranghthairoom(self.maphong)


        self.accept()

        QMessageBox.information(self, "Thành công", "Thuê phòng thành công!")
        self.close()

    def delete_customer_inform(self):

        selected_row = self.danhsachkhachthue_tableview.selectionModel().selectedRows()

        if selected_row:
            row = selected_row[0].row()
            self.model.removeRow(row)
            QMessageBox.information(self, "Thông báo", "Xóa khách hàng thành công!")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một dòng để xóa!")

    def add_customer_inform(self):
        makh = self.makh_input.text()


        if not makh:
            makh = self.db.autocreat_new_makhachhang()
        if self.db.check_makhachhang_exists(makh) or self.is_makh_in_table(makh):
            QMessageBox.warning(self, "Cảnh báo", "Mã khách hàng đã tồn tại !")
            return

        hoten = self.hoten_input.text()
        gioitinh = self.gioitinh_combobox.currentText()
        quoctich = self.quoctich_combobox.currentText()
        cccd = self.cccd_input.text()
        sdt = self.sdt_input.text()
        diachi = self.diachi_input.text()


        ngaynhan = self.ngaynhan_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        ngaytra = self.ngaytra_datetime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        if not hoten or not quoctich or not cccd or not sdt or not diachi :
            QMessageBox.warning(self,"CẢNH BÁO","BẠN VUI LÒNG NHẬP ĐẦY ĐỦ THÔNG TIN!")
            return


        items = [
            QStandardItem(makh),
            QStandardItem(hoten),
            QStandardItem(gioitinh),
            QStandardItem(quoctich),
            QStandardItem(cccd),
            QStandardItem(sdt),
            QStandardItem(diachi),
            QStandardItem(self.maphong),
        ]


        self.model.appendRow(items)
        self.makh_input.clear()
        self.hoten_input.clear()
        self.gioitinh_combobox.setCurrentIndex(0)
        self.quoctich_combobox.setCurrentIndex(0)
        self.cccd_input.clear()
        self.sdt_input.clear()
        self.diachi_input.clear()
        self.ngaynhan_datetime.setDateTime(QDateTime.currentDateTime())
        self.ngaytra_datetime.setDateTime(QDateTime.currentDateTime())


        print(f"{makh=}, {hoten=}, {gioitinh=}, {quoctich=}, {cccd=}, {sdt=}, {diachi=}, {ngaynhan=}, {ngaytra=}")
        print(self.maphong)


    def is_makh_in_table(self, makh):
        # Kiểm tra nếu mã khách hàng đã tồn tại trong bảng
        for row in range(self.model.rowCount()):
            if self.model.item(row, 0).text() == makh:
                return True
        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maphong="test123"
    window = thuephong_dialog(maphong)
    window.show()
    sys.exit(app.exec_())
