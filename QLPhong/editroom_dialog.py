import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import uic
from QLKH.database import DataBase
import os
from PyQt5.QtWidgets import  QMessageBox

class editroomdialog(QDialog):  # ❗ Kế thừa QDialog
    def __init__(self,maphong):
        super().__init__()

        self.db = DataBase()
        self.db.connection =None
        self.db.connect()
        room=self.db.get_room()
        ui_path = os.path.join(os.path.dirname(__file__), "editroom_dialog.ui")
        uic.loadUi(ui_path, self)
        self.maphong=maphong
        self.maphong_input.setText(self.maphong)
        room = self.db.find_room(self.maphong)

        room_tuple = room[0]  # Lấy tuple đầu tiên trong danh sách


        self.loaiphong_combobox.addItems(["ĐƠN", "ĐÔI","VIP"])
        self.loaiphong_combobox.setCurrentText(f"{room_tuple[1]}")

        self.giaphong_input.setText(f"{room_tuple[2]}")
        self.trangthai_input.addItems(["TRỐNG","ĐANG THUÊ","ĐANG DỌN DẸP"])
        self.trangthai_input.setCurrentText(f"{room_tuple[3]}")
        self.tiennghi_text.setText(f"{room_tuple[4]}")
        self.cancel_btn.clicked.connect(self.close)
        self.agree_btn.clicked.connect(self.checkeditroom)



    def checkeditroom(self):

        maphong = self.maphong_input.text()
        loaiphong = self.loaiphong_combobox.currentText()
        giaphong = self.giaphong_input.text()
        trangthai = self.trangthai_input.currentText()
        tiennghi = self.tiennghi_text.toPlainText()  # nếu là QTextEdit
        room_data = (loaiphong, giaphong, trangthai, tiennghi, maphong)
        if not loaiphong or not giaphong or not trangthai or not tiennghi  :
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ !")
            return

        try:
            if self.db.update_room(room_data):
                QMessageBox.information(self, "Thành công", "Đã cập nhật phòng thành công!")
                self.accept()
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể cập nhật phòng")
        except Exception as e:
            print(e)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    maphong="P101"

    window = editroomdialog(maphong)
    window.show()
    sys.exit(app.exec_())
