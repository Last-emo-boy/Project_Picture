from flask import Flask, request, jsonify
from PIL import Image
import face_recognition
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_face_images(file_path):
    # 加载图片并识别人脸
    img = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(img)
    image = Image.open(file_path)
    faces_saved = []

    # 对每个识别的人脸进行截图并保存
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image.crop((left, top, right, bottom))
        face_filename = f"{uuid.uuid4().hex}.jpg"  # 使用 UUID 生成唯一的文件名
        face_path = os.path.join(app.config['UPLOAD_FOLDER'], 'faces', face_filename)
        face_image.save(face_path)
        faces_saved.append(face_path)

    return faces_saved

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        faces_saved = save_face_images(filename)
        return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'faces': faces_saved}), 200

@app.route('/tag_face', methods=['POST'])
def tag_face():
    data = request.get_json()
    face_id = data.get('face_id')
    tag = data.get('tag')
    # 这里可以添加将标签存储到数据库的代码
    print(f"Received tag '{tag}' for face '{face_id}'")
    return jsonify({'message': 'Tag processed successfully'}), 200

if __name__ == '__main__':
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'faces'), exist_ok=True)
    app.run(debug=True)
