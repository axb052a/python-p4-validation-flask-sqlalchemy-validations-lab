from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author must have a name.")
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and len(value) != 10:
            raise ValueError("Author phone numbers must be exactly ten digits.")
        return value

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

   
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Post must have a title.")
        
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]

        for keyword in clickbait_keywords:
            if keyword.lower() in value.lower():
                return value

        raise ValueError("Post title must be sufficiently clickbait-y, containing keywords like 'Won't Believe', 'Secret', 'Top', 'Guess'.")

    @validates('content')
    def validate_content(self, key, value):
        if value and len(value) <= 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) >= 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either Fiction or Non-Fiction.")
        return value
