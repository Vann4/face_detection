from pathlib import Path
from deepface import DeepFace
# import face_recognition
# from PIL import Image

# image_path = Path("let.jpg")
# df = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], enforce_detection=False)
# print(df[0]['age'])
# print(df[0]['dominant_gender'])
# print(df[0]['dominant_race'])

# count = 0
# img = f"let.jpg"
# faces = face_recognition.load_image_file(img)
# faces_locations = face_recognition.face_locations(faces)
#
# for face_location in faces_locations:
#     top, right, bottom, left = face_location
#
#     face_img = faces[top-30:bottom + 30, left-20:right + 20]
#     pil_img = Image.fromarray(face_img)
#     pil_img.save(f"{count}_{img}")
#     count += 1

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

# import face_recognition

# Load the jpg files into numpy arrays
# biden_image = face_recognition.load_image_file("biden.png")
# obama_image = face_recognition.load_image_file("obama.png")
# print(obama_image)
# print('===============================================')
# unknown_image = face_recognition.load_image_file("cfbcad3349a6bf24308b38e0e3f6b1b8.jpeg")
# print(unknown_image)

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
# try:
#     biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
#     obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#     unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
#     print(biden_face_encoding)
#     print(obama_face_encoding)
#     print(unknown_face_encoding)
# except IndexError:
#     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
#     quit()

# known_faces = [
#     biden_face_encoding,
#     obama_face_encoding
# ]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
# results = face_recognition.compare_faces([biden_face_encoding], biden_face_encoding)

# print("Is the unknown face a picture of Biden? {}".format(results[0]))
# print("Is the unknown face a picture of Obama? {}".format(results[1]))
# print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
# print(results)

# Для прямоугольника вокруг лица
# import face_recognition
# from PIL import Image, ImageDraw
#
#
# def face_rec():
#     gal_face_img = face_recognition.load_image_file("Katya.jpg")
#     gal_face_location = face_recognition.face_locations(gal_face_img)
#
#     pil_img1 = Image.fromarray(gal_face_img)
#     draw1 = ImageDraw.Draw(pil_img1)
#
#     for (top, right, bottom, left) in gal_face_location:
#         draw1.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0), width=4)
#
#     del draw1
#     pil_img1.save("new_gal1.jpg")
#
#
# face_rec()








# import cv2
# import dlib
# import face_recognition
# import numpy as np
#
# # Загрузите модель dlib shape predictor
# shape_predictor_path = "shape_predictor_68_face_landmarks.dat"
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shape_predictor_path)
#
# # Загрузите модель для оценки возраста
# age_model_path = "age_deploy.prototxt"
# age_weights_path = "age_net.caffemodel"
# age_net = cv2.dnn.readNetFromCaffe(age_model_path, age_weights_path)
#
#
# def estimate_age(image_path):
#     img = cv2.imread(image_path)
#     rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
#     # Обнаружение лица
#     dets = detector(rgb_img, 0)
#
#     if len(dets) == 0:
#         print("No face detected.")
#         return
#
#     # Получение вектора признаков лица
#     shape = predictor(rgb_img, dets[0])
#     face_features = face_recognition.face_encodings(rgb_img, [shape_to_np(shape)])[0]
#
#     # Нормализация и изменение размера изображения для ввода в модель
#     blob = cv2.dnn.blobFromImage(img, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
#     age_net.setInput(blob)
#
#     # Получение оценки возраста
#     outputs = age_net.forward()
#     age = outputs[0, 0, :, :].argmax()
#     age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
#     estimated_age = age_list[age]
#
#     print(f"Estimated age: {estimated_age}")
#
#
# def shape_to_np(shape, dtype="int"):
#     coords = np.zeros((68, 2), dtype=dtype)
#     for i in range(0, 68):
#         coords[i] = (shape.part(i).x, shape.part(i).y)
#     return coords
#
#
# # Оцените возраст по фотографии
# estimate_age("let_2.jpg")






# import cv2
# import dlib
#
# # Загрузка модели dlib shape predictor
# shape_predictor_path = "shape_predictor_68_face_landmarks.dat"
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(shape_predictor_path)
#
# # Загрузка модели для оценки возраста
# age_model_path = "age_deploy.prototxt"
# age_weights_path = "age_net.caffemodel"
# age_net = cv2.dnn.readNetFromCaffe(age_model_path, age_weights_path)
#
# # Загрузка изображения
# image_path = "obama.png"
# image = cv2.imread(image_path)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # Обнаружение лица на изображении
# faces = detector(gray)
#
# # Определение возраста для каждого обнаруженного лица
# for face in faces:
#     # Получение ориентиров лица
#     landmarks = predictor(gray, face)
#
#     # Извлечение координат ориентиров лица
#     left_eye_x = landmarks.part(36).x
#     left_eye_y = landmarks.part(36).y
#     right_eye_x = landmarks.part(45).x
#     right_eye_y = landmarks.part(45).y
#
#     # Извлечение области лица для оценки возраста
#     face_img = gray[face.top():face.bottom(), face.left():face.right()]
#     # Преобразование изображения лица в цветное
#     face_img_color = cv2.cvtColor(face_img, cv2.COLOR_GRAY2RGB)
#     blob = cv2.dnn.blobFromImage(face_img_color, scalefactor=1.0, size=(227, 227),
#                                  mean=(78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
#
#     # Передача изображения в модель для оценки возраста
#     # Преобразование изображения лица в цветное
#     age_net.setInput(blob)
#     age_preds = age_net.forward()
#     age = age_preds[0].argmax()
#
#     # Вывод возраста на изображении
#     cv2.putText(image, "Age: " + str(age), (face.left(), face.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
#                 (0, 255, 255), 2)
#
# # Отображение изображения с выделенным возрастом лица
# cv2.imshow("Age Detection", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
