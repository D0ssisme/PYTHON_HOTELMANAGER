import sys
import pyodbc
import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QPushButton, QHeaderView, QMessageBox, QDialog, QLabel, QFormLayout, QDateEdit,
    QComboBox,QDateTimeEdit
)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QDateTime


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            server = r"DESKTOP-3FTCGLC\SQLSERVER2022"
            database = "hotel"
            username = "manhdung"
            password = "29052005"

            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            print("ket noi sql thanh cong!")
        except pyodbc.Error as e:
            print(f"Lỗi kết nối SQL: {e}")
            raise



    def get_customers(self):
        cursor = self.connection.cursor()
        data=cursor.execute("select * from khachhang")
        return data








    def add_customer(self, customer_data):

        cursor = self.connection.cursor()

        try:
            print(f"Dữ liệu thêm vào: {customer_data}")  # Debug xem dữ liệu truyền vào

            query = """
                INSERT KhachHang (
                    makh, hovaten, gioitinh, quoctich, cccd, 
                    sdt, diachi, maphong, ngaynhan, ngaytra
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, customer_data)
            self.connection.commit()
            print("Thêm khách hàng thành công.")
            return True


        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")

        finally:
            if cursor:
                cursor.close()


    def update_customer(self, customer_data):
        cursor = self.connection.cursor()
        query = """
            UPDATE KhachHang 
            SET hovaten=?, gioitinh=?, quoctich=?, cccd=?, sdt=?, 
                diachi=?, maphong=?, ngaynhan=?, ngaytra=?
            WHERE makh=?
        """
        try:
            cursor.execute(query, customer_data[1:] + [customer_data[0]])
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            return False

    def delete_customer(self, makh):
        cursor = self.connection.cursor()
        query = "DELETE FROM KhachHang WHERE makh = ?"
        try:
            cursor.execute(query, (makh,))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            return False


    def close(self):
        if self.connection:
            self.connection.close()






# dialog thêm khách hàng
class ThemKhachHangDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Thêm khách hàng mới")
        self.setFixedSize(400, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.inputs = []

        fields = [
            ("Mã KH", False), ("Họ và tên", False), ("Giới tính", False),
            ("Quốc tịch", False), ("Căn cước công dân", False),
            ("Số điện thoại", False), ("Địa chỉ", False), ("Số phòng", False),
            ("Ngày nhận", False), ("Ngày trả", False)
        ]

        for label, read_only in fields:
            lbl = QLabel(label)
            if label == "Giới tính":
                edit = QComboBox()
                edit.addItems(["Nam", "Nữ", "Khác"])
            elif label in ["Ngày nhận", "Ngày trả"]:
                edit = QDateTimeEdit()
                edit.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
                edit.setCalendarPopup(True)
                edit.setDateTime(QDateTime.currentDateTime())

            else:
                edit = QLineEdit()
                if label == "Mã KH":
                    edit.setPlaceholderText("Tự động tạo nếu để trống")

            self.inputs.append(edit)
            form_layout.addRow(lbl, edit)

        layout.addLayout(form_layout)
        self.add_button = QPushButton("Thêm")
        self.add_button.setStyleSheet("background-color: green; color: white; padding: 5px;")
        self.add_button.clicked.connect(self.check_add)
        layout.addWidget(self.add_button)

    def check_add(self):
        new_data = []

        for edit in self.inputs:  # Duyệt theo danh sách
            if isinstance(edit, QComboBox):
                new_data.append(edit.currentText())
            elif isinstance(edit, QDateTimeEdit):
                new_data.append(edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"))
            else:
                new_data.append(edit.text().strip())

        # Kiểm tra thông tin bắt buộc
        if not new_data[1] or not new_data[4] or not new_data[5]:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ Họ tên, CCCD và Số điện thoại!")
            return

        if not new_data[0]:
            QMessageBox.warning(self, "Cảnh báo", "Mã khách hàng không được để trống !")

        if self.parent().db.add_customer(new_data):
            self.parent().load_data()
            QMessageBox.information(self, "Thành công", "Đã thêm khách hàng mới thành công!")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể thêm khách hàng vào database")

        self.accept();





class SuaKhachHangDialog(QDialog):
    def __init__(self, parent, row_data, row_index):
        super().__init__(parent)
        self.setWindowTitle("Chỉnh sửa khách hàng")
        self.setFixedSize(400, 400)
        self.row_data = row_data
        self.row_index = row_index
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        self.inputs = []

        labels = [
            "Mã KH", "Họ và tên", "Giới tính", "Quốc tịch", "Căn cước công dân",
            "Số điện thoại", "Địa chỉ", "Số phòng", "Ngày nhận", "Ngày trả"
        ]

        for i, label in enumerate(labels):
            lbl = QLabel(label)
            if i == 2:
                edit = QComboBox()
                edit.addItems(["Nam", "Nữ", "Khác"])
                edit.setCurrentText(self.row_data[i])
            elif i in [8, 9]:
                edit = QDateTimeEdit()
                edit.setDisplayFormat("dd/MM/yyyy HH:mm:ss")
                edit.setCalendarPopup(True)

                if isinstance(self.row_data[i], datetime.datetime):
                    date_time_value = QDateTime.fromString(self.row_data[i].strftime("%d/%m/%Y %H:%M:%S"), "dd/MM/yyyy HH:mm:ss")
                else:

                    date_time_value = QDateTime.fromString(self.row_data[i], "dd/MM/yyyy HH:mm:ss")
                edit.setDateTime(date_time_value)
            else:
                edit = QLineEdit(self.row_data[i])
                if i == 0:
                    edit.setReadOnly(True)
                    edit.setStyleSheet("background-color: lightgray;")
            self.inputs.append(edit)
            form_layout.addRow(lbl, edit)

        layout.addLayout(form_layout)
        self.save_button = QPushButton("Lưu")
        self.save_button.setStyleSheet("background-color: green; color: white; padding: 5px;")
        self.save_button.clicked.connect(self.check_save)
        layout.addWidget(self.save_button)

    def check_save(self):
        new_data = []
        for i, edit in enumerate(self.inputs):
            if isinstance(edit, QComboBox):
                new_data.append(edit.currentText())
            elif isinstance(edit, QDateTimeEdit):
                new_data.append(edit.dateTime().toString("dd/MM/yyyy HH:mm:ss"))
            else:
                new_data.append(edit.text())



        if self.parent().db.update_customer(new_data):
            self.parent().load_data()
            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin khách hàng!")
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể cập nhật thông tin khách hàng")

        self.accept()


class QLKHMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Quản lý khách hàng")
        self.resize(1200, 600)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Thanh tìm kiếm
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo mã KH, tên hoặc số điện thoại...")
        self.search_input.setFixedHeight(35)
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Tìm kiếm")
        self.search_button.setFixedSize(100, 35)
        self.search_button.clicked.connect(self.search_customer)
        search_layout.addWidget(self.search_button)

        self.show_all_button = QPushButton("Hiển thị tất cả")
        self.show_all_button.setFixedSize(120, 35)
        self.show_all_button.clicked.connect(self.load_data)
        search_layout.addWidget(self.show_all_button)

        search_layout.addStretch()

        self.add_button = QPushButton("Thêm khách hàng")
        self.add_button.setFixedSize(150, 35)
        self.add_button.clicked.connect(self.open_add_dialog)
        search_layout.addWidget(self.add_button)

        self.main_layout.addLayout(search_layout)
        self.main_layout.addSpacing(10)

        # Bảng hiển thị
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Mã KH", "Họ và Tên", "Giới tính", "Quốc tịch", "Căn cước công dân",
            "Số điện thoại", "Địa chỉ", "Số phòng", "Ngày nhận", "Ngày trả", "Sửa", "Xóa"
        ])


        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px :
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)

        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF50;
         
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(self.table)



    def load_data(self):
            customers = self.db.get_customers()
            self.data = []

            for row in customers:
                self.data.append([
                    row.makh if row.makh else "",
                    row.hovaten if row.hovaten else "",
                    row.gioitinh if row.gioitinh else "",
                    row.quoctich if row.quoctich else "",
                    row.cccd if row.cccd else "",
                    row.sdt if row.sdt else "",
                    row.diachi if row.diachi else "",
                    row.maphong if row.maphong else "",
                    row.ngaynhan if row.ngaynhan else "",
                    row.ngaytra if row.ngaytra else ""
                ])

            self.all_data = self.data.copy()
            self.update_table()



    def update_table(self, data=None):
        if data is None:
            data = self.data

        self.table.setRowCount(len(data))

        for i, row in enumerate(data):
            for j, item in enumerate(row[:10]):
                self.table.setItem(i, j, QTableWidgetItem(str(item)))


            edit_btn = QPushButton()
            edit_btn.setToolTip("Sửa")
            edit_btn.setIcon(QIcon("image/pngtree-vector-tools-repair-icon-png-image_516354"))
            edit_btn.clicked.connect(lambda _, r=i: self.open_edit_dialog(r))
            self.table.setCellWidget(i, 10, edit_btn)


            delete_btn = QPushButton()
            delete_btn.setToolTip("Xóa")
            delete_btn.setIcon(
                QIcon("image/pngtree-trash-can-flat-red-color-icon-recycle-dustbin-glyph-vector-picture-image_9756861"))
            delete_btn.clicked.connect(lambda _, r=i: self.confirm_delete(r))
            self.table.setCellWidget(i, 11, delete_btn)

    def search_customer(self):
        keyword = self.search_input.text().strip().lower()

        filtered_data = [
            row for row in self.all_data
            if keyword in row[0].lower() or  # Mã KH
               keyword in row[1].lower() or  # Họ tên
               keyword in row[5].lower()  # Số điện thoại
        ]
        self.update_table(filtered_data)

    def open_add_dialog(self):
        dialog = ThemKhachHangDialog(self)
        dialog.exec_()


    def open_edit_dialog(self, row_index):
            dialog = SuaKhachHangDialog(self, self.data[row_index], row_index)
            dialog.exec_()







    def confirm_delete(self, row_index):
        ma_kh = self.data[row_index][0]
        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa khách hàng {ma_kh}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db.delete_customer(ma_kh):
                self.load_data()
                QMessageBox.information(self, "Thành công", "Đã xóa khách hàng thành công!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa khách hàng")

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QLKHMain()
    window.show()
    sys.exit(app.exec_())