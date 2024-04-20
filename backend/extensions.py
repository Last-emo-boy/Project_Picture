from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

def check_and_create_database_tables():
    try:
        # 尝试查询表，以检查其是否存在
        db.engine.execute('SELECT 1 FROM image LIMIT 1;')
        logging.info("Database tables are ready.")
    except Exception as e:
        logging.error("Database table check failed: %s", str(e))
        # 尝试创建表
        try:
            db.create_all()
            logging.info("Database tables created successfully.")
        except Exception as e:
            logging.error("Failed to create database tables: %s", str(e))
            # 可能需要抛出异常或终止应用启动
            raise Exception("Database initialization failed.")
