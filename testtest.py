import cv2
import numpy as np
from keras.models import load_model
from mtcnn import MTCNN
import pickle

# Load model
print("🔄 Đang load model...")
facenet_model = load_model("facenet_model/facenet_keras_2024.h5")
with open("svm_face_recognition.pkl", "rb") as f:
    model_svm, label_encoder = pickle.load(f)
print("✅ Đã load xong FaceNet & SVM")

# MTCNN detector
detector = MTCNN()

# Hàm tiền xử lý ảnh
def preprocess_face(face_img):
    face = cv2.resize(face_img, (160, 160))
    face = face.astype('float32')
    face = (face - 127.5) / 128.0
    return np.expand_dims(face, axis=0)

# Hàm lấy embedding
def get_embedding(face_img):
    preprocessed = preprocess_face(face_img)
    embedding = facenet_model.predict(preprocessed)
    return embedding[0]  # shape (512,)

# Mở webcam
cap = cv2.VideoCapture(0)
print("📷 Đang bật webcam...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb_frame)

    for face in faces:
        x, y, w, h = face['box']
        x, y = max(0, x), max(0, y)
        face_img = rgb_frame[y:y+h, x:x+w]

        try:
            embedding = get_embedding(face_img)
            probs = model_svm.predict_proba([embedding])[0]
            best_idx = np.argmax(probs)
            name = label_encoder.inverse_transform([best_idx])[0]
            confidence = probs[best_idx] * 100

            label = f"{name}: {confidence:.2f}%"
            color = (0, 255, 0) if confidence > 50 else (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Hiển thị độ tin cậy dưới tên người
            cv2.putText(frame, f"Confidence: {confidence:.2f}%",
                        (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        except Exception as e:
            print("❌ Lỗi khi nhận diện:", e)

    cv2.imshow("Face Recognition - Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
