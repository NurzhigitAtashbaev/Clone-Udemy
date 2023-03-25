from flask_login import UserMixin
from sqlalchemy import func, Enum

from project import *


class UserType(Enum):
    USER = 'user'
    ADMIN = 'admin'


class Type(Enum):
    user_name = "User"
    mentor_name = "Mentor"


class Experience(Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class Audience(Enum):
    student = "Student"
    professional = "Professional"


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, index=True)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    type = db.Column(db.String, index=True, nullable=False)
    experience = db.Column(db.String, index=True, nullable=False)
    audience = db.Column(db.String, index=True, nullable=False)
    is_mentor = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    # Define relationship to profile
    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __str__(self):
        return self.first_name

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="profile")
    competence = db.Column(db.String)
    language = db.Column(db.String)
    site_url = db.Column(db.String)
    twitter_url = db.Column(db.String)
    facebook_url = db.Column(db.String)
    linkedin_url = db.Column(db.String)
    youtube_url = db.Column(db.String)
    image = db.Column(db.String)
    is_hidden = db.Column(db.Boolean, default=False)
    is_hidden_courses = db.Column(db.Boolean, default=False)
    promotions = db.Column(db.Boolean, default=False)
    mentor_ads = db.Column(db.Boolean, default=False)
    email_ads = db.Column(db.Boolean, default=False)
