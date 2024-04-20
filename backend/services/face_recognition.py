import face_recognition
import logging
import os
import uuid
from PIL import Image as PILImage
from models.image import Image
from extensions import db
from config import Config
from pathlib import Path


# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def encode_faces(image_path, save_folder):
    """
    Encodes faces found in the image and saves cropped face images to a directory.

    :param image_path: Path to the image file
    :param save_folder: Directory to save face images
    :return: List of dictionaries containing face encodings and metadata
    """
    try:
        Path(save_folder).mkdir(parents=True, exist_ok=True)

        # Load image using face_recognition
        img = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(img)
        face_encodings = face_recognition.face_encodings(img, face_locations)

        face_data = []
        
        # PIL for cropping and saving face images
        pil_image = PILImage.open(image_path)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Generate a unique identifier for the face
            face_uuid = str(uuid.uuid4())

            # Crop face from image
            top, right, bottom, left = face_location
            face_image = pil_image.crop((left, top, right, bottom))
            face_filename = f"{face_uuid}.jpg"
            face_path = os.path.join(save_folder, face_filename)
            face_image.save(face_path)

            # Save or process the face data
            face_data.append({
                'face_uuid': face_uuid,
                'face_path': face_path,
                'face_encoding': face_encoding
            })

        return face_data

    except Exception as e:
        logging.error(f"Failed to encode faces in image {image_path}: {str(e)}")
        return None
