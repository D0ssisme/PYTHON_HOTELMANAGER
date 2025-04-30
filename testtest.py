from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quản lý phòng")
        self.setGeometry(100, 100, 600, 400)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Tạo layout cho phần trái (nút phòng)
        self.grid_layout = QGridLayout()

        # Layout để hiển thị thông tin phòng bên phải
        self.info_layout = QVBoxLayout()
        self.room_info_label = QLabel("Thông tin phòng sẽ hiển thị tại đây", self)
        self.info_layout.addWidget(self.room_info_label)

        # Tạo layout chính
        main_layout = QHBoxLayout(self.main_widget)
        main_layout.addLayout(self.grid_layout, 1)
        main_layout.addLayout(self.info_layout, 2)

        # Danh sách phòng (một ví dụ)
        self.rooms = {
            "101": "Phòng 101: Giá 500k",
            "102": "Phòng 102: Giá 600k",
            "103": "Phòng 103: Giá 700k",
        }
        self.room_buttons = {}

        # Thêm các nút phòng vào layout
        self.add_room_buttons()

        self.show()

    def add_room_buttons(self):
        row = 0
        col = 0

        # Lặp qua danh sách phòng để tạo các nút và thêm vào grid layout
        for room_number, room_info in self.rooms.items():
            button = QPushButton(room_number)
            button.clicked.connect(self.show_room_info)
            button.setProperty("room_info", room_info)  # Lưu thông tin phòng trong thuộc tính
            self.room_buttons[room_number] = button
            self.grid_layout.addWidget(button, row, col)

            # Di chuyển đến vị trí tiếp theo trong grid layout
            col += 1
            if col > 2:  # Chuyển sang hàng mới khi đã có 3 nút trong một hàng
                col = 0
                row += 1

    def show_room_info(self):
        # Lấy thông tin phòng từ nút được bấm
        button = self.sender()
        room_info = button.property("room_info")
        self.room_info_label.setText(room_info)

    def add_new_room(self, room_number, room_info):
        # Thêm phòng mới vào danh sách và thêm nút vào layout
        self.rooms[room_number] = room_info
        self.add_room_buttons()  # Cập nhật lại các nút phòng

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
