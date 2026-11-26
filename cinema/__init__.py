import os
import dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect          



class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    app = Flask(__name__)
    dotenv.load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "cinema_secret_dev_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///cinema.db"
    )

    db.init_app(app)

    csrf = CSRFProtect()                         
    csrf.init_app(app)  

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to see that page."
    login_manager.init_app(app)

    from . import model

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(model.User, int(user_id))

    with app.app_context():
        db.create_all()
        # Seed initial demo movies, showtimes and food items if database is empty
        if not db.session.execute(db.select(model.Movie)).scalars().first():
            from .main import demo_movies
            m_list, st_list = demo_movies()
            db.session.add_all(m_list)
            db.session.add_all(st_list)
            db.session.commit()

        if not db.session.execute(db.select(model.FoodItem)).scalars().first():
            from .main import demo_food_items
            db.session.add_all(demo_food_items())
            db.session.commit()

    from . import main
    from . import auth

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app