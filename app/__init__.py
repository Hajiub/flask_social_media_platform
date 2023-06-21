from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import DevelopmentConfig
from .utils import TimeFilter
from flask import Markup
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address




db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()
limiter  = Limiter(
        get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    ) 

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    limiter.init_app(app=app)
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    time_filter = TimeFilter(app)
       
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page!"
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

   
    from .auth import auth
    from .main import main
    from .profile import profile
    from .posts import post
    from .friend import friend
    from .search import search
    

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(profile)
    app.register_blueprint(post)
    app.register_blueprint(friend)
    app.register_blueprint(search)

    return app
