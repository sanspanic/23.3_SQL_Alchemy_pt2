from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app): 
    db.app = app
    db.init_app(app)

class User(db.Model): 
    """user model"""

    __tablename__ = 'users'

    def __repr__(self): 
        u = self
        return f"<user_id = {u.id}, first_name = {u.first_name}, last_name = {u.last_name}"

    id = db.Column(db.Integer, 
                    primary_key = True, 
                    autoincrement = True)

    first_name = db.Column(db.String(20), 
                        nullable = False)

    last_name = db.Column(db.String(30), 
                        nullable = False)
    
    img_url = db.Column(db.String, 
                        nullable = False, 
                        unique = True)

    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @property
    def full_name(self): 
        """returns string of full name"""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

class Post(db.Model): 
    """blog post model"""

    __tablename__ = 'posts'

    def __repr__(self): 
        p = self
        return f"post_id = {p.id}, title = {p.title}, content = {p.content}, created_at = {p.created_at} by user with id {p.user_id}"

    id = db.Column(db.Integer, 
                    primary_key = True, 
                    autoincrement = True)

    title = db.Column(db.String(70), 
                        nullable = False)

    content = db.Column(db.String, 
                        nullable = False)
    
    created_at = db.Column(db.DateTime, 
                        nullable = False, 
                        default = datetime.now())
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'), 
                        nullable=False)

    @property
    def prettified_date(self): 
        """returns nicely formatted string of date and time post was created"""
        date = str(self.created_at)
        date_time_list = date[0:-7].split(' ')
        return f"{date_time_list[0]} at {date_time_list[1]}"
    


