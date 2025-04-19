from PyQt5 import QtWidgets, uic
import sys

class MyWindow(QtWidgets.QMainWindow):  # Hoặc QDialog nếu là dialog
    def __init__(self):
        super().__init__()
        uic.loadUi("TrangChu.ui", self)  # Load file .ui vào lớp này
        self.setWindowTitle("Cửa sổ từ file .ui")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
