from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import numpy as np
#BƯỚC 3 TRAIN SVM DỰA TRÊN VECTOR VÀ LABEL CỦA KHÁCH ĐÃ LƯU VÀO FILE NPZ
# Load embeddings đã lưu
data = np.load('faces_embeddings.npz')
embeddings, labels = data['embeddings'], data['labels']

# Encode label
out_encoder = LabelEncoder()
labels_encoded = out_encoder.fit_transform(labels)

# Train SVM
model_svm = SVC(kernel='linear', probability=True)
model_svm.fit(embeddings, labels_encoded)

# Lưu model SVM nếu cần
import pickle
with open('svm_face_recognition.pkl', 'wb') as f:
    pickle.dump((model_svm, out_encoder), f)

print("✅ SVM train xong và lưu model rồi!")
