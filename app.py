# from aiohttp import request
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os 
from dotenv import load_dotenv


app = Flask(__name__)

# Add database  -----------------------------------------------------------------------------------------------------------------------------------
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
    
    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name


# Linkedin Access --------------------------------------------------------------------------------------------------------------------------

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI =os.getenv('REDIRECT_URI')

# Session secret key
app.secret_key = 'd501039709f9dd179b87310405113491d14ac0e877c51e97'

# LinkedIn API URLs
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USER_INFO_URL = 'https://api.linkedin.com/v2/me'

# Routes  -----------------------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong> Bold </strong> Text"
    return render_template("index.html", first_name=first_name, stuff=stuff)
# localhost:500/user/Noel
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
#LINKEDIN ROUTES ---------------------------------------------------------------------------------------------------------------------

@app.route('/linkedin_signin')
def linkedin_signin():
    # RedirectING the user to LinkedIn's authentication page
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'profile w_member_social',  # Update with desired permissions
    }
    auth_url = f"{AUTHORIZATION_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Callback handling from LinkedIn
    code = request.args.get('code')
    if code:
        # The authorization code for an access token exchange
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        response = requests.post(TOKEN_URL, data=token_data)
        access_token = response.json().get('access_token')

        # Using access token to get user info
        headers = {
            'Authorization': f'Bearer {access_token}',
        }        
        user_info_response = requests.get(USER_INFO_URL, headers=headers)
        
        user_info = user_info_response.json()

        # Use 'user_info' to access the LinkedIn user's profile info

        return redirect(url_for('index'))
    else:
        return 'Authorization failed'


if __name__ == "__main__":
    app.run(debug=True)