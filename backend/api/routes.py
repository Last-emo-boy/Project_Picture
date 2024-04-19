from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import numpy as np
from models.image import Image
from app import db
from services.face_recognition import encode_faces
import face_recognition

api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def search_by_face(target_encodings):
    if target_encodings is None:
        return []
    all_images = Image.query.all()
    results = []
    for image in all_images:
        if image.face_encodings is not None:
            known_encodings = np.array(image.face_encodings)
            distances = face_recognition.face_distance([known_encodings], target_encodings)
            if np.any(distances <= 0.6):  # assuming 0.6 as a threshold for face matching
                results.append(image)
    return results

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image_hash = Image.compute_image_hash(file_path)
        face_encoding = encode_faces(file_path)
        image = Image(filename=filename, image_hash=image_hash, face_encodings=face_encoding)
        db.session.add(image)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@api_bp.route('/search', methods=['GET'])
def search_images():
    face_file = request.files.get('file')
    if face_file:
        face_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'search_temp.jpg')
        face_file.save(face_path)
        target_encodings = encode_faces(face_path)
        matched_images = search_by_face(target_encodings)
        return jsonify([{'id': img.id, 'filename': img.filename} for img in matched_images])
    else:
        return jsonify({'error': 'No face file provided'}), 400

def init_api_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')
