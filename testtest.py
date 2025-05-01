import cv2
import numpy as np
from keras.models import load_model
from mtcnn import MTCNN
import pickle

# Load FaceNet model
facenet_model = load_model("facenet_model/facenet_keras_2024.h5")
print("✅ Đã load xong model FaceNet!")

# Load SVM model và encoder
with open("svm_face_recognition.pkl", "rb") as f:
    model_svm, out_encoder = pickle.load(f)


# Hàm tiền xử lý ảnh đầu vào
def preprocess_face(face_pixels):
    face = cv2.resize(face_pixels, (160, 160))
    face = face.astype('float32')
    face = (face - 127.5) / 128.0
    return np.expand_dims(face, axis=0)


# Hàm nhận diện khuôn mặt từ webcam
def recognize_face_from_camera():
    detector = MTCNN()
    cap = cv2.VideoCapture(0)

    print("📸 Đang mở webcam để nhận diện...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb_frame)

        for face in faces:
            x, y, w, h = face['box']
            x, y = max(0, x), max(0, y)
            face_img = rgb_frame[y:y + h, x:x + w]

            try:
                face_input = preprocess_face(face_img)
                embedding = facenet_model.predict(face_input)[0]

                # Dự đoán với SVM
                yhat_class = model_svm.predict([embedding])
                yhat_prob = model_svm.predict_proba([embedding])

                predicted_name = out_encoder.inverse_transform(yhat_class)[0]
                confidence = yhat_prob[0][yhat_class[0]]

                # Vẽ khung và hiển thị tên + xác suất
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                label = f"{predicted_name} ({confidence * 100:.2f}%)"
                cv2.putText(frame, label, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

                # In ra console
                print(f"✅ Nhận diện: {predicted_name} - Độ tin cậy: {confidence:.2f}")

            except Exception as e:
                print("❌ Lỗi xử lý khuôn mặt:", e)

        cv2.imshow("Nhận diện khuôn mặt", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Gọi hàm
if __name__ == "__main__":
    recognize_face_from_camera()
