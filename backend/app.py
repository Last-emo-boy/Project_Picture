from flask import Flask
from api.routes import init_api_routes
from extensions import db
from flask_cors import CORS
from config import Config  # 导入Config类
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 使用Config类配置应用

    # 设置日志记录
    logging.basicConfig(level=logging.DEBUG)

    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # 创建所有未创建的数据库表
        logging.info("All tables created.")
        
    init_api_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)