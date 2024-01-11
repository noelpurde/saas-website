# from aiohttp import request
from flask import Flask, redirect, render_template, request, url_for, jsonify, session, g
from datetime import datetime
from dotenv import load_dotenv
from filters_filling import create_filters_tables
from filtered_search import search_query_real_time_refresh, create_or_replace_table, filter_data_from_database
import requests, os, json, psycopg2

from models.models import db, Users
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Enviroment Variables ----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

# Database url
DATABASE_URL = os.getenv('DATABASE_URL')

# Linkedin Secret Stuff
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI =os.getenv('REDIRECT_URI')
STATE = os.getenv('PARAMETERS_STATE')

# Session secret key
app.secret_key = os.getenv('APP_SECRET_KEY')

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

with app.app_context():
    # Query all users
    users = Users.query.all()
    print(users)

# Add database  -----------------------------------------------------------------------------------------------------------------------------------
connection = psycopg2.connect(DATABASE_URL)

INSERT_USERS_RETURN_ID = (
    "INSERT INTO users (name, title, company, region, company_size, function, product_bought, email)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING user_id;"
)

# Database filters jinja template creation
create_filters_tables()



# LinkedIn API URLs - Endpoints -------------------------------------------------------------------
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USER_INFO_URL = 'https://api.linkedin.com/v2/me'

# Routes  -----------------------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def index():
     # MAIN SCREEN MAP FILTERS
        with connection:
            with connection.cursor() as cursor:
                # Filter Geography
                cursor.execute("SELECT * FROM filters_geography;")
                geography_data = cursor.fetchall()
                 # Filter Company Headcount
                cursor.execute("SELECT * FROM filters_headcount;")
                headcount_data = cursor.fetchall()
                 # Filter Function
                cursor.execute("SELECT * FROM filters_function;")
                function_data = cursor.fetchall()
        

        # Render the data using Jinja2 template and save it to table.html
        return render_template("index.html", geography_data=geography_data, headcount_data=headcount_data,function_data=function_data )

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

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

@app.route('/search', methods=['GET'])
def search():
    # FETCH DATA FROM THE DATABASE FOR THE OPTIONS IN FILTERS SEARCH.HTML
    with get_db(), get_db().cursor() as cursor:
        # Users Data
        cursor.execute("SELECT * FROM users;")
        users_data = cursor.fetchall()
        # Filter Geography
        cursor.execute("SELECT * FROM filters_geography;")
        geography_data = cursor.fetchall()
        # Filter Company Headcount
        cursor.execute("SELECT * FROM filters_headcount;")
        headcount_data = cursor.fetchall()
        # Filter Function
        cursor.execute("SELECT * FROM filters_function;")
        function_data = cursor.fetchall()

    return render_template("admin_routes/search.html", users_data=users_data, geography_data=geography_data, headcount_data=headcount_data, function_data=function_data)


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


# BACKCHANNEL BUTTON LOGIN CHECK FOR REDIRECTION TO ADMIN PAGE
@app.route('/update_data', methods=['POST'])
def update_data():
    filters = request.json

    # Build the query based on the filters
    filtered_data=search_query_real_time_refresh(filters)
    length = len(filtered_data)
    print(filtered_data)
    # print("The length is:", len(filtered_data))
    return jsonify({'filtered_data': filtered_data, 'length': length})

# FITLERED SEARCH ADMIN PAGE -> PASSING DATA FROM FILTERS TO JAVASCRIPT FOR LOADING TABLE COLUMNS
@app.route('/backchannel_button_data', methods=['POST', 'GET'])
def backchannel_button_data():

    filters = request.json
    print("BCH_BTN", filters)
    create_or_replace_table(filters)
    return jsonify({'filtered_data': filters})
    
# BACKCHANNEL BUTTON FILTER 'GET' METHOD
@app.route('/backchannel_button')
def backchannel_button():
    if 'linkedin_token' in session:
        # Access the filters from the user's session
        return redirect(url_for('search'))
    else:
        return redirect(url_for('linkedin_signin'))
    
# BACKCHANNEL FILTER UPDATE FROM DATABASE TO JAVASCRIPT
@app.route('/filter_db_to_js_update', methods=['GET'])
def filter_db_to_js_update():
    data = filter_data_from_database()
    print("REQUIRED", data)
    return jsonify(data)  

     
#LINKEDIN ROUTES ----------------------------------------------------------------------------------

@app.route('/linkedin_signin')
def linkedin_signin():

    if 'linkedin_token' in session:
        # User is already logged in, redirect to a certain route
        return redirect(url_for('search'))
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
        # The authorization code for an access token exchangex
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,

        }
        response = requests.post(TOKEN_URL, data=token_data)
        access_token = response.json().get('access_token')

        # Using access token to get user info
        headers = {
            'Authorization': f'Bearer {access_token}',
        }        
        user_info_response = requests.get(USER_INFO_URL, headers=headers)
        
        user_info = user_info_response.json()

        error = request.args.get('error')
        error_description = request.args.get('error_description')
    
        error_params={
            'error_name': error,
            'error_desc': error_description,
            'state': STATE,
        }
        error_url =  f"{REDIRECT_URI}?{'&'.join([f'{k}={v}' for k, v in error_params.items()])}"



        return redirect(url_for('search'))
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

    return jsonify({"response": "Request Successful"})



if __name__ == '__main__':
    debug=True
