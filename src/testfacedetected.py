
import numpy as np
import cv2
from keras.models import load_model
import pickle
from sklearn.preprocessing import LabelEncoder
from mtcnn import MTCNN
from sklearn.svm import SVC
import os

# Load mô hình Facenet và SVM
model_facenet = load_model("C:/PYTHON/facenet_model/facenet_keras_2024.h5")
with open('svm_face_recognition.pkl', 'rb') as f:
    model_svm, out_encoder = pickle.load(f)

# Hàm tiền xử lý ảnh cho mô hình Facenet
def preprocess_image(img):
    # Kiểm tra kích thước của ảnh
    print(f"Kích thước ảnh ban đầu: {img.shape}")

    # Resize ảnh về kích thước 160x160 mà mô hình yêu cầu
    img = cv2.resize(img, (160, 160))
    print(f"Kích thước ảnh sau khi resize: {img.shape}")

    # Chuyển ảnh sang dạng float32 và chuẩn hóa giá trị pixel
    img = img.astype('float32')
    img = (img - 127.5) / 128.0  # chuẩn hóa theo Facenet

    # Thêm chiều batch size
    img = np.expand_dims(img, axis=0)

    return img


def get_embedding(model, img):
    img = preprocess_image(img)
    embedding = model.predict(img)
    return embedding[0]  # lấy ra vector 512 chiều


# Khởi tạo detector MTCNN
detector = MTCNN()

# Mở camera
cap = cv2.VideoCapture(0)

while True:
    # Đọc frame từ webcam
    ret, frame = cap.read()

    if not ret:
        print("Không thể đọc từ webcam")
        break

    # Phát hiện khuôn mặt trong frame
    faces = detector.detect_faces(frame)

    # Nếu phát hiện khuôn mặt
    for face in faces:
        x, y, w, h = face['box']
        face_region = frame[y:y + h, x:x + w]

        # Lấy embedding cho khuôn mặt
        embedding = get_embedding(model_facenet, face_region)

        # Dự đoán xác suất và nhãn cho lớp SVM
        probabilities = model_svm.predict_proba([embedding])  # Lấy xác suất của từng lớp
        predicted_label = out_encoder.inverse_transform([np.argmax(probabilities)])[0]
        predicted_prob = probabilities[0][np.argmax(probabilities)]  # Xác suất của lớp dự đoán

        # Vẽ hình chữ nhật quanh khuôn mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Hiển thị nhãn và xác suất
        label = f"{predicted_label}: {predicted_prob * 100:.2f}%"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Hiển thị frame với nhận diện khuôn mặt
    cv2.imshow('Face Recognition - Real-time', frame)

    # Thoát khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên khi kết thúc
cap.release()
cv2.destroyAllWindows()
