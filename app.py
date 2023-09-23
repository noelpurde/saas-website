from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Add database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
# Secret Key
app.config['SECRET_KEY']='secret key'
# Init Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    #Create a String
    def __repr__(self):
        return '<Name %r>' % self.name



@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong> Bold </strong> Text"
    return render_template("index.html", first_name=first_name, stuff=stuff)

# localhost:500/user/Noel
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)