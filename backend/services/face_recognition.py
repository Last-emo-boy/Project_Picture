import face_recognition
from models.image import Image
from app import db

def encode_faces(image_path):
    img = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(img)
    if encodings:
        return encodings[0]  # 取第一个人脸的编码
    return None
