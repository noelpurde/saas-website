import os, json, sql
from dotenv import load_dotenv
from psycopg2 import sql
import psycopg2

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
        eraseContent = sql.SQL("""
            DELETE FROM filters_storage
        """)
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
        cursor.execute(eraseContent)
        return result

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection:
            cursor.close()
            connection.close()