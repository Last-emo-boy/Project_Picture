from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import face_recognition
import os
import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary  # 导入 LargeBinary 数据类型
import hashlib
import numpy as np
from face_utils import load_image_file, get_face_encodings, get_face_locations, cluster_faces




app = Flask(__name__, static_folder='../frontend')
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../faces.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 相对路径设置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../uploads')
FACES_FOLDER = os.path.join(UPLOAD_FOLDER, 'faces')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FACES_FOLDER'] = FACES_FOLDER

# 确保文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)

print("Current working directory:", os.getcwd())
print("Database path:", app.config['SQLALCHEMY_DATABASE_URI'])

class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    face_uuid = db.Column(db.String(36), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)
    encoding = db.Column(LargeBinary)  # 使用 LargeBinary 存储人脸编码
    image_hash = db.Column(db.String(64), nullable=False, unique=True)  # 存储图片哈希

    def __repr__(self):
        return f'<Face {self.face_uuid}>'
    
# 创建数据库和表
def create_database():
    with app.app_context():
        db.create_all()
    
def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))

    return np.linalg.norm(face_encodings - face_to_compare, axis=1)

def save_face_images(file_path):
    img = face_recognition.load_image_file(file_path)
    face_encodings = face_recognition.face_encodings(img)
    face_locations = face_recognition.face_locations(img)
    print(f"检测到 {len(face_encodings)} 个人脸")  # 调试输出
    image = Image.open(file_path)
    faces_saved = []

    for face_encoding, face_location in zip(face_encodings, face_locations):
        known_faces = Face.query.all()
        known_encodings = [np.frombuffer(face.encoding, dtype=np.float64) for face in known_faces if face.encoding]

        if known_encodings:
            distances = face_distance(known_encodings, face_encoding)
            if np.any(distances <= 0.6):  # Assuming 0.6 as a threshold
                match_index = np.argmin(distances)
                face_uuid = known_faces[match_index].face_uuid
                new_face = False
            else:
                face_uuid = str(uuid.uuid4())
                new_face = True
        else:
            face_uuid = str(uuid.uuid4())
            new_face = True

        top, right, bottom, left = face_location
        face_image = image.crop((left, top, right, bottom))
        face_filename = f"{face_uuid}.jpg"
        face_path = os.path.join(app.config['FACES_FOLDER'], face_filename)
        face_image.save(face_path)

        if new_face:
            encoding_data = face_encoding.tobytes()  # 将numpy数组转换为字节
            new_face_record = Face(face_uuid=face_uuid, encoding=encoding_data, image_hash=compute_image_hash(face_path))
            db.session.add(new_face_record)
            db.session.commit()

        faces_saved.append({'path': face_path, 'uuid': face_uuid, 'new': new_face})

    return faces_saved


def compute_image_hash(image_path):
    with open(image_path, "rb") as f:
        file_hash = hashlib.sha256()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)
    return file_hash.hexdigest()


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # 保存上传的文件
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    # 计算文件的哈希值，检查是否已存在相同的图片
    file_hash = compute_image_hash(filename)
    existing_file = Face.query.filter_by(image_hash=file_hash).first()
    if existing_file:
        # 如果文件已存在，返回已存在的消息和空的人脸列表
        return jsonify({'message': 'File already uploaded', 'filename': filename, 'faces': []}), 200

    # 处理图像文件，提取人脸数据
    faces_saved = save_face_images(filename)

    # 返回成功上传的消息和检测到的人脸信息
    return jsonify({'message': 'File uploaded successfully', 'filename': filename, 'faces': faces_saved}), 200


@app.route('/tag_face', methods=['POST'])
def tag_face():
    data = request.get_json()
    face_id = data.get('face_id')
    tag = data.get('tag')
    # 这里可以添加将标签存储到数据库的代码
    print(f"Received tag '{tag}' for face '{face_id}'")
    return jsonify({'message': 'Tag processed successfully'}), 200

@app.route('/uploads/faces/<filename>')
def serve_face_image(filename):
    return send_from_directory(app.config['FACES_FOLDER'], filename)

if __name__ == '__main__':
    create_database()  # 确保在运行服务器前创建数据库
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'faces'), exist_ok=True)
    app.run(debug=True)
