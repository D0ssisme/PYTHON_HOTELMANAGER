import sys
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os
from QLKH.database import DataBase
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication,QHeaderView
from PyQt5.QtWidgets import QAbstractItemView
from src.checkin_module import recognize_face_from_camera


class nhanphong_dialog(QDialog):  # ❗ Kế thừa QDialog
    def __init__(self,maphieudat):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "chitietphieudat_dialog.ui")
        uic.loadUi(ui_path, self)
        self.maphieudat=maphieudat

        self.db = DataBase()
        self.db.connection = None
        self.db.connect()
        self.load_dataphieudat()
        self.load_datatableview()
        self.agree_btn.clicked.connect(lambda : self.check_agreenhanphong(self.maphieudat))
        self.cancel_btn.clicked.connect(self.close)
        self.maphieudat_input.setReadOnly(True)
        self.ngaynhan_input.setReadOnly(True)
        self.ngaytra_input.setReadOnly(True)
        self.maphong_input.setReadOnly(True)






    def load_datatableview(self):
        data_customerdat = self.db.get_chitietphieudat(self.maphieudat)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Mã Khách Hàng", "Tên Khách Hàng", "Giới Tính", "Quốc Tịch",
            "CCCD", "SĐT", "Địa chỉ"
        ])
        self.khachdat_tableview.setModel(self.model)

        # Thêm dữ liệu vào model
        for row in data_customerdat:
            items = [QStandardItem(str(cell)) for cell in row]
            self.model.appendRow(items)

        # Căn chỉnh cột cho đẹp
        header = self.khachdat_tableview.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

        # Chỉ chọn 1 hàng, ẩn chỉ số, chỉnh màu
        self.khachdat_tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.khachdat_tableview.setSelectionMode(QAbstractItemView.SingleSelection)
        self.khachdat_tableview.verticalHeader().setVisible(False)
        self.khachdat_tableview.setStyleSheet("""
            QTableView {
                border: none;
                outline: none;
        
            }
            QHeaderView::section {
           
                padding: 4px;
                font-weight: bold;
                border: none;
            }
        """)

    def load_dataphieudat(self):

        data_phieudat=self.db.find_phieutdat(self.maphieudat)

        if data_phieudat:
            # Lấy dòng đầu tiên
            row = data_phieudat[0]
            self.maphieudat_input.setText(str(row[0]))
            self.ngaynhan_input.setText(str(row[3]))
            self.ngaytra_input.setText(str(row[4]))
            self.maphong_input.setText(str(row[1]))

    def check_agreenhanphong(self, maphieudat):
        list_makh = self.db.lay_ds_khach_tu_phieudat(maphieudat)

        try:
            makh = recognize_face_from_camera()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", f"Đã xảy ra lỗi khi nhận diện khuôn mặt:\n{e}")
            return

        if makh is None:
            QMessageBox.warning(self, "THẤT BẠI", "Không nhận diện được khuôn mặt.")
            return

        if makh not in list_makh:
            QMessageBox.warning(self, "Sai người", f"{makh} không có trong danh sách khách hàng của phiếu đặt này.")
            return

        if self.db.nhan_phong_tu_phieudat(maphieudat):
            QMessageBox.information(self, "Thành công", "Nhận phòng thành công!")
            self.accept()
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể nhận phòng.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maphieudat="test666"
    window = nhanphong_dialog(maphieudat)
    window.show()
    sys.exit(app.exec_())
