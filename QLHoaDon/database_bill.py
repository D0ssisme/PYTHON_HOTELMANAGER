import pyodbc
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDateTime
from PyQt5.uic.properties import QtWidgets


class DataBaseBill:
        def __init__(self):
            self.connection = None
            self.connect()

        def connect(self):
            try:
                server = r"DESKTOP-3FTCGLC\SQLSERVER2022"
                database = "HotelManagement"
                username = "manhdung"
                password = "29052005"
                self.connection = pyodbc.connect(
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password}"
                )
                print("Kết nối SQL Server thành công!")
            except pyodbc.Error as e:
                    print(f"Lỗi kết nối SQL:{e}")
                    raise

        def get_bill(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM hoa_don")
                bills = cursor.fetchall()  # <<< Phải fetch dữ liệu
                return bills  # <<< Phải return bills
            except Exception as e:
                print("Lỗi khi lấy dữ liệu hóa đơn:", e)
                return []

        def add_bill(self, bill_data):
            cursor = self.connection.cursor()
            try:
                print(f"Dữ liệu thêm hóa đơn: {bill_data}")

                query = """
                    INSERT INTO hoa_don (
                        mahoa_don, maphieuthue, manv, ngaylap, tongtien 
                    ) VALUES (?, ?, ?, ?, ?)
                """
                cursor.execute(query, bill_data)
                self.connection.commit()
                print("✅ Thêm hóa đơn thành công.")
                return True

            except Exception as e:
                print(f"❌ Lỗi khi thêm hóa đơn: {e}")
                return False
            finally:
                if cursor:
                    cursor.close()

        def delete_bill(self, mahd):
            try:
                cursor = self.connection.cursor()

                # Xóa chi tiết hóa đơn trước để tránh vi phạm khóa ngoại
                cursor.execute("DELETE FROM Hoa_Don WHERE mahoa_don = ?", (mahd,))

                self.connection.commit()
                return True
            except pyodbc.Error as e:
                print(f"Lỗi khi xóa hóa đơn: {e}")
                return False



        def show_bill_detail(self, mahd):
            from QLHoaDon.detailbill_dialog import detailbill_dialog

            try:
                cursor = self.connection.cursor()

                if not mahd:
                    QMessageBox.warning(None, "Lỗi", "Mã hóa đơn không hợp lệ.")
                    return

                cursor.execute("""
                    SELECT hd.mahoa_don, kh.hoten, hd.tongtien, pt.maphong, pt.ngaytra
                            
                    FROM hoa_don hd
                    JOIN chitietphieuthuephong ctptp ON hd.maphieuthue = ctptp.maphieuthue
                    JOIN phieuthue pt ON hd.maphieuthue = pt.maphieuthue 
                    JOIN khachhang kh ON ctptp.makh = kh.makh
                    WHERE hd.mahoa_don = ?
                """, (mahd,))
                result = cursor.fetchone()

                if not result:
                    QMessageBox.warning(None, "Lỗi", f"Không tìm thấy thông tin cho hóa đơn {mahd}")
                    return

                mahoadon, hoten, tongtien, maphong, ngaytra = result

                # Mở dialog chi tiết
                dialog = detailbill_dialog(mahoadon, hoten, tongtien, maphong, ngaytra)
                dialog.exec_()

            except Exception as e:
                QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi:\n{str(e)}")



