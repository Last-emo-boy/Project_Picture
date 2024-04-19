from app import db
import hashlib
import numpy as np

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)  # Optional: For user management
    image_hash = db.Column(db.String(64), nullable=False)
    face_encodings = db.Column(db.PickleType, nullable=True)  # 存储人脸编码

    def __repr__(self):
        return f'<Image {self.filename}>'

    @staticmethod
    def compute_image_hash(image_path):
        hasher = hashlib.sha256()
        with open(image_path, "rb") as f:
            chunk = f.read(8192)
            while chunk:
                hasher.update(chunk)
                chunk = f.read(8192)
        return hasher.hexdigest()
