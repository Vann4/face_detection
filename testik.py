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
img = f"nicole-wallace-and-gabriel-guevara_97.jpg"
faces = face_recognition.load_image_file(img)
faces_locations = face_recognition.face_locations(faces)

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

import face_recognition

# Load the jpg files into numpy arrays
biden_image = face_recognition.load_image_file("biden.jpg")
obama_image = face_recognition.load_image_file("obama.jpg")
unknown_image = face_recognition.load_image_file("obama2.jpg")

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    biden_face_encoding,
    obama_face_encoding
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Biden? {}".format(results[0]))
print("Is the unknown face a picture of Obama? {}".format(results[1]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))

