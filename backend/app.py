from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.routes import init_api_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

def create_app():
    init_api_routes(app)  # 初始化API路由
    with app.app_context():
        db.create_all()  # 创建数据库表
    return app

if __name__ == '__main__':
    create_app().run(debug=True)
