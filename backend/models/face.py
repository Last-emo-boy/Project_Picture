from extensions import db
import sqlalchemy

class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)  # Optional: Name associated with the face
    image_path = db.Column(db.String(255), nullable=False)
    face_encodings = db.Column(sqlalchemy.types.PickleType, nullable=True)  # Stored as a binary object
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)  # Link back to the image

    def __repr__(self):
        return f'<Face {self.uuid}>'
