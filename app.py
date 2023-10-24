# from aiohttp import request
from flask import Flask, redirect, render_template, request, url_for
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


# Enviroment Variables ----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI =os.getenv('REDIRECT_URI')
STATE = os.getenv('PARAMETERS_STATE')
# Session secret key
app.secret_key = os.getenv('APP_SECRET_KEY')

# LinkedIn API URLs - Endpoints -------------------------------------------------------------------
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USER_INFO_URL = 'https://api.linkedin.com/v2/me'

# Routes  -----------------------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
    first_name = "John"
    stuff = "This is <strong> Bold </strong> Text"
    return render_template("index.html", first_name=first_name, stuff=stuff)

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404
# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html"), 500
@app.route('/privacypolicy')
def privacypolicy():
    return render_template("privacypolicy.html")
#ADMIN ROUTES ----------------------------------------------------------------------------------------------------------------------------------

@app.route('/search')
def search():
    return render_template("admin_routes/search.html")

@app.route('/feed')
def feed():
    return render_template("admin_routes/feed.html")

@app.route('/introduction')
def introduction():
    return render_template("admin_routes/introduction.html")

@app.route('/lists')
def lists():
    return render_template("admin_routes/lists.html")

@app.route('/admin')
def admin():
    return render_template("admin_routes/admin.html")

@app.route('/credits')
def credits():
    return render_template("admin_routes/credits.html")

@app.route('/user/<name>')
def user(name):
    return render_template("admin_routes/user.html", name=name)

#LINKEDIN ROUTES ----------------------------------------------------------------------------------------------------------------------------------

@app.route('/linkedin_signin')
def linkedin_signin():
    # RedirectING the user to LinkedIn's authentication page
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': STATE,
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
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,

        }
        response = requests.post(TOKEN_URL, data=token_data)
        access_token = response.json().get('access_token')

        print(f'-------------------------------------------------------{access_token}')

        # Using access token to get user info
        headers = {
            'Authorization': f'Bearer {access_token}',
        }        
        user_info_response = requests.get(USER_INFO_URL, headers=headers)
        
        user_info = user_info_response.json()
        print(f'-------------------------------------------------------{user_info}')

        error = request.args.get('error')
        error_description = request.args.get('error_description')
    
        error_params={
            'error_name': error,
            'error_desc': error_description,
            'state': STATE,
        }
        error_url =  f"{REDIRECT_URI}?{'&'.join([f'{k}={v}' for k, v in error_params.items()])}"

        user_name = user_info.get('name', 'User')
        return redirect(url_for('user', name=user_name))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)