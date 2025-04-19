"""
import os
from PIL import Image
import numpy as np
from mtcnn import MTCNN
import cv2

def extract_faces(dataset_path, save_path="faces"):
    detector = MTCNN()

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for person_name in os.listdir(dataset_path):
        person_folder = os.path.join(dataset_path, person_name)
        if not os.path.isdir(person_folder):
            continue

        save_person_folder = os.path.join(save_path, person_name)
        os.makedirs(save_person_folder, exist_ok=True)

        for filename in os.listdir(person_folder):
            file_path = os.path.join(person_folder, filename)
            img = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)

            faces = detector.detect_faces(img)
            if faces:
                x, y, w, h = faces[0]['box']
                x, y = max(0, x), max(0, y)
                face = img[y:y+h, x:x+w]
                face = cv2.resize(face, (160, 160))

     

                face_save_path = os.path.join(save_person_folder, filename)
                cv2.imwrite(face_save_path, cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
                print(f"Đã lưu khuôn mặt: {face_save_path}")
            else:
                print(f"Không tìm thấy khuôn mặt trong ảnh: {file_path}")


extract_faces("C:/PYTHON/dataset")
"""


import cv2
import numpy as np
from keras.models import load_model


# Load mô hình Facenet
model = load_model("facenet_model/facenet_keras_2024.h5")
print("✅ Load model thành công!")

# Hàm tiền xử lý ảnh cho mô hình Facenet
def preprocess_image(img_path):
    # Đọc ảnh từ file
    img = cv2.imread(img_path)
    # Resize ảnh về kích thước 160x160 mà mô hình yêu cầu
    img = cv2.resize(img, (160, 160))
    # Chuyển đổi ảnh sang dạng float32 và chuẩn hóa giá trị pixel
    img = img.astype('float32')
    img = (img - 127.5) / 128.0  # chuẩn hóa theo Facenet
    # Thêm chiều batch size
    img = np.expand_dims(img, axis=0)
    return img

# Hàm lấy embedding từ mô hình
def get_embedding(model, img_path):
    img = preprocess_image(img_path)
    # Chạy ảnh qua mô hình để lấy embedding
    embedding = model.predict(img)
    return embedding

# Đọc ảnh và lấy embedding
img_path = r'C:\PYTHON\faces\CR7_KH003\IMG1.jpg' # Đảm bảo đường dẫn đầy đủ

embedding = get_embedding(model, img_path)

print("Embedding của ảnh:", embedding)
