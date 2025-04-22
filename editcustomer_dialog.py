from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import  QMessageBox
from main import mainui
class editcustomer_dialog(QtWidgets.QDialog):
    def __init__(self,makh):
        super().__init__()
        uic.loadUi("editcustomer_dialog.ui", self)  # Load file .ui
        self.setWindowTitle("THÊM KHÁCH HÀNG")
        self.makh_value.setText(makh)  # Đặt giá trị mới cho QLineEdit







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = editcustomer_dialog()
    dialog.exec_()  # Dùng exec_() để hiển thị dialog dạng modal (chặn)
