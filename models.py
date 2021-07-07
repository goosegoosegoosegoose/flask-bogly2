"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)

    last_name = db.Column(db.String(50),
                           nullable=True,
                           unique=False)

    image_url = db.Column(db.Text(),
                          nullable=True,
                          unique=False,
                          server_default="https://news.artnet.com/app/news-upload/2015/09/c6e48da82c0e49d1a012971e652a5132-1560x2158-256x256.jpg")

# can't get default to work with users made with new user form on frontend