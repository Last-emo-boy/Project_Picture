from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import numpy as np
from models.image import Image
from extensions import db
from services.face_recognition import encode_faces
import face_recognition
from models.face import Face
import logging
from config import Config  # 导入Config类


api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@api_bp.route('/search_by_face', methods=['POST'])
def api_search_by_face():
    try:
        # Assume the request contains face encoding data in JSON format
        data = request.get_json()
        target_encodings = np.array(data['encodings'])  # Ensure this matches the format you expect
        
        matching_images = search_by_face(target_encodings)
        result_data = [{'image_id': img.id, 'filename': img.filename} for img in matching_images]
        
        return jsonify(result_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # 确保上传目录存在，如果不存在则创建
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)
        try:
            file.save(file_path)
        except IOError as e:
            logging.error(f"Error saving file: {e}")
            return jsonify({'error': 'Failed to save file', 'detail': str(e)}), 500

        try:
            image_hash = Image.compute_image_hash(file_path)
            face_data = encode_faces(file_path, Config.CROPPED_FACE)
            if face_data is None:
                raise ValueError("Failed to encode any faces in the image")

            # Extract face encodings from face_data and convert them to lists
            face_encoding_lists = [face['face_encoding'].tolist() for face in face_data]

            image = Image(filename=filename, image_hash=image_hash, face_encodings=face_encoding_lists)
            db.session.add(image)
            db.session.commit()
            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
        except (ValueError, IOError) as e:
            logging.error(f"Error processing image or database operation: {e}")
            db.session.rollback()
            return jsonify({'error': 'Error processing image or saving to database', 'detail': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400
'''

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    except Exception as e:
        current_app.logger.error('Unhandled exception: %s', str(e))
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500
'''

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
