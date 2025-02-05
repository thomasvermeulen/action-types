from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Log in om deze pagina te bekijken.'

@login_manager.user_loader
def load_user(id):
    from app.models.teacher import Teacher
    return Teacher.query.get(int(id))

def create_app():
    app = Flask(__name__)
    
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'

    db.init_app(app)
    login_manager.init_app(app)

    app.jinja_env.globals.update(min=min)

    with app.app_context():
        from app.models.student import Student
        from app.models.statement import Statement, StatementChoice
        from app.models.response import Response
        from app.models.teacher import Teacher
        
        from app.controllers.main import bp as main_bp
        app.register_blueprint(main_bp)
        
        from app.controllers.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        
        from app.controllers.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
