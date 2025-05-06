from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QMessageBox
import os
from QLHoaDon.database_bill import DataBaseBill  # Kết nối đúng file database bill

class editbill_dialog(QtWidgets.QDialog):
    def __init__(self, mahoadon, madatphong, manv, ngaylap, tongtien):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "editbill_dialog.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("CHỈNH SỬA HÓA ĐƠN")

        self.mahd_value.setText(mahoadon)
        self.mahd_value.setReadOnly(True)
        self.madp_value.setText(madatphong)
        self.manv_value.setText(manv)
        self.ngaylap_value.setText(ngaylap)
        self.tongtien_value.setText(tongtien)

        self.cancel_button.clicked.connect(self.close)
        self.agree_button.clicked.connect(self.check_editbill)

        self.db = DataBaseBill()
        self.db.connection = None
        self.db.connect()

    def check_editbill(self):
        if not self.db.connection:
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối đến cơ sở dữ liệu.")
            return

        mahoadon   = self.mahd_value.text().strip()
        madatphong = self.madp_value.text().strip()
        manv       = self.manv_value.text().strip()
        ngaylap    = self.ngaylap_value.text().strip()
        raw_tongtien = self.tongtien_value.text().strip()

        if not all([mahoadon, madatphong, manv, raw_tongtien]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ các trường bắt buộc!")
            return

        clean_tien = raw_tongtien.replace(".", "")
        try:
            tongtien_num = float(clean_tien)
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá trị Tổng Tiền không hợp lệ!")
            return

        cursor = self.db.connection.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM hoa_don WHERE mahoa_don = ?", (mahoadon,))
            if cursor.fetchone()[0] == 0:
                QMessageBox.warning(self, "Lỗi", f"Hóa đơn {mahoadon} không tồn tại!")
                return

            query = """
                UPDATE hoa_don
                SET maphieuthue = ?, manv = ?, ngaylap = ?, tongtien = ?
                WHERE mahoa_don = ?
            """
            cursor.execute(query, (
                madatphong,
                manv,
                ngaylap,
                tongtien_num,
                mahoadon
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Thành công", "Cập nhật thông tin hóa đơn thành công.")
            self.accept()

        except Exception as e:
            self.db.connection.rollback()
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi cập nhật: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = editbill_dialog(
        "HD001", "DP001", "NV001",
        "2025-04-26 10:00:00", "1.500.000",
        "Tiền mặt", "Đã thanh toán"
    )
    dialog.exec_()
