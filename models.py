from flask_sqlalchemy import SQLAlchemy

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


