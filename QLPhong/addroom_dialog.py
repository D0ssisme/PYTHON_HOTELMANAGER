import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
import os
from QLKH.database import DataBase
from PyQt5.QtWidgets import  QMessageBox

class addroomdialog(QDialog):  # ❗ Kế thừa QDialog
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "addroom_dialog.ui")
        uic.loadUi(ui_path, self)
        self.loaiphong_combobox.addItems(["ĐƠN", "ĐÔI","VIP"])
        self.trangthai_combobox.addItems(["TRỐNG", "ĐANG DỌN DẸP", "ĐANG BẢO TRÌ","ĐANG SỬ DỤNG"])
        self.db = DataBase()
        self.db.connection = None
        self.db.connect()
        self.agree_button.clicked.connect(self.checkaddroom)
        self.cancel_button.clicked.connect(self.close)

    def checkaddroom(self):
        # Lấy dữ liệu từ các input
        maphong = self.maphong_input.text().strip()
        giaphong = self.giaphong_input.text().strip()
        tiennghi = self.tiennghi_input.toPlainText().strip()
        loaiphong = self.loaiphong_combobox.currentText().strip()
        trangthai = self.trangthai_combobox.currentText().strip()  # Sửa lỗi "curentText"

        # Kiểm tra dữ liệu có trống không
        if not all([maphong, giaphong, tiennghi, loaiphong, trangthai]):
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin !")
            return
        if self.db.check_maphong_exists(maphong):
            QMessageBox.warning(self, "Lỗi", f"Mã phòng '{maphong}' đã tồn tại.")
            return
        # Kiểm tra giaphong là số
        try:
            giaphong = float(giaphong)
        except ValueError:
            QMessageBox.warning(self, "Cảnh báo", "giá phòng phải là số!")
            return

        # Tạo tuple dữ liệu
        room_data = (maphong, loaiphong, giaphong, trangthai, tiennghi)

        # Gọi hàm thêm phòng trong lớp database
        success = self.db.add_room(room_data)
        if success:
            QMessageBox.information(self, "Thành công", "Đã thêm phòng thành công!")
            self.accept();
        else:
            QMessageBox.information(self, "Thành công", "thêm thất bại !")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addroomdialog()
    window.show()
    sys.exit(app.exec_())
