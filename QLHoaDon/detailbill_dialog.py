from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDateTime
import sys
import os
from QLHoaDon.database_bill import DataBaseBill

class detailbill_dialog(QtWidgets.QDialog):
    def __init__(self, mahoadon, hoten, tongtien, maphong, ngaytra):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "detailbill_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("THÔNG TIN HÓA ĐƠN")

        # Gán dữ liệu vào các ô trên giao diện
        self.mahd_value.setText(mahoadon)
        self.hoten_value.setText(hoten)
        self.tongtien_value.setText(f"{tongtien:,.0f}")
        self.maphong_value.setText(maphong)

        # Chuyển chuỗi ngày thành QDateTime
        qdt = QDateTime(ngaytra)  # chuyển từ datetime sang QDateTime
        self.ngaytra_value.setDateTime(qdt)

        # Không cho chỉnh sửa các ô
        for field in [self.mahd_value, self.hoten_value, self.tongtien_value,
                       self.maphong_value]:
            field.setReadOnly(True)
        self.ngaytra_value.setReadOnly(True)

        # Nút thoát
        self.cancel_button.clicked.connect(self.close)

# Chạy thử nếu cần
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = detailbill_dialog(
        "HD002", "Trần Thị B", 1600000,
        "102", "2025-04-23 00:00:00",
    )
    dialog.exec_()
