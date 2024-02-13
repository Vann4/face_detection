from pathlib import Path
from deepface import DeepFace

image_path = Path("Vin_2.jpg")
df = DeepFace.analyze(img_path=image_path, actions=['age', 'gender', 'race'], enforce_detection=False)
print(df[0]['age'])
print(df[0]['dominant_gender'])
print(df[0]['dominant_race'])