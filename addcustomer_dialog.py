from PyQt5 import QtWidgets, uic
import sys

class addcustomer_dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("addcustomer_dialog.ui", self)  # Load file .ui
        self.setWindowTitle("THÊM KHÁCH HÀNG")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = dialog_edituser()
    dialog.exec_()  # Dùng exec_() để hiển thị dialog dạng modal (chặn)
