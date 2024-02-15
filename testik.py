from pathlib import Path
from deepface import DeepFace

image_path = Path("detection_face/face_app/media/2_1663137622_10-mykaleidoscope-ru-p-veselie-lyudi-pinterest-10.jpg")
df = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], enforce_detection=False)
print(df[0]['age'])
print(df[0]['dominant_gender'])
print(df[0]['dominant_race'])