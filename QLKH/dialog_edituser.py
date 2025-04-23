from PyQt5 import QtWidgets, uic
import sys


class dialog_edituser(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("dialog_edituser.ui", self)  # Load file .ui
        self.setWindowTitle("Thông tin người dùng")
        self.taikhoan_radiobutton.toggled.connect(self.switch_page)
        self.matkhau_radiobutton.toggled.connect(self.switch_page)

    def switch_page(self):
            if self.taikhoan_radiobutton.isChecked():
                self.stackedWidget.setCurrentIndex(0)
            elif self.matkhau_radiobutton.isChecked():
                self.stackedWidget.setCurrentIndex(1)# Trang mật khẩu

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = dialog_edituser()
    dialog.exec_()  # Dùng exec_() để hiển thị dialog dạng modal (chặn)
