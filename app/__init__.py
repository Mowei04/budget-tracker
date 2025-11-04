import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))        # .../coursework1/app
    project_root = os.path.dirname(basedir)
    db_path = os.path.join(project_root, "data.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.setdefault("SECRET_KEY", "dev-secret")

    db.init_app(app)
    migrate.init_app(app, db)

    # 导入模型，确保迁移能发现表结构（避免循环依赖，放在这里）
    from . import models  # noqa

    # 注册蓝图
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    return app