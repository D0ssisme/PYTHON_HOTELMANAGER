def recognize_face_from_camera():
    import cv2
    import numpy as np
    from keras.models import load_model
    import pickle
    from mtcnn import MTCNN
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))  # thư mục "src"
    pkl_path = os.path.join(current_dir, "svm_face_recognition.pkl")

    # Load model
    model = load_model("C:/PYTHON/facenet_model/facenet_keras_2024.h5")

    with open(pkl_path, "rb") as f:
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
            face_img = rgb[y:y + h, x:x + w]
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

            # Vẽ vòng tròn quanh khuôn mặt
            center = (x + w // 2, y + h // 2)
            radius = int((w + h) // 4)
            cv2.circle(frame, center, radius, (0, 255, 0), 2)  # Vẽ vòng tròn xanh

            # Hiển thị confidence lên màn hình
            text = f'{predicted_name}: {confidence * 100:.2f}%'
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Nếu confidence cao hơn 50%, thì thông báo thành công
            if confidence > 0.7:
                print(f"✅ Nhận diện thành công: {predicted_name} với độ tin cậy {confidence * 100:.2f}%")
                return predicted_name
            else:
                print(f"🚫 Xác thực thất bại với độ tin cậy {confidence * 100:.2f}%")

        cv2.imshow("NHAN DIEN", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
