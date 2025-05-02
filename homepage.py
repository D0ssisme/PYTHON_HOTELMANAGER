from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QHeaderView
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from QLKH.database import DataBase

from PyQt5.QtWidgets import QPushButton
from functools import partial


from PyQt5.QtWidgets import QToolButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon


from QLNV.database_staff import DataBaseStaff

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAbstractItemView



class mainui(QMainWindow):
    def __init__(self,username,password):
        super().__init__()
        self.selected_button = None  # Lưu nút đang được chọn

        uic.loadUi('homepage.ui', self)  # Load trực tiếp file .ui

        # Gọi các hàm xử lý hoặc style sau khi load UI
        self.applyStylesheet()
        self.db = DataBase()
        self.db_staff = DataBaseStaff()
        self.db.connection = None
        self.db.connect()

        self.main_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.main))
        self.phieuthue_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.phieuthue))
        self.phieudatphong_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.phieudat))
        self.room_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.room))
        self.report_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.report))
        self.staff_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.staff))
        self.customer_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.customer))
        self.bill_btn.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.bill))
        self.main_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.main))
        self.room_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.room))
        self.report_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.report))
        self.staff_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.staff))
        self.customer_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.customer))
        self.bill_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.bill))
        self.phieuthue_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.phieuthue))
        self.phieudatphong_btn2.clicked.connect(lambda: self.widget_page.setCurrentWidget(self.phieudat))


        self.logout_btn2.clicked.connect(self.logout)
        self.logout_btn.clicked.connect(self.logout)
        self.deleteroom_button.clicked.connect(self.delete_room)
        self.username=username
        self.password=password
        self.user_btn2.clicked.connect(lambda: self.open_edituserdialog(self.username, self.password))
        self.user_btn1.clicked.connect(lambda: self.open_edituserdialog(self.username,self.password))
        self.user_btn3.clicked.connect(lambda: self.open_edituserdialog(self.username,self.password))
        self.username_input.setText(username)
        self.selectoption_combobox.addItems(["Tất Cả", "mã khách hàng"])
        self.loc_phieuthue.addItems(["Tất Cả", "mã khách hàng"])
##############################################################################
                    #khách hàng
        self.addcustomer_button.clicked.connect(self.open_addcustomer_dialog)
        self.editcustomer_button.clicked.connect(self.open_editcustomer_dialog)
        self.checkcustomer_button.clicked.connect(self.open_detailcustomerdialog)
        self.deletecustomer_button.clicked.connect(self.open_deletecustomer)
        self.customer_table.verticalHeader().setVisible(False)
        self.customer_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.customer_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.phieuthue_tableview.verticalHeader().setVisible(False)
        self.phieuthue_tableview.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.phieuthue_tableview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.khachthue_tableview.verticalHeader().setVisible(False)
        self.khachthue_tableview.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.khachthue_tableview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.refresh_button.clicked.connect(self.search_tablecustomer)
        self.loaddata_tablecustomer()

##############################################################################
        # phòng
        self.addroom_button.clicked.connect(self.open_addroom_diaglog)
        maphong = self.maphong_output.text()
        self.editroom_button.clicked.connect(lambda: self.open_editroom_dialog(self.maphong_output.text()))
        self.locloaiphong_combobox.addItems(["TẤT CẢ","ĐƠN", "ĐÔI", "VIP"])
        self.loctrangthai_combobox.addItems(["TẤT CẢ","TRỐNG", "ĐANG THUÊ","ĐANG DỌN DẸP"])
        self.loc_btn.clicked.connect(self.search_room)
        self.tinhtrang_output.setReadOnly(True)
        self.loaiphong_output.setReadOnly(True)
        self.ngaythue_output.setReadOnly(True)
        self.load_rooms()
        self.loaddata_phieuthue()
        self.btn_check.clicked.connect(lambda : self.open_thuephong_dialog(self.maphong_output.text()))
        self.btn_checkout.clicked.connect(lambda :self.checkout(self.maphong_output.text()))
        self.addphieudat_btn.clicked.connect(self.open_datphong_dialog)
        self.phieudat_tableview.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.phieudat_tableview.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.phieudat_tableview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.phieudat_tableview.verticalHeader().setVisible(False)

        self.nhanphong_btn.clicked.connect( self.open_nhanphong_dialog)
        self.huyphieudat_btn.clicked.connect(self.cancel_nhanphong_dialog)

        ##############################################################################
        # phiếu thuê

        self.locphieuthue_btn.clicked.connect(self.search_tablephieuthue)
        self.loaddata_phieudattableview()
        self.locphieudat_combobox.addItems(["TẤT CẢ", "SỐ ĐIỆN THOẠI","CĂN CƯỚC CÔNG DÂN"])
        self.loc_phieuthue2.addItems(["ĐANG THUÊ", "ĐÃ TRẢ"])
        self.locphieudat_combobox2.addItems(["ĐANG CHỜ", "ĐÃ NHẬN","ĐÃ HỦY"])



###############################################################################
        # Nhân viên
        self.load_staff_data()
        self.addstaff_button.clicked.connect(self.open_addstaff_dialog)
        self.editstaff_button.clicked.connect(self.open_editstaff_dialog)
        self.deletestaff_button.clicked.connect(self.open_deletestaff)






######################################################
    #phiếu đặt phòng


    def loadwindow(self):
        self.load_rooms()
        self.loaddata_phieudattableview()
        self.loaddata_phieuthue()
        self.load_staff_data()
        self.loaddata_tablecustomer()
        self.show_room_info()

    def cancel_nhanphong_dialog(self):
        index = self.phieudat_tableview.currentIndex()
        if index.isValid():
            row = index.row()
            model = self.phieudat_tableview.model()
            trangthai = model.index(row, 5).data()

            if trangthai == "ĐÃ NHẬN":
                QMessageBox.warning(self, "CẢNH BÁO", "PHIẾU ĐẶT ĐÃ ĐƯỢC XÁC NHẬN")
                return
            if trangthai == "ĐÃ HỦY":
                QMessageBox.warning(self, "CẢNH BÁO", "PHIẾU ĐẶT ĐÃ BỊ HỦY TRƯỚC ĐÓ")
                return

            maphieudat = model.index(row, 0).data()

            # ✅ Hỏi xác nhận hủy
            reply = QMessageBox.question(
                self,
                "Xác nhận hủy",
                f"Bạn có chắc chắn muốn hủy phiếu đặt [{maphieudat}] không?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                if self.db.huyphieudat(maphieudat):
                    QMessageBox.information(self, "Thành công", "Đã hủy phiếu đặt.")
                    self.loadwindow()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể hủy phiếu đặt.")
            else:
                # Người dùng chọn No
                return
        else:
            QMessageBox.warning(self, "CẢNH BÁO", "VUI LÒNG CHỌN PHIẾU ĐẶT!")

    def open_nhanphong_dialog(self):

        index = self.phieudat_tableview.currentIndex()
        if index.isValid():
            row = index.row()
            model = self.phieudat_tableview.model()
            trangthai=model.index(row,5).data()
            if(trangthai=="ĐÃ NHẬN"):
                QMessageBox.warning(self,"CẢNH BÁO","PHIẾU ĐẶT ĐÃ ĐƯỢC XÁC NHẬN")
                return
            if (trangthai == "ĐÃ HỦY"):
                QMessageBox.warning(self, "CẢNH BÁO", "PHIẾU ĐẶT ĐÃ ĐƯỢC BỊ HỦY")
                return
            maphieudat = model.index(row, 0).data()  # 0 là số thứ tự cột bạn muốn lấy
            from QLPhong.nhanphong_dialog import nhanphong_dialog
            dialog = nhanphong_dialog(maphieudat)
            dialog.exec_()
            self.loadwindow()

        else :
            QMessageBox.warning(self,"CẢNH BÁO ","VUI LÒNG CHỌN PHIẾU ĐẶT ! ")
            return


    def open_datphong_dialog(self):
        try:
            from QLPhong.datphong_dialog import datphong_dialog  # Điều chỉnh theo đúng thư mục bạn lưu file .py
            dialog = datphong_dialog()
            dialog.exec_()
            self.loaddata_phieudattableview()  # Hàm này bạn cần có để load lại bảng nhân viên
        except Exception as e:
            print("Lỗi khi mở dialog đặt phòng:", e)


    def loaddata_phieudattableview(self):

        phieudat = self.db.get_phieudat()

        # 2. Tạo model với số cột phù hợp
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Mã Phiếu Đặt", "Mã Phòng", "Ngày Đặt", "Ngày Nhận",
            "Ngày Trả", "Trạng Thái"
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in phieudat:
            row_items = [QStandardItem(str(cell)) for cell in row]
            self.model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.phieudat_tableview.setModel(self.model)

        # 5. Căn chỉnh cột cho đẹp
        header = self.phieudat_tableview.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)



###############################################################################################
                                    #đặt phòng


    def search_tablephieuthue(self):

        if  self.loc_phieuthue.currentText()=="Tất Cả":
            self.loaddata_phieuthue()
        else :
            self.close_table()
            maphong=self.loc_inputphieuthue.text()
            phieuthue = self.db.find_phieuthue(maphong)
            for row in phieuthue:
                row_items = [QStandardItem(str(cell)) for cell in row]
                self.model.appendRow(row_items)
            if(maphong==""):
                self.close_table()


    def checkout(self, maphong):
        # Lấy phiếu thuê đang hoạt động của phòng này
        if maphong=="":
            QMessageBox.warning(self,"CẢNH BÁO","VUI LÒNG CHỌN PHÒNG MUỐN TRẢ ")
            return

        maphieuthue = self.db.get_maphieuthue_by_room(maphong)
        if not maphieuthue:
            QMessageBox.warning(self, "LỖI", f"Không tìm thấy phiếu thuê đang hoạt động cho phòng {maphong}.")
            return

        # Xác nhận trước khi trả phòng
        reply = QMessageBox.question(
            self,
            "XÁC NHẬN TRẢ PHÒNG",
            f"Bạn có chắc chắn muốn trả phòng {maphong} (phiếu thuê {maphieuthue}) không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = self.db.checkout_room(maphieuthue, maphong)

            if success:
                QMessageBox.information(self, "THÀNH CÔNG", "Trả phòng thành công!")
                self.loadwindow()
            else:
                QMessageBox.critical(self, "LỖI", "Trả phòng thất bại. Vui lòng thử lại.")

    def open_thuephong_dialog(self,maphong):
        if maphong=="":
            QMessageBox.warning(self,"CẢNH BÁO ","VUI LÒNG CHỌN PHÒNG MUỐN THUÊ")
            return
        from QLPhong.thuephong_dialog import thuephong_dialog
        dialog = thuephong_dialog(maphong)


        dialog.exec_()
        self.load_rooms()
        self.loaddata_tablecustomer()
        self.loaddata_phieuthue()

    def loaddata_phieuthue(self):
        phieuthue = self.db.get_phieuthue()

        # 2. Tạo model với số cột phù hợp
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "MÃ PHIẾU THUÊ", "MÃ PHÒNG", 'NGÀY NHẬN', "NGÀY TRẢ", 'TÌNH TRẠNG'
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in phieuthue:
            row_items = []
            for cell in row:
                item = QStandardItem(str(cell))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Loại bỏ quyền chỉnh sửa
                row_items.append(item)
            self.model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.phieuthue_tableview.setModel(self.model)

        # 5. Căn chỉnh cột cho đẹp
        header = self.phieuthue_tableview.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    #############################################################################################
                                    #QUẢN LÍ PHÒNG

    def search_room(self):
        loaiphong_selected = self.locloaiphong_combobox.currentText()
        trangthai_selected = self.loctrangthai_combobox.currentText()

        all_rooms = self.db.get_room()

        filtered_rooms = []
        for room in all_rooms:
            match_loaiphong = (loaiphong_selected == "TẤT CẢ") or (room[1] == loaiphong_selected)
            match_trangthai = (trangthai_selected == "TẤT CẢ") or (room[3] == trangthai_selected)

            if match_loaiphong and match_trangthai:
                filtered_rooms.append(room)

        self.display_rooms(filtered_rooms)

    def display_rooms(self, room_data):
        layout = self.room_layout.layout()
        if layout is None:
            return

        # Xóa các nút cũ
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Thêm các nút mới từ room_data
        row = 0
        col = 0
        for room in room_data:
            button = QToolButton()
            button.setText(f"{room[0]}")
            button.setProperty("trangthai", room[3])  # Gán trạng thái vào property để dùng sau
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setFixedSize(110, 110)
            button.setIconSize(QSize(50, 50))

            # Set icon theo loại phòng
            if room[1] == "ĐƠN":
                button.setIcon(QIcon("image/đơn.svg"))
            elif room[1] == "ĐÔI":
                button.setIcon(QIcon("image/đôi.svg"))
            elif room[1] == "VIP":
                button.setIcon(QIcon("image/vip.svg"))

            # Style theo trạng thái
            if room[3] == "ĐANG THUÊ":
                button.setStyleSheet("""
                              QToolButton {
                                  font-size: 20px;
                                  font-weight: bold;
                                  background-color: #759f1e;
                              }
                          """)
            elif room[3] == "ĐANG DỌN DẸP":
                button.setStyleSheet("""
                    QToolButton {
                        font-size: 20px;
                        font-weight: bold;
                        background-color: #FFFF00;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QToolButton {
                        font-size: 20px;
                        font-weight: bold;
                    }
                """)

            # Bắt sự kiện click
            maphong = room[0]
            button.clicked.connect(lambda _, btn=button, maphong=maphong: self.on_room_button_clicked(btn, maphong))

            layout.addWidget(button, row, col)
            col += 1
            if col >= 8:
                col = 0
                row += 1

    def on_room_button_clicked(self, button, maphong):
        # Trả lại style cho nút đã chọn trước đó (nếu có)
        if self.selected_button:
            prev_trangthai = self.selected_button.property("trangthai")
            if prev_trangthai == "ĐANG THUÊ":
                self.selected_button.setStyleSheet("""
                    QToolButton {
                        font-size: 20px;
                        font-weight: bold;
                        background-color: #759f1e;
                    }
                """)
            elif prev_trangthai == "ĐANG DỌN DẸP":
                self.selected_button.setStyleSheet("""
                    QToolButton {
                        font-size: 20px;
                        font-weight: bold;
                        background-color: #FFFF00;
                    }
                """)

            else:
                self.selected_button.setStyleSheet("""
                    QToolButton {
                        font-size: 20px;
                        font-weight: bold;
                    }
                """)

        # Gán style có viền cho nút mới
        trangthai = button.property("trangthai")
        if trangthai == "ĐANG THUÊ":
            button.setStyleSheet("""
                QToolButton {
                    font-size: 20px;
                    font-weight: bold;
                    background-color: #759f1e;
                    border: 3px solid black;
                }
            """)
        elif trangthai == "ĐANG DỌN DẸP":
            button.setStyleSheet("""
                QToolButton {
                    font-size: 20px;
                    font-weight: bold;
                    background-color: #FFFF00;
                    border: 3px solid black;
                }
            """)
        elif trangthai == "BẢO TRÌ":
            button.setStyleSheet("""
                QToolButton {
                    font-size: 20px;
                    font-weight: bold;
                    background-color: #FFA07A;
                    border: 3px solid black;
                }
            """)
        else:
            button.setStyleSheet("""
                QToolButton {
                    font-size: 20px;
                    font-weight: bold;
                    border: 3px solid black;
                }
            """)

        # Cập nhật lại nút đã chọn
        self.selected_button = button

        # Hiển thị thông tin phòng
        self.show_room_info(maphong)

    def open_editroom_dialog(self, maphong):
        try:
            from QLPhong.editroom_dialog import editroomdialog
            dialog = editroomdialog(maphong)
            dialog.exec_()

            self.load_rooms()
            self.show_room_info(maphong)
        except Exception as e:
            print(f"Lỗi khi mở hộp thoại chỉnh sửa phòng: {e}")

    def open_addroom_diaglog(self):
        try:
            from QLPhong.addroom_dialog import addroomdialog
            dialog = addroomdialog()
            dialog.exec_()
            self.load_rooms()

        except Exception as e:
            print("Lỗi khi mở dialog thêm phòng", e)

    def load_rooms(self):
        layout = self.room_layout.layout()
        if layout is None:
            return

        # Xóa các nút cũ
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Lấy dữ liệu phòng
        room_data = self.db.get_room()
        room_data.sort(key=lambda x: int(x[0][1:]))  # Sắp xếp theo số trong mã phòng, ví dụ: P008 -> 8

        row = 0
        col = 0
        for room in room_data:
            button = QToolButton()
            button.setText(f"{room[0]}")  # Mã phòng
            button.setStyleSheet("""
                QToolButton {
                    font-size: 20px;
                    font-weight: bold;
                 
                }
            """)

            if room[1] == "ĐƠN":
                button.setIcon(QIcon("image/đơn.svg"))
            if room[1]=="VIP":
                button.setIcon(QIcon("image/vip.svg"))

            if room[1]=="ĐÔI":
                button.setIcon(QIcon("image/đôi.svg"))

            button.setIconSize(QSize(50 , 50))  # Kích thước icon
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Icon trên, text dưới
            button.setFixedSize(110, 110)  # Kích thước nút
            button.setProperty("trangthai", room[3])  # room[3] là trạng thái phòng

            button.clicked.connect(lambda _, b=button, m=room[0]: self.on_room_button_clicked(b, m))
            if room[3] == "ĐANG THUÊ":
                button.setStyleSheet("""
                                 QToolButton {
                                     background-color: #759f1e; 
                                     font-size: 20px;
                                 font-weight: bold;



                                 }
                             """)

            if room[3] == "ĐANG DỌN DẸP":
                button.setStyleSheet("""
                    QToolButton {
                        background-color: #FFFF00; /* Màu vàng */
                        font-size: 20px;
                    font-weight: bold;
                        
                        
                    
                    }
                """)




            # Căn giữa icon trong button

            # Thêm button vào layout
            layout.addWidget(button, row, col)

            col += 1
            if col >= 8:  # Tối đa 8 nút trên mỗi dòng
                col = 0
                row += 1
    def delete_room(self):
        maphong = self.maphong_output.text()

        if maphong=="":
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn xóa !")
            return

        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa phòng  {maphong}",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db.delete_room(maphong):
                self.load_rooms()
                QMessageBox.information(self, "Thành công", "Đã xóa phòng thành công!")


            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa phòng")

    def set_khachhang_table(self):
        # Thiết lập số cột
        self.khachthue_tableview.setColumnCount(2)

        # Thiết lập tiêu đề cột
        self.khachthue_tableview.setHorizontalHeaderLabels(["Mã Khách Hàng", "Tên Khách Hàng"])

        # Thiết lập chế độ kéo dãn cho các cột để chia đều không gian bảng
        header = self.khachthue_tableview.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # Hoặc nếu bạn muốn cột đầu hẹp hơn và cột thứ hai rộng hơn:
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Cột 1 tự động điều chỉnh theo nội dung
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # Cột 2 chiếm phần còn lại
    def show_room_info(self, maphong):

        # Tìm phòng theo mã
        room = self.db.find_room(maphong)
        chitietphieunhap = self.db.get_chitietphieuthue(maphong)

        # Kiểm tra nếu có dữ liệu trả về
        if room:
            room_tuple = room[0]  # Lấy tuple đầu tiên trong danh sách

            # In thông tin chi tiết phòng ra console
            print(f"Phòng được chọn: {maphong}")
            print(f"Thông tin chi tiết: {room_tuple}")
            self.maphong_output.setText(f"{room_tuple[0]}")
            self.maphong_output.setStyleSheet("font-weight: bold; font-size: 40px;")

            self.loaiphong_output.setText(f"{room_tuple[1]}")
            self.tinhtrang_output.setText(f"{room_tuple[3]}")
            if not chitietphieunhap:
                self.ngaythue_output.setText("")
                self.ngaytra_output.setText("")
                self.khachthue_tableview.setRowCount(0)  # Đặt số hàng là 0 để xóa tất cả dữ liệu



            if chitietphieunhap:
                self.khachthue_tableview.setColumnCount(2)
                self.khachthue_tableview.setHorizontalHeaderLabels(["Mã Khách Hàng", "Tên Khách Hàng"])

                # Thiết lập số hàng bằng số lượng khách hàng
                self.khachthue_tableview.setRowCount(len(chitietphieunhap))

                # Hiển thị tất cả khách hàng vào bảng
                for row, ctpn_tuple in enumerate(chitietphieunhap):
                    # Lấy thông tin khách thuê phòng
                    makh, hoten, ngaynhan, ngaytra = ctpn_tuple

                    # In ra để kiểm tra
                    print(f"Đang thêm khách hàng: {makh} - {hoten}")

                    # Thêm vào bảng
                    self.khachthue_tableview.setItem(row, 0, QtWidgets.QTableWidgetItem(makh))
                    self.khachthue_tableview.setItem(row, 1, QtWidgets.QTableWidgetItem(hoten))

                # Hiển thị thông tin ngày thuê và ngày trả từ khách hàng đầu tiên
                # (hoặc bạn có thể thay đổi logic này nếu cần)
                first_customer = chitietphieunhap[0]
                makh, hoten, ngaynhan, ngaytra = first_customer

                self.ngaythue_output.setText(f"{ngaynhan.strftime('%d/%m/%Y %H:%M')}")
                self.ngaytra_output.setText(f"{ngaytra.strftime('%d/%m/%Y %H:%M')}")

                # Thiết lập chế độ kéo dãn cho các cột
                header = self.khachthue_tableview.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)


            room_info = f"""
            Mã phòng: {room_tuple[0]}
            Loại phòng: {room_tuple[1]}
            Giá phòng: {room_tuple[2]}
            Trạng thái: {room_tuple[3]}
            Tiện nghi: {room_tuple[4]}
            """
            if (f"{room_tuple[3]}" == "TRỐNG"):
                self.btn_check.setEnabled(True)
                self.btn_checkout.setEnabled(False)
                self.btn_check.setText("THUÊ PHÒNG")
                self.btn_checkout.setText("TRẢ PHÒNG")


            elif (f"{room_tuple[3]}" == "ĐANG DỌN DẸP"):
                self.btn_check.setEnabled(False)
                self.btn_checkout.setEnabled(False)
                self.btn_check.setText("THUÊ PHÒNG")
                self.btn_checkout.setText("TRẢ PHÒNG")
            elif (f"{room_tuple[3]}" == "ĐANG THUÊ"):
                self.btn_check.setEnabled(False)
                self.btn_checkout.setEnabled(True)
                self.btn_check.setText("THUÊ PHÒNG")
                self.btn_checkout.setText("TRẢ PHÒNG")


        else:
            print(f"Không tìm thấy phòng với mã {maphong}")







        #######################################################################################3
                                        #CUSTOMER
    def open_detailcustomerdialog(self):
        from QLKH.detailcustomer_dialog import detailcustomer_dialog
        selected_indexes = self.customer_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            makh = self.customer_table.model().index(selected_index.row(), 0)
            hoten = self.customer_table.model().index(selected_index.row(), 1)
            gioitinh = self.customer_table.model().index(selected_index.row(), 2)
            quoctich = self.customer_table.model().index(selected_index.row(), 3)
            cccd = self.customer_table.model().index(selected_index.row(), 4)
            sdt = self.customer_table.model().index(selected_index.row(), 5)
            diachi = self.customer_table.model().index(selected_index.row(), 6)
            maphong = self.customer_table.model().index(selected_index.row(), 7)
            ngaynhan = self.customer_table.model().index(selected_index.row(), 8)
            ngaytra = self.customer_table.model().index(selected_index.row(), 9)

            value = makh.data()
            value1 = hoten.data()
            value2 = gioitinh.data()
            value3 = quoctich.data()
            value4 = cccd.data()
            value5 = sdt.data()
            value6 = diachi.data()
            value7 = maphong.data()
            value8 = ngaynhan.data()
            value9 = ngaytra.data()

            dialog = detailcustomer_dialog(value, value1, value2, value3, value4, value5, value6, value7, value8, value9)
            dialog.exec_()



    def search_tablecustomer(self):

        if  self.selectoption_combobox.currentText()=="Tất Cả":
            self.loaddata_tablecustomer()
        else :
            self.close_table()
            makh=self.loc_input.text()
            customers = self.db.find_customer(makh)
            for row in customers:
                row_items = [QStandardItem(str(cell)) for cell in row]
                self.model.appendRow(row_items)
            if(makh==""):
                self.close_table()



    def close_table(self):
        self.model.removeRows(0, self.model.rowCount())







    def loaddata_tablecustomer(self):

        customers = self.db.get_customers()

        # 2. Tạo model với số cột phù hợp
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([
            "Mã Khách Hàng", "Họ Tên", "Giới Tính", "Quốc Tịch",
            "CCCD", "SĐT", "Địa Chỉ", "Mã Phòng", "Ngày Nhận", "Ngày Trả"
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in customers:
            row_items = [QStandardItem(str(cell)) for cell in row]
            self.model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.customer_table.setModel(self.model)

        # 5. Căn chỉnh cột cho đẹp
        header = self.customer_table.horizontalHeader()
        for column in range(self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def open_deletecustomer(self):

        selected_indexes = self.customer_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            first_cell_index = self.customer_table.model().index(selected_index.row(), 0)
            value = first_cell_index.data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn xóa !")
            return


        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa khách hàng  {value}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db.delete_customer(value):
                self.loaddata_tablecustomer()
                QMessageBox.information(self, "Thành công", "Đã xóa khách hàng thành công!")


            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa khách hàng")


    def open_addcustomer_dialog(self):
        try:
            from QLKH.addcustomer_dialog import addcustomer_dialog
            dialog = addcustomer_dialog()
            dialog.exec_()
            self.loaddata_tablecustomer()
        except Exception as e:
            print("Lỗi khi mở dialog thêm khách hàng:", e)




    def open_editcustomer_dialog(self):
        from QLKH.editcustomer_dialog import editcustomer_dialog
        selected_indexes = self.customer_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            makh = self.customer_table.model().index(selected_index.row(), 0)
            hoten = self.customer_table.model().index(selected_index.row(), 1)
            gioitinh = self.customer_table.model().index(selected_index.row(), 2)
            quoctich = self.customer_table.model().index(selected_index.row(), 3)
            cccd = self.customer_table.model().index(selected_index.row(), 4)
            sdt = self.customer_table.model().index(selected_index.row(), 5)
            diachi = self.customer_table.model().index(selected_index.row(), 6)
            maphong = self.customer_table.model().index(selected_index.row(), 7)
            ngaynhan = self.customer_table.model().index(selected_index.row(), 8)
            ngaytra = self.customer_table.model().index(selected_index.row(), 9)



            value = makh.data()
            value1=hoten.data()
            value2=gioitinh.data()
            value3=quoctich.data()
            value4=cccd.data()
            value5=sdt.data()
            value6=diachi.data()
            value7=maphong.data()
            value8=ngaynhan.data()
            value9=ngaytra.data()

            dialog = editcustomer_dialog(value,value1,value2,value3,value4,value5,value6,value7,value8,value9)
            dialog.exec_()
            self.loaddata_tablecustomer()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn khách hàng muốn sửa !")
            return

    def open_edituserdialog(self, username, password):
        try:

            from QLKH.dialog_edituser import dialog_edituser
            dlg = dialog_edituser(username, password)
            dlg.update_completed.connect(self.logout_fast)


            dlg.exec_()  # Mở dialog sửa user
        except Exception as e:
            print("Lỗi khi mở dialog sửa user:", e)




    def logout(self):
        from login import loginui
        reply = QMessageBox.question(
            self, "Xác nhận đăng xuất",
            "Bạn có chắc chắn muốn đăng xuất?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Thông báo")
            msg_box.setText("Bạn đã đăng xuất thành công.")
            msg_box.setIcon(QMessageBox.Information)
            msg_box.exec_()

            # Ẩn cửa sổ chính và có thể hiện lại Login ở đây
            self.hide()
            self.login_window = QtWidgets.QMainWindow()
            self.login_ui = loginui()
            self.login_ui.setupUi(self.login_window)
            self.login_window.show()

    def logout_fast(self):
        from login import loginui
        self.hide()
        self.login_window = QtWidgets.QMainWindow()
        self.login_ui = loginui()
        self.login_ui.setupUi(self.login_window)
        self.login_window.show()





    def applyStylesheet(self):

        with open('QLKH/style.qss', 'r') as f:
            self.setStyleSheet(f.read())
            self.change_btn.click()
            style = """
                              QPushButton {
                                  background-color: #E0E0E0;
                                  border: none;
                                  padding:px;
                                  border-radius:10px;
                              }

                              QPushButton:hover {
                                  background-color: 		#D5D5D5;
                                      border-radius:10px;
                              }

                              QPushButton:focus {
                                  outline: none;
                                  border: none;
                                  background-color: 	#D5D5D5;
                                      border-radius:10px;
                              }
                           
                              """

            # Cặp nút: [(nút to, nút nhỏ), ...]
            self.menu_pairs = [
                (self.main_btn, self.main_btn2),
                (self.room_btn, self.room_btn2),
                (self.customer_btn, self.customer_btn2),
                (self.staff_btn, self.staff_btn2),
                (self.report_btn, self.report_btn2),
                (self.bill_btn, self.bill_btn2),
                (self.phieudatphong_btn, self.phieudatphong_btn2),
                (self.phieuthue_btn, self.phieuthue_btn2)


            ]

            # Gán style và setCheckable
            for btn1, btn2 in self.menu_pairs:
                btn1.setCheckable(True)
                btn2.setCheckable(True)
                btn1.setStyleSheet(style)
                btn2.setStyleSheet(style)





 #########################################################################################
                                    #NHÂN VIÊN


    def load_staff_data(self):
        # 1. Kết nối và lấy dữ liệu
        staffs = self.db_staff.get_staff()

        # 2. Tạo model với số cột phù hợp
        self.staff_model = QStandardItemModel()
        self.staff_model.setHorizontalHeaderLabels([
            "Mã NV", "Họ Tên", "Chức Vụ", "SĐT", "Ca Làm"
        ])

        # 3. Đổ dữ liệu từ SQL vào model
        for row in staffs:
            row_items = [QStandardItem(str(cell)) for cell in row]
            self.staff_model.appendRow(row_items)

        # 4. Gắn model vào QTableView
        self.staff_table.setModel(self.staff_model)
        self.staff_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.staff_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.staff_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.staff_table.verticalHeader().setVisible(False)

        # 5. Căn chỉnh cột cho đẹp
        header = self.staff_table.horizontalHeader()
        for column in range(self.staff_model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Stretch)

    def open_addstaff_dialog(self):
        try:
            from QLNV.addstaff_dialog import addstaff_dialog  # Điều chỉnh theo đúng thư mục bạn lưu file .py
            dialog = addstaff_dialog()
            dialog.exec_()
            self.load_staff_data()  # Hàm này bạn cần có để load lại bảng nhân viên
        except Exception as e:
            print("Lỗi khi mở dialog thêm nhân viên:", e)

    def open_editstaff_dialog(self):
        from QLNV.editstaff_dialog import editstaff_dialog

        selected_rows = self.staff_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            model = self.staff_table.model()

            manv = model.index(row, 0).data()
            hoten = model.index(row, 1).data()
            chucvu = model.index(row, 2).data()
            sdt = model.index(row, 3).data()
            calam = model.index(row, 4).data()

            print(f"manv: {manv}, hoten: {hoten}, chucvu: {chucvu}, sdt: {sdt}, calam: {calam}")

            dialog = editstaff_dialog(manv, hoten, chucvu, calam, sdt)
            dialog.exec_()
            self.load_staff_data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn nhân viên muốn chỉnh sửa!")

    def open_deletestaff(self):
        selected_indexes = self.staff_table.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            first_cell_index = self.staff_table.model().index(selected_index.row(), 0)
            manv = first_cell_index.data()
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn nhân viên muốn xóa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa nhân viên {manv}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            if self.db_staff.delete_staff(manv):
                self.load_staff_data()
                QMessageBox.information(self, "Thành công", "Đã xóa nhân viên thành công!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể xóa nhân viên.")

if __name__ == '__main__':
    app = QApplication([])
    user="123"
    password="29052005"
    window = mainui(user,password)
    window.show()
    app.exec_()
