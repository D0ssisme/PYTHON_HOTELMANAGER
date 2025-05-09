import pyodbc

class DataBaseStaff:
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
            print(f"Lỗi kết nối SQL: {e}")
            raise

    def get_staff(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM nhanvien")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu nhân viên:", e)
            return []

    def add_staff(self, staff_data):
        cursor = self.connection.cursor()
        try:
            print(f"Dữ liệu thêm vào: {staff_data}")

            query = """
                INSERT INTO NhanVien (
                    manv, hoten, chucvu, sdt, ca_lam
                ) VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, staff_data)
            self.connection.commit()
            print("✅ Thêm nhân viên thành công.")
            return True

        except Exception as e:
            print(f"❌ Lỗi khi thêm nhân viên: {e}")
            return False

        finally:
            if cursor:
                cursor.close()

    def delete_staff(self, manv):
        try:
            cursor = self.connection.cursor()

            # Xóa tất cả dữ liệu liên quan trước
            cursor.execute("DELETE FROM Hoa_Don WHERE manv = ?", (manv,))
            cursor.execute("DELETE FROM ChamCong WHERE manv = ?", (manv,))
            cursor.execute("DELETE FROM NhanVien WHERE manv = ?", (manv,))

            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi xóa nhân viên: {e}")
            return False


