import os
from dotenv import load_dotenv

import psycopg2

load_dotenv()

# Database url
URL = os.getenv('DATABASE_URL')

def create_filters_tables():
    conn = psycopg2.connect(URL)
    cur = conn.cursor()


#-------------------- GEOGRAPHY FILTERS TABLE --------------------
    cur.execute('''
        CREATE TABLE IF NOT EXISTS filters_geography (
            geography_name TEXT
        );
    ''')

    geography_data = [
        'Oceania',
        'EMEA',
        'DACH',
        'North America',
        'Benelux',
        'APJ',
        'APAC',
        'Asia',
        'Nordics',
        'MENA',
        'Europe',
        'Africa',
        'South America'
    ]

    # Loop through geography_data and insert only if the value does not already exist
    for geography in geography_data:
        cur.execute('SELECT * FROM filters_geography WHERE geography_name = %s', (geography,))
        existing_geography = cur.fetchone()
        if not existing_geography:
            cur.execute('INSERT INTO filters_geography (geography_name) VALUES (%s)', (geography,))


#------------------COMPANY HEADCOUNT FILTERS TABLE ---------------

    cur.execute('''
        CREATE TABLE IF NOT EXISTS filters_headcount (
            headcount_name TEXT
        )
    ''')

    headcount_data = [
        'Self-employed',
        '1-10',
        '11-50',
        '51-200',
        '201-500',
        '501-1,000',
        '1,001-5,000',
        '5,001-10,000',
        '10,001+'
    ]

    # Loop through headcount_data and insert only if the value does not already exist
    for headcount in headcount_data:
        cur.execute('SELECT * FROM filters_headcount WHERE headcount_name = %s', (headcount,))
        existing_headcount = cur.fetchone()
        if not existing_headcount:
            cur.execute('INSERT INTO filters_headcount (headcount_name) VALUES (%s)', (headcount,))


#-------------------- FUNCTION FILTERS TABLE ---------------------

    cur.execute('''
        CREATE TABLE IF NOT EXISTS filters_function (
           function_name TEXT
        )
    ''')

    function_data = [
        'Accounting',
        'Administrative',
        'Arts and Design',
        'Business Development',
        'Community and Social Services',
        'Consulting',
        'Customer Success and Support',
        'Education',
        'Engineering',
        'Entrepreneurship',
        'Finance',
        'Healthcare Services',
        'Human Resources',
        'Information Technology',
        'Legal',
        'Marketing',
        'Media and Communication',
        'Military and Protective Services',
        'Operations',
        'Product Management',
        'Program and Project Management',
        'Purchasing',
        'Quality Assurance',
        'Real Estate',
        'Research',
        'Sales'
    ]

    for function in function_data:
        cur.execute('SELECT * FROM filters_function WHERE function_name = %s', (function,))
        existing_function = cur.fetchone()
        if not existing_function:
            cur.execute('INSERT INTO filters_function (function_name) VALUES (%s)', (function,))

    conn.commit()
    conn.close()

