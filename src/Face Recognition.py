
# BƯỚC 1 DÙNG MTCNN ĐỂ LẤY ẢNH KHUÔN MẶT KHÁCH VÀ OPENCV ĐỂ RESIZE ẢNH VỀ 160X160

from keras.models import load_model
import os
from PIL import Image
import numpy as np
from mtcnn import MTCNN
import cv2


def extract_faces(dataset_path, save_path=r"C:\PYTHON\faces"):
    detector = MTCNN()

    # Kiểm tra và tạo thư mục lưu trữ faces nếu không tồn tại
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
                face = img[y:y + h, x:x + w]
                face = cv2.resize(face, (160, 160))

                face_save_path = os.path.join(save_person_folder, filename)
                cv2.imwrite(face_save_path, cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
                print(f"Đã lưu khuôn mặt: {face_save_path}")
            else:
                print(f"Không tìm thấy khuôn mặt trong ảnh: {file_path}")


# Gọi hàm để trích xuất khuôn mặt
extract_faces(r"C:\PYTHON\dataset")




#BƯỚC 2 DÙNG FACENET TRÍCH XUẤT RA VECTOR ĐẶC TRƯNG TỪ CÁC ẢNH ĐÃ QUA XỬ LÍ BẰNG MTCNN VÀ LƯU NÓ VÀO FILE ĐUÔI NPZ  CÙNG LABEL ĐỂ ĐƯA VÀO SVM TRAIN

model = load_model("C:/PYTHON/facenet_model/facenet_keras_2024.h5")

print("✅ Load model thành công!")

# Hàm tiền xử lý ảnh
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (160, 160))
    img = img.astype('float32')
    img = (img - 127.5) / 128.0
    img = np.expand_dims(img, axis=0)
    return img

# Hàm lấy embedding
def get_embedding(model, img_path):
    img = preprocess_image(img_path)
    embedding = model.predict(img)
    return embedding[0]  # lấy ra vector 512 chiều

# Tạo list lưu embedding và label
embeddings = []
labels = []

# Folder faces đã detect sẵn
faces_folder = r"C:\PYTHON\faces"

for person_name in os.listdir(faces_folder):
    person_folder = os.path.join(faces_folder, person_name)
    if not os.path.isdir(person_folder):
        continue
    for filename in os.listdir(person_folder):
        img_path = os.path.join(person_folder, filename)
        embedding = get_embedding(model, img_path)
        embeddings.append(embedding)
        labels.append(person_name)
        print(f"✅ Đã lấy embedding cho {img_path}")

# Chuyển thành mảng numpy
embeddings = np.asarray(embeddings)
labels = np.asarray(labels)

# Lưu vào file
np.savez_compressed('faces_embeddings.npz', embeddings=embeddings, labels=labels)
print("✅ Đã lưu embeddings vào file faces_embeddings.npz!")
