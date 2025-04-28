import sys
import copy
import time
import os
import re  
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QFrame, QScrollArea, QDesktopWidget, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from functools import partial
from datetime import datetime
import pyodbc
import random

LIGHTGREEN_HEX = QColor("lightgreen").name()   # '#90ee90'

rooms = []
#Format #new_room = Room(room_label.text(), "Thường", "100", "None",fake_status,"2025-03-25")
customer = [["Nguyễn Văn A","123456789"],
            ["Nguyễn Văn B","987654"]]
house = []

class DataBase:
    def __init__(self):
        self.connection = None
        self.connect()
    def connect(self):
        try:
            server = r"DESKTOP-5P464VF\MSSQLSERVER2022"
            database = "HotelManagement"
            username = "hotel_user"
            password = "1234"

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
    def write_dtb(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT maphong, loaiphong, giaphong, trangthai, tiennghi FROM phong")
        # Lấy tất cả dòng dữ liệu
        rows = cursor.fetchall()
        data = []
        for row in rows:
            house.append(list(row))  # Chuyển mỗi dòng thành một danh sách và thêm vào mảng
        # In mảng 2 chiều
        
        for row in house:
            
            print(row)
            
    def update_dtb(self,maphong,new_maphong,loaiphong,giaphong,trangthai,tiennghi):
        print()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM phong WHERE maphong = ?", (maphong,))
        row = cursor.fetchone()

        if row:
    # 3. Lấy dữ liệu dòng (row)
            # 4. UPDATE dòng đó
            cursor.execute("""
            UPDATE phong
            SET loaiphong = ?, giaphong = ?, trangthai = ?, tiennghi = ?
            WHERE maphong = ?
""", (loaiphong, giaphong, trangthai, tiennghi, maphong))


            self.connection.commit()
            print("Cập nhật thành công!")

        else:
            print("Không tìm thấy phòng!")

    def add_dtb(self,maphong,loaiphong,giaphong,trangthai,tiennghi):
        cursor = self.connection.cursor()
        sql = "INSERT INTO phong (maphong, loaiphong, giaphong, trangthai, tiennghi) VALUES (?, ?, ?, ?, ?)"
        data = (maphong, loaiphong, giaphong, trangthai, tiennghi)
        # Thực thi câu lệnh
        cursor.execute(sql, data)
        self.connection.commit()
    def delete_dtb(self,maphong):
        cursor = self.connection.cursor()
        cursor.execute("SELECT madatphong FROM datphong WHERE maphong = ?", (maphong,))
        madatphong_value = cursor.fetchone()
        result = str(madatphong_value).strip("()").replace(",", "")
        print(result)
        # Kiểm tra xem có kết quả không
        if madatphong_value:
            cursor.execute("DELETE FROM hoadon WHERE madatphong = ?", (result,))
            self.connection.commit()
            cursor.execute("DELETE FROM datphong WHERE maphong = ?", (maphong,))
            self.connection.commit()
            cursor.execute("DELETE FROM phong WHERE maphong = ?", (maphong,))
            self.connection.commit()

        else:
            print("Không tìm thấy giá trị madatphong cho maphong đã cho.")
        
    def update_status(self,maphong,trangthai):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM phong WHERE maphong = ?", (maphong,))
        row = cursor.fetchone()
        if row:
            cursor.execute("""
            UPDATE phong
            SET trangthai = ?
            WHERE maphong = ?
""", (trangthai))
            
    def close(self):
        if self.connection:
            self.connection.close()
db = DataBase()  # Kết nối tới cơ sở dữ liệu
db.write_dtb()   # In dữ liệu từ bảng phong

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def validate_date(s):
    try:
        # Parse theo format ngày-tháng-năm
        date = datetime.strptime(s, "%d-%m-%Y")
    except ValueError:
        return False, "Sai định dạng, phải là DD-MM-YYYY với ngày/tháng đủ 2 chữ số."

    day, month, year = date.day, date.month, date.year

    # Kiểm tra tháng
    if not (1 <= month <= 12):
        return False, f"Tháng {month} không hợp lệ. Phải từ 1 đến 12."

    # Xác định số ngày tối đa của tháng
    if month == 2:
        max_day = 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31

    # Kiểm tra ngày
    if not (1 <= day <= max_day):
        if month == 2 and day == 29:
            return False, f"Năm {year} không phải năm nhuận, tháng 2 chỉ có {max_day} ngày."
        return False, f"Ngày {day} không hợp lệ với tháng {month}."

    return True, "Hợp lệ."


def find_dup(maph):
    for room in rooms:
        if room.room_id == maph:
            return room
    return False 

def is_float(s):
  try:
    float(s)
    return True
  except ValueError:
    return False 

class Customer:
    def __init__(self, room_id, name):
        self.room_id = room_id
        self.name = name

    def __str__(self):
        return f"room_id: {self.room_id}, Tên: {self.name}"


class Room:
    def __init__(self, room_id, room_type, price, amenities, status, date):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.amenities = amenities
        self.status = status
        self.customer_list = []  # List to store customers
        self.date = date

    def add_customer(self, customer):
        """Add a customer to the room."""
        self.customer_list.append(customer)

    def remove_customer(self, room_id):
        """Remove a customer from the room using room_id."""
        self.customer_list = [c for c in self.customer_list if c.room_id != room_id]

    def list_customers(self):
        """Return a formatted string of all customers in the room."""
        if not self.customer_list:
            return "No customers in this room."
        return "\n".join(str(customer) for customer in self.customer_list)
    
    def update(self, room_id, room_type, price, amenities):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.amenities = amenities

    def __str__(self):
        return (f"Phòng {self.room_id}: {self.room_type}, Giá: {self.price} \n"
                f"Nội thất: {self.amenities} \nTrạng thái: {self.status} \n"
                f"Khách hàng:\n{self.list_customers()} \n"
                f"Ngày thuê: {self.date}"
                )

class HouseButton(QWidget):
    clicked = pyqtSignal(str, object)  # Emit room name and object

    def __init__(self, icon_path, label_text, rooms, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QVBoxLayout()

        # Create button
        self.button = QPushButton()
        self.button.setIcon(QIcon(QPixmap(icon_path)))  # Set house icon
        self.button.setIconSize(QSize(60, 60))
        self.button.setFixedSize(100, 100)

        # Create label
        self.label = QLabel(label_text)
        self.label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Connect button click signal to function with parameters
        self.button.clicked.connect(partial(self.on_button_clicked, label_text, rooms))

    def change_button_color(self, color: str):
        """Đổi *chỉ* màu nền, giữ nguyên border và các thuộc tính khác."""
        ss = self.button.styleSheet()

        if "background-color" in ss.lower():
            # thay giá trị cũ của background‑color
            ss = re.sub(
                r"background-color\s*:\s*[^;]+;",          # khớp dòng cũ
                f"background-color: {color};",             # thay thế
                ss,
                flags=re.I,
            )
        else:
            # chưa hề có background‑color → chèn thêm cuối chuỗi
            if ss and not ss.strip().endswith(";"):
                ss += ";"           # chắc chắn có dấu ';' trước khi nối
            ss += f"\nbackground-color: {color};"

        self.button.setStyleSheet(ss)

    def get_label_text(self):
        """Return the text of the label."""
        return self.label.text()

    def get_widget(self):
        """Return the entire HouseButton widget."""
        return self

    def on_button_clicked(self, room_name, rooms):
        """Handle button click and pass room name and rooms list."""
        self.clicked.emit(room_name, rooms)  # Emit signal with parameters

    def set_image(self, path):
        """Set a new image for the button."""
        self.button.setIcon(QIcon(QPixmap(path)))  # Set house icon

    def get_color(self) -> QColor:
        """Get the background color of the button."""
        # Kiểm tra xem self.button có còn tồn tại không
        if not self.button:
            #print("Button has been deleted or is invalid.")
            return QColor("white")  # Trả về màu mặc định nếu button đã bị xóa

        ss = self.button.styleSheet()

        # 1) Đọc màu trong styleSheet (nếu có)
        m = None  # Khởi tạo m trước
        if "background-color" in ss:
            # Khớp 'background-color: <value>;'
            m = re.search(r"background-color\s*:\s*([^;]+);", ss, re.I)
        
        if m:
            return QColor(m.group(1).strip())

        # 2) Fallback: màu từ palette (theme hệ điều hành)
        return self.button.palette().color(self.button.backgroundRole())
    def add_status_circle(self, color="green", size=15):
        """
    Thêm 1 nút hình tròn nhỏ ở góc trên bên trái của nút chính.

    Args:
        color (str): màu của hình tròn
        size (int): đường kính hình tròn (pixel)
    """

    # Tạo nút hình tròn
        self.status_circle = QPushButton(self)
        self.status_circle.setFixedSize(size, size)
    
    # Set style hình tròn và màu
        self.status_circle.setStyleSheet(f"""
        QPushButton {{
            background-color: {color};
            border-radius: {size // 2}px;
            border: 1px solid white;
        }}
    """)

    # Đặt vị trí góc trên trái (ví dụ cách 5px)
        margin = 5
        self.status_circle.move(margin, margin)

    # Không cho click vào nút tròn
        self.status_circle.setEnabled(False)
        self.status_circle.raise_()  # Đảm bảo nút tròn nổi lên trên nút chính


class AddRoomWindow(QWidget):
    send_signal = pyqtSignal(str)  # tạo signal gửi string
    def __init__(self,parent=None):
        super().__init__()
        self.parent = parent  # Store reference to parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Thêm phòng")
        self.setGeometry(500, 250, 450, 600)  # Set window size (450x600)

        layout = QGridLayout()

        # Set font size
        label_font = QFont("Arial", 14)  # Labels font
        input_font = QFont("Arial", 14)  # Input fields font
        button_font = QFont("Arial", 16, QFont.Bold)  # Button font

        # Labels and Input Fields
        self.room_id = QLabel("Nhập mã phòng:")
        self.room_id.setFont(label_font)
        self.input_room_id = QLineEdit()
        self.input_room_id.setFont(input_font)

        self.room_type = QLabel("Nhập loại phòng:")
        self.room_type.setFont(label_font)
        self.input_type = QComboBox()
        self.input_type.setFont(input_font)
        self.input_type.addItems(["Thường", "Vip"])

        self.room_price = QLabel("Nhập giá:")
        self.room_price.setFont(label_font)
        self.input_price = QLineEdit()
        self.input_price.setFont(input_font)

        self.room_amenities = QLabel("Nội thất:")
        self.room_amenities.setFont(label_font)
        self.input_amenities = QLineEdit()
        self.input_amenities.setFont(input_font)

        self.btn_add = QPushButton("Thêm phòng")
        self.btn_add.setFixedHeight(60)  # Bigger button
        self.btn_add.setFont(button_font)
        self.btn_add.clicked.connect(self.show_success_message)  # Connect button to function

        # Add widgets to layout
        layout.addWidget(self.room_id)
        layout.addWidget(self.input_room_id)
        layout.addWidget(self.room_type)
        layout.addWidget(self.input_type)
        layout.addWidget(self.room_price)
        layout.addWidget(self.input_price)
        layout.addWidget(self.room_amenities)
        layout.addWidget(self.input_amenities)
        layout.addWidget(self.btn_add)

        self.setLayout(layout)

        self.mode = 0

    def add_room(self,textbox_maph,textbox_loaiph,textbox_giaph,textbox_noithat,status,rooms):
        room_id = textbox_maph.text()
        room_type = textbox_loaiph.currentText()
        price = textbox_giaph.text()
        amenities = textbox_noithat.text()
        valid = False
        if (room_id!="") and (price!="") and (room_type!="") and (amenities!=""):
            valid = True
        if valid==True:
            if is_float(price)==False:                  
                #print("Giá không hợp lệ")
                self.mode = 1
            else:
                amenities = textbox_noithat.text()
                room_status = "Trống"
                if find_dup(room_id) == False:
                    new_room = Room(room_id, room_type, price, amenities,status,"")
                    rooms.append(new_room)
                    house.append([room_id,room_type,price,status,amenities,"",""])
                    db.add_dtb(room_id,room_type,price,status,amenities)
                    self.send_signal.emit("Nội dung từ Window A")
                    self.mode = 2
                else:
                    #print("Phong da ton tai")
                    self.mode = 3
                
        else:
            #print("Vui lòng nhập đầy đủ")
            self.mode = 4

    def show_success_message(self):
        self.add_room(self.input_room_id,self.input_type,self.input_price,self.input_amenities,"Trống",rooms)
        """ Show success message and close the window after a delay """
        self.msg = QMessageBox(self)  # Store in an instance variable
        self.msg.setWindowTitle("Thông báo")
        match self.mode:
            case 1:
                self.msg.setText("Giá không hợp lệ")
            case 2:
                self.msg.setText("Đã thêm")
            case 3:
                self.msg.setText("Phòng đã tồn tại")
            case 4:
                self.msg.setText("Vui lòng nhập đầy đủ")
        
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

        


        # Close the window after 1 second (1000 milliseconds)
        #QTimer.singleShot(1000, self.msg.close)
class DeleteRoomWindow(QWidget):
    send_signal = pyqtSignal(str)  # tạo signal gửi string
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Xóa phòng")
        self.setGeometry(500, 250, 450, 600)  # Set window size (450x600)

        layout = QGridLayout()

        # Set font size
        label_font = QFont("Arial", 14)  # Labels font
        input_font = QFont("Arial", 14)  # Input fields font
        button_font = QFont("Arial", 16, QFont.Bold)  # Button font

        # Labels and Input Fields
        self.room_id = QLabel("Nhập mã phòng:")
        self.room_id.setFont(label_font)
        self.input_room_id = QLineEdit()
        self.input_room_id.setFont(input_font)

        self.btn_add = QPushButton("Xóa phòng")
        self.btn_add.setFixedHeight(60)  # Bigger button
        self.btn_add.setFont(button_font)
        self.btn_add.clicked.connect(self.show_success_message)  # Connect button to function

        # Add widgets to layout
        layout.addWidget(self.room_id)
        layout.addWidget(self.input_room_id)
        layout.addWidget(self.btn_add)

        self.setLayout(layout)

        self.mode = 0


    def show_success_message(self):
        for i, row in enumerate(house):
            if (house[i][0]==self.input_room_id.text()):
                del house[i]
                for room in rooms:
                    if room.room_id == self.input_room_id.text():

                        
                        rooms.remove(room)
                        db.delete_dtb(self.input_room_id.text())
                        self.mode = 1
                        break
               
        
        """ Show success message and close the window after a delay """
        self.msg = QMessageBox(self)  # Store in an instance variable
        self.msg.setWindowTitle("Thông báo")
        match self.mode:
            case 0:
                self.msg.setText("Không tìm thấy phòng")
            case 1:
                self.msg.setText("Đã xóa")
        
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

        self.send_signal.emit("Nội dung từ Window B")

        # Close the window after 1 second (1000 milliseconds)
        #QTimer.singleShot(1000, self.msg.close)

class UpdateRoomWindow(QWidget):
    send_signal = pyqtSignal(str)  # tạo signal gửi string
    def __init__(self,selected_room,parent=None):
        super().__init__(parent)
        self.selected_room = selected_room #Cả cái room
        self.selected_room_id = self.selected_room.room_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cập nhật phòng")
        self.setGeometry(500, 250, 450, 600)  # Set window size (450x600)

        layout = QGridLayout()

        # Set font size
        label_font = QFont("Arial", 14)  # Labels font
        input_font = QFont("Arial", 14)  # Input fields font
        button_font = QFont("Arial", 16, QFont.Bold)  # Button font

        # Labels and Input Fields
        #self.room_id = QLabel("Nhập mã phòng:")
        #self.room_id.setFont(label_font)
        #self.input_room_id = QLineEdit()
        #self.input_room_id.setFont(input_font)

        self.room_type = QLabel("Nhập loại phòng:")
        self.room_type.setFont(label_font)
        self.input_type = QComboBox()
        self.input_type.setFont(input_font)
        self.input_type.addItems(["Thường", "Vip"])

        self.room_price = QLabel("Nhập giá:")
        self.room_price.setFont(label_font)
        self.input_price = QLineEdit()
        self.input_price.setFont(input_font)

        self.room_amenities = QLabel("Nội thất:")
        self.room_amenities.setFont(label_font)
        self.input_amenities = QLineEdit()
        self.input_amenities.setFont(input_font)

        self.btn_add = QPushButton("Cập nhật")
        self.btn_add.setFixedHeight(60)  # Bigger button
        self.btn_add.setFont(button_font)
        self.btn_add.clicked.connect(self.show_success_message)  # Connect button to function

        # Add widgets to layout
        #layout.addWidget(self.room_id)
        #layout.addWidget(self.input_room_id)
        layout.addWidget(self.room_type)
        layout.addWidget(self.input_type)
        layout.addWidget(self.room_price)
        layout.addWidget(self.input_price)
        layout.addWidget(self.room_amenities)
        layout.addWidget(self.input_amenities)
        layout.addWidget(self.btn_add)

        self.setLayout(layout)
        
    def update_room(self,textbox_loaiph,textbox_giaph,textbox_noithat):
        self.mode = 0
        #room_id = textbox_maph.text()
        room_type = textbox_loaiph.currentText()
        price = textbox_giaph.text()
        amenities = textbox_noithat.text()
        valid = False
        if (price!="") and (room_type!="") and (amenities!=""):
            valid = True
        if valid==True:
            if is_float(price)==False:                  
                #print("Giá không hợp lệ")
                self.mode = 1
            else:
                if find_dup(self.selected_room_id)!=False: #Tìm thấy
                    for item in rooms:
                        if self.selected_room_id == item.room_id:
                            self.mode = 2
                            break
                    if self.selected_room_id == self.selected_room_id:
                        self.mode = 3
                    if self.mode !=2:
                        for index, room in enumerate(house):
                            if (room[0]==self.selected_room_id):
                                #room[0] = room_id
                                room[1] = room_type
                                room[3] = price
                                room[4] = amenities  
                        sec_room = find_dup(self.selected_room_id)
                        sec_room.update(self.selected_room_id, room_type, price, amenities)         
                        self.send_signal.emit("")

                        db.update_dtb(self.selected_room_id,self.selected_room_id,room_type,price,'Trống',"None")
                        self.mode = 3

                else:
                    #print("Không tìm thấy "+self.selected_room_id)
                    self.mode = 4
                
        else:
            #print("Vui lòng nhập đầy đủ")
            self.mode = 5

    def show_success_message(self):
        self.update_room(self.input_type,self.input_price,self.input_amenities)
        """ Show success message and close the window after a delay """
        self.msg = QMessageBox(self)  # Store in an instance variable
        self.msg.setWindowTitle("Thông báo")
        match self.mode:
            case 1:
                self.msg.setText("Giá không hợp lệ")
            case 2:
                self.msg.setText("Trùng Id")
            case 3:
                self.msg.setText("Đã cập nhật")
            case 4:
                self.msg.setText("Không tìm thấy")
            case 5:
                self.msg.setText("Vui lòng nhập đầy đủ")
        
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

class ScheduleWindow(QWidget):
    send_signal = pyqtSignal(str)  # tạo signal gửi string
    def __init__(self,selected_room,parent=None):
        super().__init__(parent)
        self.selected_room = selected_room #Cả cái room

        self.selected_room_id = self.selected_room.room_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Thêm lịch bảo trì")
        self.setGeometry(500, 250, 450, 600)  # Set window size (450x600)

        layout = QGridLayout()

        # Set font size
        label_font = QFont("Arial", 14)  # Labels font
        input_font = QFont("Arial", 14)  # Input fields font
        button_font = QFont("Arial", 16, QFont.Bold)  # Button font

        # Labels and Input Fields
        self.room_id = QLabel("Nội dung:")
        self.room_id.setFont(label_font)
        self.input_room_id = QLineEdit()
        self.input_room_id.setFont(input_font)

        self.room_type = QLabel("Ngày thực hiện")
        self.room_type.setFont(label_font)
        self.input_type= QLineEdit()
        self.input_type.setFont(input_font)

        self.btn_add = QPushButton("Thêm")
        self.btn_add.setFixedHeight(60)  # Bigger button
        self.btn_add.setFont(button_font)
        self.btn_add.clicked.connect(self.show_success_message)  # Connect button to function

        # Add widgets to layout
        layout.addWidget(self.room_id)
        layout.addWidget(self.input_room_id)
        layout.addWidget(self.room_type)
        layout.addWidget(self.input_type)
        layout.addWidget(self.btn_add)

        self.setLayout(layout)

        self.mode = 0
    def add_schedule(self):

            print()


    def show_success_message(self):
            print()

   

class HotelManagementApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()  

    def initUI(self):

        self.setWindowTitle('Quản lý khách sạn')
        self.resize(1568, 728)
        
        # Layout chính
        main_layout = QVBoxLayout(self)
        
        # Tiêu đề
        title_label = QLabel('QUẢN LÝ PHÒNG')
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; text-align: center;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        content_layout = QHBoxLayout()
        
        # Sidebar
        sidebar_layout = QVBoxLayout()
        buttons = ['Quản lý phòng', 'Thanh toán', 'Thuê phòng', 'Khách hàng', 'Nhân viên']
        for btn_text in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(271, 131)
            button.setStyleSheet("font-size: 18px; font-weight: bold;")
            sidebar_layout.addWidget(button)
        sidebar_layout.addStretch()
        
        # Danh sách phòng
        room_group = QGroupBox('Danh sách phòng')
        room_group.setStyleSheet("font-size: 18px; font-weight: bold;")
        room_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        
        search_label = QLabel('Tìm kiếm theo :')
        search_label.setStyleSheet("font-size: 16px;")
        self.search_combo = QComboBox()
        self.search_combo.setStyleSheet("font-size: 16px;")
        self.search_combo.addItems(['Số phòng', 'Loại phòng'])
        self.search_input = QLineEdit()
        self.search_input.setStyleSheet("font-size: 16px;")



        self.search_input.textChanged.connect(self.on_text_changed)
        

        search_button = QPushButton('Tìm kiếm')
        search_button.setStyleSheet("font-size: 16px;")
        show_all_button = QPushButton('Xem tất cả')
        show_all_button.setStyleSheet("font-size: 16px;")
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_combo)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(show_all_button)
        
        self.room_frame = QFrame()
        self.room_scroll = QScrollArea()
        self.room_scroll.setWidgetResizable(True)
        self.room_frame = QWidget()
        self.room_grid = QGridLayout()
        self.room_grid.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.room_frame.setLayout(self.room_grid)
        self.room_frame.setStyleSheet("background-color: #ffffff;")
        self.room_scroll.setWidget(self.room_frame)   
        index = 0
        self.num_selected = 0
        icon_path1 = os.path.join(os.path.expanduser("~"), "Documents", "icons", "house_icon.png")
        icon_path2 = os.path.join(os.path.expanduser("~"), "Documents", "icons", "vip_icon.png")

        self.house_btn_array: list[HouseButton] = []

        def add_house_button(btn: HouseButton) -> None:
            if btn not in self.house_btn_array:
                self.house_btn_array.append(btn)
        
        for index, h in enumerate(house):
            # ----- tạo nút & Room -----------------------------
            if h[1] == "Thường":
                house_button = HouseButton(icon_path1, h[0], rooms)
            else:
                house_button = HouseButton(icon_path2, h[0], rooms)

            new_room = Room(h[0], h[1], h[2], h[4], h[3], "2025")
           #def __init__room_id, room_type, price, amenities, status, date):

            rooms.append(new_room)

            # ----- tô màu trạng thái --------------------------
            if new_room.status == "Đang sử dụng":
                house_button.change_button_color("lightblue")
            if new_room.room_id == rooms[0].room_id:
                house_button.change_button_color("lightgreen")

            # ----- connect nút với slot -----------------------
            add_house_button(house_button)
            if new_room.status =="Bảo trì":
                house_button.add_status_circle(color="lime", size=15)
            house_button.clicked.connect(
                partial(self.on_room_button_clicked, house_button, new_room.room_id, rooms)
                #   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #   Đóng băng  ➜  btn               room_number       rooms
            )

            # ----- đặt widget vào lưới ------------------------
            self.room_grid.addWidget(house_button.get_widget(), index // 6, index % 6)

        
        #print(rooms)
        room_layout.addLayout(search_layout)
        room_layout.addWidget(self.room_scroll)
        room_group.setLayout(room_layout)
        
        # Thông tin phòng
        info_group = QGroupBox('Thông tin phòng')
        info_group.setStyleSheet("font-size: 18px; font-weight: bold;")
        info_layout = QGridLayout()
        
        info_label_style = "font-size: 16px;"
        
        label_status = QLabel('Tình trạng')
        label_status.setStyleSheet(info_label_style)
        info_layout.addWidget(label_status, 0, 0)
        self.status_input = QComboBox()
        self.status_input.setStyleSheet("font-size: 16px;")
        self.status_input.addItems(['Đang sử dụng', 'Trống','Bảo trì','Đang dọn dẹp'])

        self.status_input.currentIndexChanged.connect(self.on_index_changed,self.num_selected)

        info_layout.addWidget(self.status_input, 0, 1)
        
        room_price = QLabel('Ngày thuê')
        room_price.setStyleSheet(info_label_style)
        info_layout.addWidget(room_price, 1, 0)
        self.date_input = QLineEdit()
        self.date_input.setStyleSheet("font-size: 16px;")
        info_layout.addWidget(self.date_input, 1, 1)

        self.date_input.editingFinished.connect(self.on_text_changed_2)
        
        label_tenant = QLabel('Người thuê')
        label_tenant.setStyleSheet(info_label_style)
        info_layout.addWidget(label_tenant, 2, 0, 1, 2, Qt.AlignLeft)
        
        self.tenant_table = QTableWidget(0, 3)  # Bảng hiển thị người thuê
        self.tenant_table.setStyleSheet("font-size: 16px;")
        self.tenant_table.setHorizontalHeaderLabels(['Tên', 'CMND','Giá thuê'])
        info_layout.addWidget(self.tenant_table, 3, 0, 1, 2)
        
        button_layout = QGridLayout()
        button_texts = ['Thêm mới', 'Xóa', 'Cập nhật', 'Lịch bảo trì']
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for pos, text in zip(positions, button_texts):
            button = QPushButton(text)
            button.setStyleSheet("font-size: 16px; width: 141px; height: 41px;")
            button_layout.addWidget(button, *pos)

            if (button.text()=="Thêm mới"):
                button.clicked.connect(self.add_room_button_clicked)
            if (button.text()=="Xóa"):
                button.clicked.connect(self.delete_room_button_clicked)
            if (button.text()=="Cập nhật"):
                button.clicked.connect(self.update_room_button_clicked)
            if (button.text()=="Lịch bảo trì"):
                button.clicked.connect(self.schedule_button_clicked)
        
        content_layout.addLayout(sidebar_layout, 1)
        content_layout.addWidget(room_group, 3)
        content_layout.addWidget(info_group, 2)
        
        info_group.setLayout(info_layout)
        info_layout.addLayout(button_layout, 4, 0, 1, 2)
        
        main_layout.addLayout(content_layout)
        
        self.setLayout(main_layout)
        self.child_window = None

        self.room_selected = rooms[0]


    def add_room_button_clicked(self):
        self.add_customer_window = AddRoomWindow()
        self.add_customer_window.show()
        self.add_customer_window.send_signal.connect(self.handle_signal)
    def update_room_button_clicked(self):
        self.update_customer_window = UpdateRoomWindow(self.room_selected)
        self.update_customer_window.show()
        self.update_customer_window.send_signal.connect(self.handle_signal)
    def delete_room_button_clicked(self):
        self.delete_customer_window = DeleteRoomWindow()

        self.delete_customer_window.send_signal.connect(self.handle_signal)
        self.delete_customer_window.show()

    def schedule_button_clicked(self):
        self.schedule_window = ScheduleWindow(self.room_selected)

        self.schedule_window.send_signal.connect(self.handle_signal)
        self.schedule_window.show()

    def repaint_lightgreen_to_white(self):
        LIGHTGREEN_HEX = QColor("lightgreen").name().lower()
        for btn in self.house_btn_array:        # dùng trực tiếp
            if btn.get_color().name().lower() == LIGHTGREEN_HEX:
                btn.change_button_color("white")
                #print("Repainted")

    def on_room_button_clicked(self,btn, room_number,rooms, checked=False):
        self.search_input.clearFocus()
        self.repaint_lightgreen_to_white()
        btn.change_button_color("lightgreen")
        
        for room in rooms:
            for item in self.house_btn_array:
                    if item.get_label_text() == room.room_id:
                        if room.status == "Trống":
                            item.change_button_color("white")
                        if room.status == "Đang thuê":
                            item.change_button_color("lightblue")
                        if item == btn:
                            item.change_button_color("lightgreen")
            if room.room_id == room_number:
                #print("room_status: " + str(room.status))  
                self.status_input.setCurrentText(str(room.status))
                self.date_input.setText(room.date)
                self.tenant_table.setRowCount(0)
                self.room_selected = room
                
                            
                #print(self.room_selected.room_id)
                for customer in room.customer_list:
                    row_position = self.tenant_table.rowCount()
                    self.tenant_table.insertRow(row_position)
                    self.tenant_table.setItem(row_position, 0, QTableWidgetItem(customer.name))
                    self.tenant_table.setItem(row_position, 1, QTableWidgetItem(customer.room_id))
                    self.tenant_table.setItem(row_position, 2, QTableWidgetItem(room.price))
                  
    def Refresh(self,room_grid,house_array):
        #Delete all the widget

        while room_grid.count():
            item = room_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)      # Gỡ khỏi layout
                widget.deleteLater()        # Xóa khỏi giao diện
        room_grid.update()

        sorted_house = sorted(house_array, key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
        #print("Sorted")
        index = 0
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Thư mục chứa file .py hiện tại
        icon_path1 = os.path.join(os.path.expanduser("~"), "Documents", "icons", "house_icon.png")
        icon_path2 = os.path.join(os.path.expanduser("~"), "Documents", "icons", "vip_icon.png")
        ######
        self.house_btn_array.clear()
        for index, h in enumerate(sorted_house):
            # ----- tạo nút & Room -----------------------------
            if h[1] == "Thường":
                house_button = HouseButton(icon_path1, h[0], rooms)
            else:
                house_button = HouseButton(icon_path2, h[0], rooms)

            new_room = Room(h[0], h[1], h[2], h[4], h[3], "2025")
            rooms.append(new_room)

            # ----- tô màu trạng thái --------------------------
            if new_room.status == "Đang sử dụng":
                house_button.change_button_color("lightblue")
            if new_room.room_id == rooms[0].room_id:
                house_button.change_button_color("lightgreen")

            if new_room.status =="Bảo trì":
                house_button.add_status_circle(color="lime", size=15)

            # ----- connect nút với slot -----------------------
            
            if house_button not in self.house_btn_array:
                self.house_btn_array.append(house_button)
            
            house_button.clicked.connect(
                partial(self.on_room_button_clicked, house_button, new_room.room_id, rooms)
                #   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                #   Đóng băng  ➜  btn               room_number       rooms
            )

            # ----- đặt widget vào lưới ------------------------
            self.room_grid.addWidget(house_button.get_widget(), index // 6, index % 6)
        self.room_selected = rooms[0]
        try:
            self.house_btn_array[0].change_button_color("lightgreen")
            #print(self.room_selected)  
        except IndexError:
            print("Oops! Index out of range.")
         

    def handle_signal(self, message):
        self.Refresh(self.room_grid,house)
        #print(f"Đã nhận: {message}")
    
    def on_text_changed(self, text):
        #Search
        house_copy = copy.deepcopy(house)
        #print(house_copy)
        filtered = [row for row in house_copy if self.search_input.text() in row[0]]
        #print(f"Text changed: {text}")
        if (self.search_input.text() !=""):
            self.Refresh(self.room_grid,filtered)
        else:
            self.Refresh(self.room_grid,house)

    def on_index_changed(self, index):
        #print(f"Selected index: {index}, Value: {self.status_input.itemText(index)}")
        #Set Status
        if self.status_input.hasFocus():
            #print("Focusing")
            did = False
            for room in rooms:
                if room.room_id == self.room_selected.room_id:
                    room.status = self.status_input.itemText(index)
                    did = True
            if (did == False): 
                print("room_id: " + str(room.room_id) + " and " + str(self.room_selected.room_id))

            for i, row in enumerate(house):
                if (house[i][0]==self.room_selected.room_id):
                    house[i][3] = self.status_input.itemText(index)
                    db.update_status(self.room_selected.room_id,self.status_input.itemText(index))
                    #print("Set status")
            self.Refresh(self.room_grid,house)

    def on_text_changed_2(self):
        #Set date
            text = self.date_input.text()
            for room in rooms:
                if room.room_id == self.room_selected.room_id:
                    room.date = text
            for i, row in enumerate(house):
                if (house[i][0]==self.room_selected.room_id):
                    house[i][5] = text
            self.Refresh(self.room_grid,house)

    def open_window(self):
        self.child_window = ChildWindow()
        self.child_window.show()

    def closeEvent(self, event):
        print("Cửa sổ đã đóng")
        db.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HotelManagementApp()
    window.show()
    sys.exit(app.exec_())
    app.exec_()