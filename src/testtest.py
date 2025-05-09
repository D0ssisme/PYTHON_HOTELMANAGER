import cv2
import numpy as np
from keras.models import load_model
import pickle
from mtcnn import MTCNN

def recognize_face_from_camera():
    # Load model
    model = load_model("C:/PYTHON/facenet_model/facenet_keras_2024.h5")
    with open("svm_face_recognition.pkl", "rb") as f:
        model_svm, out_encoder = pickle.load(f)

    detector = MTCNN()

    cap = cv2.VideoCapture(0)
    print("🎥 Mở webcam để nhận diện... Nhấn 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)
        for face in faces:
            x, y, w, h = face['box']
            x, y = max(0, x), max(0, y)
            face_img = rgb[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (160, 160)).astype('float32')
            face_img = (face_img - 127.5) / 128.0
            face_img = np.expand_dims(face_img, axis=0)

            # Lấy embedding và dự đoán
            embedding = model.predict(face_img)[0]
            embedding = embedding.reshape(1, -1)
            yhat_class = model_svm.predict(embedding)
            yhat_prob = model_svm.predict_proba(embedding)

            predicted_name = out_encoder.inverse_transform(yhat_class)[0]
            confidence = yhat_prob[0][yhat_class[0]]

            if confidence > 0.7:
                cap.release()
                cv2.destroyAllWindows()
                print("✅ Nhận diện thành công:", predicted_name)
                return predicted_name
            else:
                print("🚫 xác thực thất bại . Hãy thử lại!")

        cv2.imshow("NHAN DIEN ", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

if __name__ == "__main__":
    recognized_name = recognize_face_from_camera()
    if recognized_name:
        print("Kết quả nhận diện:", recognized_name)
    else:
        print("Không nhận diện được khuôn mặt.")
