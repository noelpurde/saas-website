# from aiohttp import request
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os 
from dotenv import load_dotenv
import psycopg2


app = Flask(__name__)

# Enviroment Variables ----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

# Database url
URL = os.getenv('DATABASE_URL')

# Linkedin Secret Stuff
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI =os.getenv('REDIRECT_URI')
STATE = os.getenv('PARAMETERS_STATE')

# Session secret key
app.secret_key = os.getenv('APP_SECRET_KEY')


# Add database  -----------------------------------------------------------------------------------------------------------------------------------

connection = psycopg2.connect(URL)

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, name TEXT,title TEXT, company TEXT, region TEXT, company_size TEXT, function TEXT, product_bought TEXT, email TEXT);"
)
INSERT_USERS_RETURN_ID = (
    "INSERT INTO users (name, title, company, region, company_size, function, product_bought, email) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_id;"
)



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
#ADMIN PURPLE NAVBAR ROUTES -----------------------------------------------------------------------

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

#USER SETTINGS ROUTES -----------------------------------------------------------------------------

@app.route('/user-settings/integrations')
def integrations():
    return render_template('user_settings/integrations.html')

@app.route('/user-settings/team')
def team():
    return render_template('user_settings/team.html')

@app.route('/user-settings/notifications')
def notifications():
    return render_template('user_settings/notifications.html')

@app.route('/user-settings/ team_settings')
def team_settings():
    return render_template('user_settings/team_settings.html')

@app.route('/user-settings/profile_settings')
def profile_settings():
    return render_template('user_settings/profile_settings.html')

@app.route('/user-settings/reports')
def reports():
    return render_template('user_settings/reports.html')

@app.route('/user-settings/billing')
def billing():
    return render_template('user_settings/billing.html')

#LINKEDIN ROUTES ----------------------------------------------------------------------------------

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

@app.route('/database_testing', methods=['POST'])
def database_testing():
    # Database Users Table Population
    if request.method == 'POST':

        data = request.get_json()
        name = data["name"]
        title = data["title"]
        company = data["company"]
        region = data["region"]
        company_size = data["company_size"]
        function = data["function"]
        product_bought = data["product_bought"]
        email = data["email"]

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(CREATE_USERS_TABLE)
                cursor.execute(INSERT_USERS_RETURN_ID, (name, title, company, region, company_size, function, product_bought, email))
    return jsonify({"response": "Request Succesful"})


if __name__ == "__main__":
    app.run(debug=True)