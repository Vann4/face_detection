from pathlib import Path
from deepface import DeepFace
#
# image_path = Path("detection_face/face_app/media/2_1663137622_10-mykaleidoscope-ru-p-veselie-lyudi-pinterest-10.jpg")
# df = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], enforce_detection=False)
# print(df[0]['age'])
# print(df[0]['dominant_gender'])
# print(df[0]['dominant_race'])

# import face_recognition
# from PIL import Image
#
# count = 0
# img = f"nicole-wallace-and-gabriel-guevara_97.jpg"
# faces = face_recognition.load_image_file(img)
# faces_locations = face_recognition.face_locations(faces)
#
# for face_location in faces_locations:
#     top, right, bottom, left = face_location
#
#     face_img = faces[top:bottom, left:right]
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

import face_recognition

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
try:
    # biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    biden_face_encoding = [-0.09749204, 0.16283968, 0.0928993, -0.07910567, -0.0892586, 0.03796205,
                           -0.0704493, -0.09257451, 0.06200829, -0.01645486, 0.17627372, -0.05695267,
                           -0.32136664, 0.03394438, 0.02716736, 0.11324412, -0.13818718, -0.0517398,
                           -0.25245893, -0.07880363, 0.00101264, 0.03239107, 0.06770262, -0.05068592,
                           -0.12406863, -0.22574116, -0.06369082, -0.11727406, -0.0122924, -0.1167083,
                           0.08848497, -0.03301142, -0.22500709, -0.07459413, -0.06950361, -0.03221207,
                           -0.03736795, -0.06974325, 0.12900005, 0.01273101, -0.17156938, 0.06036876,
                           0.04117397, 0.21459694, 0.2841135, -0.00650079, 0.01214006, -0.12317383,
                           0.10798009, -0.19006832, 0.03749418, 0.08830278, 0.2269192, 0.07516217,
                           0.11391088, -0.06061251, 0.08569899, 0.18698515, -0.21869189, 0.09704304,
                           0.06439742, -0.02142407, 0.01267852, -0.04423641, 0.14488287, 0.08870284,
                           -0.06023942, -0.12219066, 0.20075195, -0.07001486, -0.09809951, 0.08566003,
                           -0.13369566, -0.1504201, -0.35563287, -0.03676324, 0.27737042, 0.03113138,
                           -0.27203831, -0.06014, -0.07408885, -0.06196934, -0.01853711, 0.06219992,
                           -0.09054386, -0.13057122, -0.01445889, 0.02093165, 0.26027289, -0.10458262,
                           -0.01240739, 0.25309214, 0.05926039, -0.16694558, 0.0232409, 0.06279705,
                           -0.09426161, -0.04321767, -0.13543546, -0.03567099, -0.01456931, -0.16184346,
                           -0.06240197, 0.08676378, -0.21868765, 0.13213521, 0.0357991, -0.04701253,
                           -0.02920898, -0.05455891, -0.04410928, -0.02514305, 0.25299588, -0.211643,
                           0.18291698, 0.23769064, -0.04312382, 0.00057312, 0.00258662, 0.10011249,
                           -0.01159052, 0.08598831, -0.13610862, -0.11338811, 0.05575416, -0.00860824,
                           -0.04337286, 0.09052694]
    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    # print(biden_face_encoding)
    # print(obama_face_encoding)
    # print(unknown_face_encoding)
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

# known_faces = [
#     biden_face_encoding,
#     obama_face_encoding
# ]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces([biden_face_encoding], biden_face_encoding)

# print("Is the unknown face a picture of Biden? {}".format(results[0]))
# print("Is the unknown face a picture of Obama? {}".format(results[1]))
# print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
print(results)

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
