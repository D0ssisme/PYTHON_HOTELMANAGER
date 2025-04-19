
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

