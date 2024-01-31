# from aiohttp import request
from flask import Flask, redirect, render_template, request, url_for, jsonify, session, g
from datetime import datetime
from dotenv import load_dotenv
from filters_filling import create_filters_tables
from filtered_search import search_query_real_time_refresh, create_or_replace_table, filter_data_from_database, add_to_list, geography_filters_data_selection, headcount_filters_data_selection, function_filters_data_selection
import requests, os, json, psycopg2
from models.models import db, Users, Teams, TeamUsers, Invitations, Introductions, Notifications, Subscriptions, Connections
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Enviroment Variables ----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

# Database url
DATABASE_URL = os.getenv('DATABASE_URL')

# LinkedIn Secret Stuff
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
STATE = os.getenv('PARAMETERS_STATE')

# Session secret key
app.secret_key = os.getenv('APP_SECRET_KEY')

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


with app.app_context():
    # Query all users
    users = Users.query.all()
    print("Users: ", users)

# Add database  -----------------------------------------------------------------------------------------------------------------------------------
connection = psycopg2.connect(DATABASE_URL)

# Database filters jinja template creation
create_filters_tables()

# LinkedIn API URLs - Endpoints -------------------------------------------------------------------
AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
USER_INFO_URL = 'https://api.linkedin.com/v2/userinfo'

# Routes  -----------------------------------------------------------------------------------------------------------------------------------------
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(DATABASE_URL)
    return g.db

@app.route('/')
def index():
     # MAIN SCREEN MAP FILTERS
        with get_db(), get_db().cursor() as cursor:

            # Filter Geography
            geography_data = geography_filters_data_selection()

                # Filter Company Headcount
            headcount_data = headcount_filters_data_selection()

                # Filter Function
            function_data = function_filters_data_selection()


            cursor.execute("SELECT COUNT(*) AS user_count FROM users;")
            result = cursor.fetchone()
            champion_number = int(result[0])
            

        # Render the data using Jinja2 template and save it to table.html
        return render_template("index.html", geography_data=geography_data, headcount_data=headcount_data,function_data=function_data, champion_number = champion_number)

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

@app.route('/search', methods=['GET'])
def search():
    # FETCH DATA FROM THE DATABASE FOR THE OPTIONS IN FILTERS SEARCH.HTML
    with get_db(), get_db().cursor() as cursor:
        # Users Data
        cursor.execute("SELECT * FROM users;")
        users_data = cursor.fetchall()
        # Filter Geography
        geography_data = geography_filters_data_selection()

        # Filter Company Headcount
        headcount_data = headcount_filters_data_selection()

        # Filter Function
        function_data = function_filters_data_selection()

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

@app.route('/admin/integrations')
def integrations():
    return render_template('user_settings/integrations.html')

@app.route('/admin/team')
def team():
    return render_template('user_settings/team.html')

@app.route('/admin/notifications')
def notifications():
    return render_template('user_settings/notifications.html')

@app.route('/admin/ team_settings')
def team_settings():
    return render_template('user_settings/team_settings.html')

@app.route('/admin/profile_settings')
def profile_settings():
    return render_template('user_settings/profile_settings.html')

@app.route('/admin/reports')
def reports():
    return render_template('user_settings/reports.html')

@app.route('/admin/billing')
def billing():
    return render_template('user_settings/billing.html')


# BACKCHANNEL BUTTON LOGIN CHECK FOR REDIRECTION TO ADMIN PAGE
@app.route('/update_data', methods=['POST'])
def update_data():
    filters = request.json

    # Build the query based on the filters
    filtered_data=search_query_real_time_refresh(filters)
    length = len(filtered_data)
    print("[/updated_data]:Filtered Data: ", filtered_data)
    # print("The length is:", len(filtered_data))
    return jsonify({'filtered_data': filtered_data, 'length': length})

# FITLERED SEARCH ADMIN PAGE -> PASSING DATA FROM FILTERS TO JAVASCRIPT FOR LOADING TABLE COLUMNS
@app.route('/backchannel_button_data', methods=['POST', 'GET'])
def backchannel_button_data():

    filters = request.json
    print("BCH_BTN_DATA: ", filters)
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
    return jsonify(data)  

# Deletes the filters_storage filters after pressing Start Backchanneling
@app.route('/delete_table', methods=['POST'])
def delete_table():

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM filters_storage")
        connection.commit()  # Commit the changes
    except Exception as e:
        print(f"Error during database operation: {e}")
    finally:
        cursor.close()
        connection.close()
    return jsonify("Empty Text")

# Saves filters from search to lists
@app.route('/save_to_list', methods=["POST"])
def save_to_list_method():
    if request.method == 'POST':
        filters = request.json
        print("[/save_to_list]:Saved Filters", filters)
        add_to_list(filters, "1")
        response_data = {"message": "Filters saved successfully"}
        return jsonify(response_data)
    else:
        return jsonify({"message": "Unsupported method"})

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
        'scope': 'profile',
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
        print("USER INFO-------------------------------------------------------", user_info)
        linkedin_user_id = user_info.get('id')  # Assuming 'id' is the LinkedIn user ID field

        # Check if the user already exists in the database
        user = Users.query.filter_by(linkedin_user_id=linkedin_user_id).first()

        if not user:
            # User doesn't exist, create a new user record
            user = Users(linkedin_user_id=linkedin_user_id, name=user_info.get('localizedFirstName'),
                          email=user_info.get('email'))
            db.session.add(user)
            db.session.commit()

        # Store user information in the session for future use (if needed)
        session['user_id'] = user.user_id

        return redirect(url_for('search'))
    else:
        return redirect(url_for('index'))

# ADD USERS TO DATABASE
@app.route('/add_user', methods=['POST'])
def database_testing():
    data = request.get_json()
    new_user = Users(
        name=data['name'],
        linkedin_id=data['linkedin_id'],
        title=data['title'],
        company=data['company'],
        region=data['region'],
        company_size=data['company_size'],
        function=data['function'],
        product_bought=data['product_bought'],
        email=data['email']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.user_id})

if __name__ == '__main__':
    debug=True