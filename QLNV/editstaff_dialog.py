from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import  QMessageBox
import pycountry
import os
from QLNV.database_staff import DataBaseStaff
class editstaff_dialog(QtWidgets.QDialog):
    def __init__(self, manv, hoten, chucvu, calam, sdt):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "editstaff_dialog.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("CHỈNH SỬA NHÂN VIÊN")

        # Gán giá trị cho các widget
        self.manv_value.setText(manv)
        self.manv_value.setReadOnly(True)
        self.hotennv_value.setText(hoten)

        self.chucvu_value.addItems(["Lễ tân", "Quản lý", "Tạp vụ", "Bảo vệ", "Bảo trì"])
        self.chucvu_value.setCurrentText(chucvu)

        self.calam_value.addItems(["Ca sáng", "Ca chiều", "Ca tối", "Hành chính"])
        self.calam_value.setCurrentText(calam)

        self.sdtnv_value.setText(sdt)

        # Kết nối nút
        self.cancel_button.clicked.connect(self.close)
        self.agree_button.clicked.connect(self.check_editstaff)

        # Khởi tạo DB
        self.db = DataBaseStaff()
        self.db.connection = None
        self.db.connect()


    def check_editstaff(self):
        manv = self.manv_value.text()
        hoten = self.hotennv_value.text()
        chucvu = self.chucvu_value.currentText()
        calam = self.calam_value.currentText()
        sdt = self.sdtnv_value.text()

        if not hoten or not sdt:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        try:
            cursor = self.db.connection.cursor()
            query = """
                UPDATE nhanvien
                SET hoten = ?, chucvu = ?, ca_lam = ?, sdt = ?
                WHERE manv = ?
            """
            cursor.execute(query, (hoten, chucvu, calam, sdt, manv))
            self.db.connection.commit()
            QMessageBox.information(self, "Thành công", "Cập nhật thông tin nhân viên thành công.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {str(e)}")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Dữ liệu mẫu để test giao diện
    manv = "NV001"
    hoten = "Nguyễn Thị A"
    chucvu = "Lễ tân"
    calam = "Ca sáng"
    sdt = "0911111111"

    # Tạo dialog và truyền dữ liệu test
    dialog = editstaff_dialog(manv, hoten, chucvu, calam, sdt)
    dialog.exec_()
