import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

# Database url
URL = os.getenv('DATABASE_URL')

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
