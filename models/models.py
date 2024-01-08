from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    company = db.Column(db.String)
    region = db.Column(db.String)
    company_size = db.Column(db.String)
    function = db.Column(db.String)
    product_bought = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"User ID: {self.user_id}, Name: {self.name}, Email: {self.email}"
