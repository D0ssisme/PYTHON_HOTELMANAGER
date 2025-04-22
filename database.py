import pyodbc

class DataBase:
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
            print("Kết nối SQL Server thành công!")
        except pyodbc.Error as e:
            print(f"Lỗi kết nối SQL: {e}")
            raise

    def get_customers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM khachhang")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu khách hàng:", e)
            return []

    def check_login(self, username, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT [mat khau] FROM login WHERE [tai khoan] = ?", (username,))
            result = cursor.fetchone()
            return result and result[0] == password
        except Exception as e:
            print("Lỗi khi kiểm tra đăng nhập:", e)
            return False

    def close(self):
        if self.connection:
            self.connection.close()



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
