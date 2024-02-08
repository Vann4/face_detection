import face_recognition
import deepface
from deepface import DeepFace

# Загрузка фото
image = face_recognition.load_image_file("dataset/stat_1.png")

# Распознавание лиц на фото
face_locations = face_recognition.face_locations(image, model="cnn", enforce_detection=False)
face_encodings = face_recognition.face_encodings(image, face_locations)

# Определение пола и возраста на основе разблокированной модели deepface
results = DeepFace.analyze(image, actions=["gender", "age"])

for i, face_encoding in enumerate(face_encodings):
    top, right, bottom, left = face_locations[i]
    # print(f"Пол: {results['gender'][i]}")
    # print(f"Возраст: {results['age'][i]}")
    print(f"Возраст: {results[i]}")
