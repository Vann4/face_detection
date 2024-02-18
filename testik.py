from pathlib import Path
from deepface import DeepFace
#
# image_path = Path("detection_face/face_app/media/2_1663137622_10-mykaleidoscope-ru-p-veselie-lyudi-pinterest-10.jpg")
# df = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], enforce_detection=False)
# print(df[0]['age'])
# print(df[0]['dominant_gender'])
# print(df[0]['dominant_race'])

import face_recognition
from PIL import Image

count = 0
img = "photo_2024-01-09_20-02-42.jpg"
faces = face_recognition.load_image_file(img)
faces_locations = face_recognition.face_locations(faces, model='cnn')

for face_location in faces_locations:
    top, right, bottom, left = face_location

    face_img = faces[top:bottom, left:right]
    pil_img = Image.fromarray(face_img)
    pil_img.save(f"{count}_{img}")
    count += 1

# Загрузка модели VGG-Face
# vggface_model = DeepFace.build_model('VGG-Face')
#
# # Путь к изображению
# img_path = "2024-02-18_151516.png"
#
# # Выполнение анализа лица с использованием модели VGG-Face
# result = DeepFace.analyze(img_path, detector_backend='ssd', enforce_detection=False)
#
# # Вывод результата
# print("dominant_emotion:", result[0]["dominant_emotion"])
# print("dominant_gender:", result[0]["dominant_gender"])
# print("dominant_race:", result[0]["dominant_race"])
# print("Age:", result[0]["age"])

