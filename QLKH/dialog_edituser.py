from PyQt5 import QtWidgets, uic
import sys
import os
from PyQt5.QtWidgets import  QMessageBox
from QLKH.database import DataBase
from PyQt5.QtCore import pyqtSignal, QObject

class dialog_edituser(QtWidgets.QDialog):
    update_completed = pyqtSignal()
    def __init__(self,user,password):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "dialog_edituser.ui")
        uic.loadUi(ui_path, self)
        self.setWindowTitle("Thông tin người dùng")
        self.taikhoan_radiobutton.toggled.connect(self.switch_page)
        self.matkhau_radiobutton.toggled.connect(self.switch_page)
        self.taikhoan_radiobutton.setChecked(True)
        self.taikhoan_input.setText(user)
        self.cancel_button.clicked.connect(self.close)
        self.agree_button.clicked.connect(self.checksave)
        self.db = DataBase()
        self.db.connect()
        self.user = user
        self.password = password

    def checksave(self):
        from login import loginui
        newusername = self.taikhoan_input.text()
        passold=self.matkhaucu_input.text()
        passnew1=self.matkhaumoi1_input.text()
        passnew2=self.matkhaumoi2_input.text()
        if self.user is None:

            QMessageBox.warning(self,"enrror")

        if self.taikhoan_radiobutton.isChecked():


            reply = QMessageBox.question(
                self, "Xác nhận Sửa",
                f"Bạn có chắc chắn muốn sửa từ {self.user} tài khoản thành {newusername}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if self.db.update_taikhoanuser(self.user,newusername):

                    QMessageBox.information(self, "Thành công", "Đã Sửa khách hàng thành công!")
                    self.update_completed.emit()

                    self.close()
                else:
                    QMessageBox.critical(self, "Lỗi", "Không thể Sửa khách hàng")


        else :
            if not passold or not passnew1 or not passnew2:
                QMessageBox.warning(self,"Cảnh báo",f"Vui Lòng Nhập Đầy Đủ Thông Tin")
            else :
                if not passold or not passnew1 or not passnew2:
                    QMessageBox.warning(self, "Cảnh báo", "Vui Lòng Nhập Đầy Đủ Thông Tin")
                else:
                    if passold != self.password:
                        QMessageBox.warning(self, "Lỗi", "Mật khẩu cũ không chính xác.")
                    elif passnew1 != passnew2:  # Sử dụng elif thay cho else + điều kiện
                        QMessageBox.warning(self, "Cảnh báo", "Mật Khẩu Mới Không Khớp ")
                    else :
                        reply = QMessageBox.question(
                            self, "Xác nhận Sửa",
                            f"Bạn có chắc chắn muốn sửa mật khẩu ?",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        if reply == QMessageBox.Yes:
                            if self.db.update_matkhauuser(self.user, passnew2):

                                QMessageBox.information(self, "Thành công", "Đã Mật Khẩu thành công!")
                                self.update_completed.emit()

                                self.close()
                            else:
                                QMessageBox.critical(self, "Lỗi", "Không thể Sửa Mật Khẩu")




    def switch_page(self):
            if self.taikhoan_radiobutton.isChecked():
                self.stackedWidget.setCurrentIndex(0)
            elif self.matkhau_radiobutton.isChecked():
                self.stackedWidget.setCurrentIndex(1)# Trang mật khẩu

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    user="1234"
    password="1234"
    dialog = dialog_edituser(user,password)
    dialog.exec_()  # Dùng exec_() để hiển thị dialog dạng modal (chặn)
