from multiprocessing.spawn import old_main_modules

import pyodbc
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import  QMessageBox


class DataBase:
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

    def get_customers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM khachhang")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu khách hàng:", e)
            return []

    def get_phieudat(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM phieudat")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phiếu đặt  :", e)
            return []
    def check_login(self, username, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT [matkhau] FROM login WHERE [taikhoan] = ?", (username,))
            result = cursor.fetchone()
            return result and result[0] == password
        except Exception as e:
            print("Lỗi khi kiểm tra đăng nhập:", e)
            return False

    def close(self):
        if self.connection:
            self.connection.close()





    def find_customer(self,makh):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM khachhang WHERE makh LIKE '{makh}%'")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu khách hàng:", e)
            return []



    def find_phieuthue(self,maphphong):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM phieuthue WHERE maphong LIKE '{maphphong}%'")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu khách hàng:", e)
            return []


    def add_customer(self, customer_data):

        cursor = self.connection.cursor()



        try:
            print(f"Dữ liệu thêm vào: {customer_data}")  # Debug xem dữ liệu truyền vào

            query = """
                INSERT KhachHang (
                    makh, hoten, gioitinh, quoctich, cccd, 
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

    def update_customer(self, customer_data):
        cursor = self.connection.cursor()
        query = """
            UPDATE KhachHang 
            SET hoten=?, gioitinh=?, quoctich=?, cccd=?, sdt=?, 
                diachi=?, maphong=?, ngaynhan=?, ngaytra=?
            WHERE makh=?
        """
        try:

            cursor.execute(query, customer_data)
            self.connection.commit()

            if cursor.rowcount == 0:
                print("Không có dòng nào được cập nhật. Có thể mã khách hàng không tồn tại.")
                return False

            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            return False


    def update_taikhoanuser(self,oldtaikhoan,newtaikhoan):
        cursor = self.connection.cursor()
        query="""
        UPDATE login
        set taikhoan=?
        WHERE taikhoan=?
        """
        try :
            cursor.execute(query, (newtaikhoan, oldtaikhoan))
            self.connection.commit()
            return True

        except Exception as e:
            print("Lỗi khi cập nhật tài khoản:", e)
            return False

    def update_matkhauuser(self,taikhoan,matkhaunew):
        cursor=self.connection.cursor()
        query="""
        UPDATE login
        SET matkhau=?
        WHERE taikhoan=?
        """
        try:
            cursor.execute(query,(matkhaunew,taikhoan))
            self.connection.commit()
            return True


        except Exception as e:
            print("lỗi khi cập nhật mật khẩu :",e)
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Đã ngắt kết nối SQL Server.")


    def get_room(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM phong")
                return cursor.fetchall()
            except Exception as e:
                print("Lỗi khi lấy dữ liệu phongf :", e)
                return []




    def get_room(self):
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM phong")
                return cursor.fetchall()
            except Exception as e:
                print("Lỗi khi lấy dữ liệu phongf :", e)
                return []

    def find_room(self, maphong):
        try:
            cursor = self.connection.cursor()
            # Đảm bảo maphong được bao quanh bởi dấu nháy đơn nếu là chuỗi
            cursor.execute(f"SELECT * FROM phong WHERE maphong='{maphong}'")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phòng:", e)
            return []




    def add_room(self, room_data):

        cursor = self.connection.cursor()

        try:
            print(f"Dữ liệu thêm vào: {room_data}")  # Debug xem dữ liệu truyền vào

            query = """
                INSERT phong (
                    maphong, loaiphong, giaphong, trangthai, tiennghi
                
                ) VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, room_data)
            self.connection.commit()
            print("Thêm phòng thành công.")
            return True

        except pyodbc.IntegrityError as e:
            print("❌ Lỗi: Trùng mã phòng (PRIMARY KEY).")

        except Exception as e:
            print(f"❌ Lỗi không xác định: {e}")

        finally:
            if cursor:
                cursor.close()

    def check_maphong_exists(self, maphong):
        cursor = self.connection.cursor()
        try:
            query = "SELECT COUNT(*) FROM phong WHERE maphong = ?"
            cursor.execute(query, (maphong,))
            result = cursor.fetchone()
            return result[0] > 0  # Trả về True nếu có ít nhất 1 bản ghi
        except Exception as e:
            print(f"❌ Lỗi khi kiểm tra mã phòng: {e}")
            return False
        finally:
            cursor.close()

    def check_makhachhang_exists(self, makh):
        cursor = self.connection.cursor()
        try:
            query = "SELECT COUNT(*) FROM khachhang WHERE makh = ?"
            cursor.execute(query, (makh,))
            result = cursor.fetchone()
            return result[0] > 0  # Trả về True nếu có ít nhất 1 bản ghi
        except Exception as e:
            print(f"❌ Lỗi khi kiểm tra mã phòng: {e}")
            return False
        finally:
            cursor.close()

    def autocreat_new_makhachhang(self):
            # Truy vấn cơ sở dữ liệu để lấy mã khách hàng cao nhất
            query = "SELECT MAX(CAST(SUBSTRING(makh, 3, LEN(makh)) AS INT)) FROM khachhang"
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()

            # Nếu không có khách hàng nào, khởi tạo mã là KH001
            if result[0] is None:
                return "KH001"

            # Tăng mã khách hàng lên 1
            new_makh = result[0] + 1
            return f"KH{new_makh:03d}"  # Chuyển thành dạng KHxxx (ví dụ: KH002)

    def delete_room(self, maphong):
        cursor = self.connection.cursor()
        query = "DELETE FROM phong WHERE maphong = ?"
        try:
            cursor.execute(query, (maphong,))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi xóa phòng: {e}")
            return False

    def update_tranghthairoom(self, maphong):
        cursor = self.connection.cursor()
        query = """
              UPDATE phong 
              SET  trangthai=?

              WHERE maphong=?
          """
        try:
            data_room=("ĐANG THUÊ",maphong)
            cursor.execute(query, data_room)
            self.connection.commit()

            if cursor.rowcount == 0:
                print("Không có dòng nào được cập nhật. Có thể mã khách hàng không tồn tại.")
                return False

            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi cập nhật phòng: {e}")
            return False

    def update_room(self, data_room):
        cursor = self.connection.cursor()
        query = """
            UPDATE phong 
            SET  loaiphong=?, giaphong=?, trangthai=?, tiennghi=?
       
            WHERE maphong=?
        """
        try:

            cursor.execute(query, data_room)
            self.connection.commit()

            if cursor.rowcount == 0:
                print("Không có dòng nào được cập nhật. Có thể mã khách hàng không tồn tại.")
                return False

            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi cập nhật phòng: {e}")
            return False

    def update_trangthai_phong(self, maphong, trangthai):
        cursor = self.connection.cursor()
        try:
            query = "UPDATE Phong SET trangthai = ? WHERE maphong = ?"
            cursor.execute(query, (trangthai, maphong))
            self.connection.commit()
        except Exception as e:
            print(f"❌ Lỗi cập nhật trạng thái phòng: {e}")
        finally:
            cursor.close()

    def autocreate_maphieuthue(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT TOP 1 maphieuthue FROM phieuthue ORDER BY maphieuthue DESC")
        last = cursor.fetchone()
        if last:
            num = int(last[0][2:]) + 1
        else:
            num = 1
        return f"PT{num:03d}"

    def autocreate_maphieudat(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT TOP 1 maphieudat FROM phieudat ORDER BY maphieudat DESC")
        last = cursor.fetchone()
        if last:
            num = int(last[0][2:]) + 1
        else:
            num = 1
        return f"PT{num:03d}"

    def create_phieuthue(self, maphieuthue, maphong, ngaynhan, ngaytra, tinhtrang):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO phieuthue (maphieuthue, maphong, ngaynhan, ngaytra, tinhtrang)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (maphieuthue, maphong, ngaynhan, ngaytra, tinhtrang))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi tạo phiếu thuê: {e}")
            return False
    def creat_phieudat(self, maphieudat, maphong,ngaydat, ngaynhan, ngaytra, trangthai):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO phieudat (maphieudat, maphong,ngaydat,ngaynhan, ngaytra, trangthai)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(query, (maphieudat, maphong,ngaydat, ngaynhan, ngaytra, trangthai))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi tạo phiếu thuê: {e}")
            return False

    def add_ct_phieuthue(self, maphieuthue, makh):
        cursor = self.connection.cursor()
        query = "INSERT INTO chitietphieuthuephong (maphieuthue, makh) VALUES (?, ?)"
        try:
            cursor.execute(query, (maphieuthue, makh))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thêm vào chitietphieuthuephong: {e}")
            return False
    def add_ct_phieudat(self, maphieudat, makh):
        cursor = self.connection.cursor()
        query = "INSERT INTO chitietphieudatphong (maphieudat, makh) VALUES (?, ?)"
        try:
            cursor.execute(query, (maphieudat, makh))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Lỗi khi thêm vào chitietphieudatphong: {e}")
            return False

    def get_phieuthue(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM phieuthue")
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phiếu thuê:", e)
            return []

    def get_chitietphieuthue(self,maphong):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT kh.makh, kh.hoten, pt.ngaynhan, pt.ngaytra
                FROM phieuthue pt
                JOIN chitietphieuthuephong ctpt ON pt.maphieuthue = ctpt.maphieuthue
                JOIN khachhang kh ON ctpt.makh = kh.makh
                WHERE pt.tinhtrang LIKE N'ĐANG THUÊ' AND pt.maphong=?
            """
            cursor.execute(query, (maphong,))

            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phiếu thuê:", e)
            return []

    def get_chitietphieudat(self, maphieudat):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT kh.makh, kh.hoten, kh.gioitinh, kh.quoctich, kh.cccd, kh.sdt, kh.diachi 
                FROM phieudat pd
                JOIN chitietphieudatphong ctpd ON pd.maphieudat = ctpd.maphieudat
                JOIN khachhang kh ON ctpd.makh = kh.makh
                WHERE pd.maphieudat = ?
            """
            cursor.execute(query, (maphieudat,))
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phiếu thuê:", e)
            return []

    def checkout_room(self, maphieuthue, maphong):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE phieuthue SET tinhtrang = N'ĐÃ TRẢ' WHERE maphieuthue = ?", (maphieuthue,))

            cursor.execute("UPDATE phong SET trangthai = N'TRỐNG' WHERE maphong = ?", (maphong,))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print("Lỗi khi trả phòng:", e)
            return False

    def get_maphieuthue_by_room(self, maphong):
        cursor = self.connection.cursor()
        query = "SELECT maphieuthue FROM phieuthue WHERE maphong = ? AND tinhtrang LIKE N'ĐANG THUÊ'"
        try:
            cursor.execute(query, (maphong,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Trả về maphieuthue của phiếu thuê đang hoạt động
            else:
                return None  # Không có phiếu thuê nào đang hoạt động cho phòng này
        except pyodbc.Error as e:
            print(f"Lỗi khi lấy maphieuthue: {e}")
            return None

    def find_phieutdat(self, maphieudat):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM phieudat WHERE maphieudat = ?"
            cursor.execute(query, (maphieudat,))
            return cursor.fetchall()
        except Exception as e:
            print("Lỗi khi lấy dữ liệu phiếu đặt:", e)
            return []

    def nhan_phong_tu_phieudat(self, maphieudat):
        try:
            cursor = self.connection.cursor()

            # Lấy thông tin phiếu đặt
            cursor.execute("SELECT maphong, ngaynhan, ngaytra FROM phieudat WHERE maphieudat = ?", (maphieudat,))
            row = cursor.fetchone()
            if not row:
                print("Không tìm thấy phiếu đặt")
                return False

            maphong, ngaynhan, ngaytra = row
            from datetime import datetime
            maphieuthue = "PT" + datetime.now().strftime("%Y%m%d%H%M%S")

            # Thêm vào phieuthue
            cursor.execute("""
                INSERT INTO phieuthue (maphieuthue, maphong, ngaynhan, ngaytra, tinhtrang)
                VALUES (?, ?, ?, ?, N'ĐANG THUÊ')
            """, (maphieuthue, maphong, ngaynhan, ngaytra))

            # Copy khách từ chitietphieudat
            cursor.execute("""
                INSERT INTO chitietphieuthuephong (maphieuthue, makh)
                SELECT ?, makh FROM chitietphieudatphong WHERE maphieudat = ?
            """, (maphieuthue, maphieudat))

            # Cập nhật trạng thái phiếu đặt
            cursor.execute("""
                UPDATE phieudat SET trangthai = N'ĐÃ NHẬN' WHERE maphieudat = ?
            """, (maphieudat,))
            cursor.execute("""
                UPDATE phong SET trangthai = N'ĐANG THUÊ' WHERE maphong = ?
            """, (maphong,))
            self.connection.commit()
            print("Nhận phòng thành công!")
            return True

        except Exception as e:
            print("Lỗi khi nhận phòng:", e)
            self.connection.rollback()
            return False

    def huyphieudat(self, maphieudat):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE phieudat SET trangthai = N'ĐÃ HỦY' WHERE maphieudat = ?
            """, (maphieudat,))
            self.connection.commit()
            print("Hủy phiếu đặt thành công!")
            return True
        except Exception as e:
            print("Lỗi khi hủy phiếu đặt:", e)
            self.connection.rollback()
            return False

    def lay_ds_khach_tu_phieudat(self, maphieudat):
        cursor = self.connection.cursor()
        cursor.execute("SELECT makh FROM chitietphieudatphong WHERE maphieudat = ?", (maphieudat,))
        return [row[0] for row in cursor.fetchall()]


