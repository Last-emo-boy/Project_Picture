# face_utils.py
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN
import os

def load_image_file(file_path):
    """加载图像文件"""
    return face_recognition.load_image_file(file_path)

def get_face_encodings(img):
    """获取图像中所有人脸的编码"""
    return face_recognition.face_encodings(img)

def get_face_locations(img):
    """获取图像中所有人脸的位置"""
    return face_recognition.face_locations(img)

def cluster_faces(face_encodings):
    """使用DBSCAN聚类算法对面部编码进行聚类"""
    if len(face_encodings) == 0:
        return []

    # DBSCAN聚类
    clustering_model = DBSCAN(eps=0.6, min_samples=1, metric="euclidean")
    clustering_model.fit(face_encodings)

    return clustering_model.labels_
