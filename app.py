# from aiohttp import request
from flask import Flask, redirect, render_template, request, url_for, jsonify, session, g
from datetime import datetime
from dotenv import load_dotenv
from filters_filling import create_filters_tables
from filtered_search import search_query_real_time_refresh, create_or_replace_table, filter_data_from_database, add_to_list, geography_filters_data_selection, headcount_filters_data_selection, function_filters_data_selection, show_list_content
import requests, os, json, psycopg2
from models.models import db, Users, Teams, TeamUsers, Invitations, Introductions, Notifications, Subscriptions, Connections
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Enviroment Variables ----------------------------------------------------------------------------------------------------------------------------

load_dotenv()

# Database url
DATABASE_URL = os.getenv("DATABASE_URL")  # or other relevant config var
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

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

    lists_data = show_list_content(session['user_id'])
    print("LIST DATA", lists_data)
    return render_template("admin_routes/lists.html", lists_data=lists_data)
 
@app.route('/admin')
def admin():
    return render_template("admin_routes/admin.html")

@app.route('/credits')
def credits():
    return render_template("admin_routes/credits.html")

@app.route('/user')
def user():
    # Retrieve the user name from the session
    user_name = session.get('user_name')

    # Check if the user name is present in the session
    if user_name is not None:
        # Replace spaces with underscores
        user_name_url = user_name.replace(" ", "_")
        return redirect(url_for('user_profile', name=user_name_url))
    else:
        # Handle the case where the user name is not available in the session
        return redirect(url_for('index'))  # Redirect to the home page or handle appropriately

@app.route('/user/<name>')
def user_profile(name):
    # Replace underscores with spaces for displaying the user name
    user_name_display = name.replace("_", " ")
    return render_template("admin_routes/user.html", name=user_name_display)

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
    # Save Filters in Session
    session['filters'] = filters
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
@app.route('/lists_insert', methods=['GET'])
def lists_insert():
    session['filters']
    print("SAVE TO LIST")
    if not session['filters']["geography"] and not session['filters']["headcount"] and not session['filters']["function"]:
        print("No Filters Selected")
    else:
        add_to_list(session['filters'], session['user_id'], "List Name")
        print("[/save_to_list]:Saved Filters", session['filters'])
    response_data = {"message": "Filters saved successfully"}
    return jsonify(response_data)

@app.route("/lists_update", methods=["POST", "GET"])
def list_update():
    try:
        if request.method == "POST":
            list_id = request.form.get('id')
            name = request.form.get('name')
            alerts = request.form.get('alerts')
        else:
            list_id = request.args.get('list_id')
            name = request.args.get('name')
            alerts = request.args.get('alerts')

        print("List ID:", list_id)
        print("Name:", name)
        print("Alerts:", alerts)

        # Validate the received values
        if list_id and name and alerts:
            # Update the list
            my_list = db.Lists.query.get(list_id)
            if my_list:
                my_list.name = name
                my_list.alerts = alerts
                db.session.commit()
                return "Update successful"
            else:
                return "List not found"
        else:
            return "Error while updating list: Invalid data"
        
    except Exception as e:
        print(e)
        return "Error while updating list"
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
        'scope': 'openid profile w_member_social email',
    }
    auth_url = f"{AUTHORIZATION_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
        }

        # Print or log the token response for debugging
        response = requests.post(TOKEN_URL, data=token_data)
        print("TOKEN RESPONSE:", response.json())
        access_token = response.json().get('access_token')

        headers = {
            'Authorization': f'Bearer {access_token}',
        }        
        user_info_response = requests.get(USER_INFO_URL, headers=headers)

        # Print or log the user info response for debugging
        user_info = user_info_response.json()
        print("USER INFO-------------------------------------------------------", user_info)
        linkedin_user_id = user_info.get('sub')  # Using 'sub' as the LinkedIn user ID field

        # Check if the user already exists in the database
        user = Users.query.filter_by(linkedin_user_id=linkedin_user_id).first()

        if not user:
            # User doesn't exist, create a new user record
            new_user = Users(
                linkedin_user_id=linkedin_user_id,
                name=user_info.get('name'),
                email=user_info.get('email'),
                profile_picture=user_info.get('picture')
            )
            db.session.add(new_user)
            db.session.commit()
        else:
            # User exists, update user details
            user.name = user_info.get('name')
            user.email = user_info.get('email')
            user.profile_picture = user_info.get('picture')
            db.session.commit()

        # Store user information in the session for future use (if needed)
        session['user_id'] = user.user_id if user else new_user.user_id
        session['user_name'] = user.name if user else new_user.name
        session['user_emai  l'] = user.email if user else new_user.email
        session['user_profile_picture'] = user.profile_picture if user else new_user.profile_picture

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
