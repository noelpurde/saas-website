import os, json, sql
from dotenv import load_dotenv
from psycopg2 import sql
import psycopg2
from models.models import db, Users, Teams, TeamUsers, Invitations, Introductions, Notifications, Subscriptions, Connections, Lists
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


load_dotenv()

# Database url
URL = os.getenv('DATABASE_URL')

#-------------------------------------------------------------------------------
# FUNCTION TO SEARCH ELEMENTS IN THE FILTER SEARCH
def search_query_real_time_refresh(filters):
    conn = psycopg2.connect(URL)
    cur = conn.cursor()

    # Check if all filter arrays are empty
    if not any(filters.values()):
        return []

    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if 'geography' in filters and filters['geography']:
        query += " AND region IN %s"
        params.append(tuple(filters['geography']))

    if 'headcount' in filters and filters['headcount']:
        query += " AND company_size IN %s"
        params.append(tuple(filters['headcount']))

    if 'function' in filters and filters['function']:
        query += " AND function IN %s"
        params.append(tuple(filters['function']))

    # Execute the query
    with psycopg2.connect(URL) as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            result = cur.fetchall()
    return result

#-------------------------------------------------------------------------------
# DELETE AND CREATE TABLE FOR PASSING FILTERS LANDING PAGE -> SEARCH
def create_or_replace_table(filters):
    # Get the database URL from the environment variable
    DATABASE_URL = os.getenv('DATABASE_URL')

    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Table name
        table_name = 'filters_storage'

        # Drop the table if it exists
        cursor.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table_name)))

        # Create the table if not exists
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                geography TEXT,
                headcount TEXT,
                function TEXT
            )
        """).format(sql.Identifier(table_name))
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_data_query = sql.SQL("""
            INSERT INTO {} (geography, headcount, function)
            VALUES (%s, %s, %s)
        """).format(sql.Identifier(table_name))

        # Convert filters dictionary to text
        filters_text = {
            'geography': ",".join(map(str, filters.get('geography', []))),
            'headcount': ",".join(map(str, filters.get('headcount', []))),
            'function': ",".join(map(str, filters.get('function', [])))
        }

        # Execute the query
        cursor.execute(insert_data_query, (filters_text['geography'], filters_text['headcount'], filters_text['function']))

        # Commit the changes
        connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        if connection:
            cursor.close()
            connection.close()
#-------------------------------------------------------------------------------
# GETTING THE FILTERS FROM THE DATABASE TO THE JAVASCRIPT FILE FUNCTION FOR ROUTE

def filter_data_from_database():
    DATABASE_URL = os.getenv('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        table_name = 'filters_storage'

        select_data_query = sql.SQL("""
            SELECT geography, headcount, function FROM {}
        """).format(sql.Identifier(table_name))

        cursor.execute(select_data_query)
        data = cursor.fetchall()

        # Converting data to a list of dictionaries
        result = []
        for row in data:
            result.append({
                'geography': row[0].split(','),
                'headcount': row[1].split(','),
                'function': row[2].split(',')
            })
        cursor.execute("DELETE FROM filters_storage")
        print("FILTERS DELETED")
        print(cursor.execute("SELECT * FROM filters_storage"))

        return result

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()

# FUNCTION TO ADD FILTERS TO LIST "SAVE TO LIST" BUTTON IN SEARCH
            
def add_to_list(filters, user_id):
    try:
        # Create a new Lists instance
        new_list = Lists(
            user_id=user_id,
            geography=",".join(map(str, filters.get('geography', []))),
            headcount=",".join(map(str, filters.get('headcount', []))),
            function=",".join(map(str, filters.get('function', []))),
            created_at=datetime.utcnow()
        )

        # Add the new_list to the database
        db.session.add(new_list)
        db.session.commit()

        print("List added successfully.")

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()


# FILTERS SELECTED AND GREY NUMBER TEXT + 
                                                            ### GEOGRAPHY ###
def geography_filters_data_selection():
    DATABASE_URL = os.getenv('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        select_data_query = sql.SQL("""
            SELECT filters_geography.region, COUNT(users.user_id) as user_count
            FROM filters_geography
            LEFT JOIN users ON users.region = filters_geography.region
            GROUP BY filters_geography.region
            ORDER BY
            CASE filters_geography.region
                WHEN 'Oceania' THEN 1
                WHEN 'EMEA' THEN 2
                WHEN 'DACH' THEN 3
                WHEN 'North America' THEN 4
                WHEN 'Benelux' THEN 5
                WHEN 'APJ' THEN 6
                WHEN 'APAC' THEN 7
                WHEN 'Asia' THEN 8
                WHEN 'Nordics' THEN 9
                WHEN 'MENA' THEN 10
                WHEN 'Europe' THEN 11
                WHEN 'Africa' THEN 12
                WHEN 'South America' THEN 13
                ELSE 14 -- For any other regions not in the specified order
            END;
        """)

        cursor.execute(select_data_query)
        data = cursor.fetchall()
       
        return data

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()
                                                            ### HEADCOUNT ###
def headcount_filters_data_selection():
    DATABASE_URL = os.getenv('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        select_data_query = sql.SQL("""
            SELECT filters_headcount.company_size, COUNT(users.user_id) as user_count
            FROM filters_headcount
            LEFT JOIN users ON users.company_size = filters_headcount.company_size
            GROUP BY filters_headcount.company_size
            ORDER BY
            CASE filters_headcount.company_size
                WHEN 'Self-employed' THEN 1
                WHEN '1-10' THEN 2
                WHEN '11-50' THEN 3
                WHEN '51-200' THEN 4
                WHEN '201-500' THEN 5
                WHEN '501-1,000' THEN 6
                WHEN '1,001-5,000' THEN 7
                WHEN '5,001-10,000' THEN 8
                WHEN '10,001+' THEN 9
                ELSE 10 -- For any other sizes not in the specified order
            END;
        """)

        cursor.execute(select_data_query)
        data = cursor.fetchall()

        return data

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()
                                                            ### FUNCTION ###
def function_filters_data_selection():
    DATABASE_URL = os.getenv('DATABASE_URL')

    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        select_data_query = sql.SQL("""
            SELECT filters_function.function, COUNT(users.user_id) as user_count
            FROM filters_function
            LEFT JOIN users ON users.function = filters_function.function
            GROUP BY filters_function.function
            ORDER BY
            CASE filters_function.function
                WHEN 'Accounting' THEN 1
                WHEN 'Administrative' THEN 2
                WHEN 'Arts and Design' THEN 3
                WHEN 'Business Development' THEN 4
                WHEN 'Community and Social Services' THEN 5
                WHEN 'Consulting' THEN 6
                WHEN 'Customer Success and Support' THEN 7
                WHEN 'Education' THEN 8
                WHEN 'Engineering' THEN 9
                WHEN 'Entrepreneurship' THEN 10
                WHEN 'Finance' THEN 11
                WHEN 'Healthcare Services' THEN 12
                WHEN 'Human Resources' THEN 13
                WHEN 'Information Technology' THEN 14
                WHEN 'Legal' THEN 15
                WHEN 'Marketing' THEN 16
                WHEN 'Media and Communication' THEN 17
                WHEN 'Military and Protective Services' THEN 18
                WHEN 'Operations' THEN 19
                WHEN 'Product Management' THEN 20
                WHEN 'Program and Project Management' THEN 21
                WHEN 'Purchasing' THEN 22
                WHEN 'Quality Assurance' THEN 23
                WHEN 'Real Estate' THEN 24
                WHEN 'Research' THEN 25
                WHEN 'Sales' THEN 26
                ELSE 27 -- For any other functions not in the specified order
            END;
        """)

        cursor.execute(select_data_query)
        data = cursor.fetchall()

       
        return data

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()