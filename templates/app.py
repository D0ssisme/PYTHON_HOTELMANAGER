from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Cấu hình kết nối với SQL Server
server = r"DESKTOP-5P464VF\MSSQLSERVER2022"
database = "HotelManagement"
username = "manhdung2"
password = "29052005"

# Cấu hình thư mục lưu ảnh
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Kết nối tới SQL Server
def connect_to_db():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                          f'SERVER={server};'
                          f'DATABASE={database};'
                          f'UID={username};'
                          f'PWD={password}')
    return conn

# Kiểm tra định dạng file ảnh
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route để hiển thị form
@app.route('/')
def home():
    return render_template("index.html")

# Route xử lý form và upload ảnh
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    gender = request.form['gender']
    nationality = request.form['nationality']
    cccd = request.form['cccd']
    phone = request.form['phone']
    diachi = request.form['diachi']
    maphong = request.form['room_id']
    check_in_date = datetime.strptime(request.form['check_in_date'], "%Y-%m-%d").date()
    check_out_date = datetime.strptime(request.form['check_out_date'], "%Y-%m-%d").date()
    check_in_datetime = datetime.combine(check_in_date, datetime.now().time())
    check_out_datetime = datetime.combine(check_out_date, datetime.now().time())
    contact_info = request.form['contact_info']
    photo_url = None

    # Kiểm tra ảnh
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(filename)
            photo_url = filename

    # Kết nối CSDL
    conn = connect_to_db()
    cursor = conn.cursor()

    # Kiểm tra trùng ngày thuê với mã phòng
    query = "SELECT ngaynhan, ngaytra FROM dbo.phieuthue WHERE maphong = ?"
    cursor.execute(query, (maphong,))
    rows = cursor.fetchall()
    legal = True

    for row in rows:
        ngaynhan_datetime = row[0]
        ngaytra_datetime = row[1]
        ngaynhan_date = ngaynhan_datetime.date()
        ngaytra_date = ngaytra_datetime.date()

        if (check_in_date >= ngaynhan_date) or (check_in_date <= ngaynhan_date and check_out_date <= ngaytra_date):
            flash('Phòng này đã được thuê trong khoảng thời gian bạn yêu cầu. Vui lòng chọn phòng khác.', 'error')
            return redirect(url_for('home'))

    # Tạo mã phiếu thuê mới (PT001, PT002, ...)
    query = "SELECT maphieuthue FROM dbo.phieuthue ORDER BY maphieuthue DESC"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        last_code = rows[0][0]
        last_number = int(last_code[2:])
        new_code = f"PT{last_number + 1:03d}"
    else:
        new_code = "PT001"
    
    insert_query = """
    INSERT INTO dbo.phieuthue (maphieuthue, maphong, ngaynhan, ngaytra, tinhtrang)
    VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (new_code, maphong, check_in_datetime, check_out_datetime, 'ĐANG THUÊ'))



    insert_query = """
    INSERT INTO dbo.khachhang (makh, hoten, gioitinh, quoctich, cccd, sdt, diachi, maphong, ngaynhan, ngaytra)
    VALUES (?, ?, ?, ?, ?,?,?,?,?,?)
    """

    query = "SELECT makh FROM dbo.khachhang ORDER BY makh DESC"
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        last_code = rows[0][0]
        last_number = int(last_code[2:])
        new_code = f"KH{last_number + 1:03d}"
    else:
        new_code = "KH001"
    
    cursor.execute(insert_query, (new_code, name, gender, nationality, cccd, phone, diachi, maphong, check_in_datetime,check_out_datetime))
    unique_code = new_code

    query = "SELECT maphieudat FROM dbo.phieudat ORDER BY maphieudat DESC"
    cursor.execute(query)
    rows = cursor.fetchall()


    if rows:
        last_code = rows[0][0]
        last_number = int(last_code[2:])
        new_code = f"PD{last_number + 1:03d}"
    else:
        new_code = "PD001"
    
    

    insert_query = """
    INSERT INTO dbo.phieudat (maphieudat, makh, ngaydat, ngaynhan, ngaytra, trangthai)
    VALUES (?, ?, ?, ?, ?,?)
    """
    cursor.execute(insert_query, (new_code, unique_code, datetime.now(), check_in_datetime, check_out_datetime, "ĐANG THUÊ"))

    conn.commit()

    flash('Đặt phòng thành công!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
