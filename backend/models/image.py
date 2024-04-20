import hashlib
from extensions import db
from sqlalchemy import JSON


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)  # Optional: For user management
    image_hash = db.Column(db.String(64), nullable=False)
    face_encodings = db.Column(JSON, nullable=True)  # Add this line
    primary_face_id = db.Column(db.Integer, db.ForeignKey('face.id'), nullable=True)  # New field

    # Relation to Face objects
    faces = db.relationship('Face', backref='image', lazy=True)

    def __init__(self, filename, image_hash, face_encodings=None, user_id=None, primary_face_id=None):  # Update constructor
        self.filename = filename
        self.image_hash = image_hash
        self.face_encodings = face_encodings  # Add this line
        self.user_id = user_id
        self.primary_face_id = primary_face_id

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