from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDateTime  # Import QDateTime

from QLHoaDon.database_bill import DataBaseBill  # Import đúng file database bill

import os


class addbill_dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "addbill_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("THÊM HÓA ĐƠN")

        # Kết nối các nút
        self.add_agreebutton.clicked.connect(self.check_addbill)
        self.cancel_button.clicked.connect(self.close)

        # Kết nối database
        self.db = DataBaseBill()
        self.db.connection = None
        self.db.connect()

    def check_addbill(self):
        mahoadon = self.mahd_input.text()
        mathuephong = self.madp_input.text()
        manv = self.manv_input.text()

        # Lấy ngày và giờ hiện tại
        ngaylap = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")

        tongtien = self.tongtien_input.text()


        # Kiểm tra dữ liệu bắt buộc
        if not mathuephong or not manv or not tongtien:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ các trường bắt buộc!")
            return

        # Nếu để trống mã hóa đơn, tự tạo
        # if not mahoadon:
        #     mahoadon = "HD" + str(self.db.get_next_bill_id())  # Bạn cần làm hàm get_next_bill_id()

        bill_data = (mahoadon, mathuephong, manv, ngaylap, tongtien)
        success = self.db.add_bill(bill_data)

        if success:
            QMessageBox.information(self, "Thành công", "Đã thêm hóa đơn thành công!")
            self.accept()
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể thêm hóa đơn.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = addbill_dialog()
    dialog.exec_()
