import requests
import sqlite3

BASE_URL = 'https://api.openbrewerydb.org/v1/breweries'
DB_NAME = 'breweries_simple.db'

def get_breweries():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json()
    return []

def create_database():
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS breweries (
        id TEXT PRIMARY KEY,
        name TEXT,
        brewery_type TEXT,
        address_1 TEXT,
        city TEXT,
        state_province TEXT,
        postal_code TEXT,
        country TEXT,
        longitude REAL,
        latitude REAL,
        phone TEXT,
        website_url TEXT,
        street TEXT
    )
    ''')

    conn.commit()
    conn.close()

def connect_to_database():
    return sqlite3.connect(DB_NAME)

def save_breweries_to_database(breweries):
    conn = connect_to_database()
    cursor = conn.cursor()

    for brewery in breweries:
        cursor.execute('''
        INSERT OR REPLACE INTO breweries (
            id, name, brewery_type, address_1, city, state_province, postal_code, 
            country, longitude, latitude, phone, website_url, street
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            brewery.get('id'),
            brewery.get('name'),
            brewery.get('brewery_type'),
            brewery.get('address_1'),
            brewery.get('city'),
            brewery.get('state_province'),
            brewery.get('postal_code'),
            brewery.get('country'),
            brewery.get('longitude'),
            brewery.get('latitude'),
            brewery.get('phone'),
            brewery.get('website_url'),
            brewery.get('street')
        ))

    conn.commit()
    conn.close()

def main():
    create_database()
    breweries = get_breweries()
    
    if breweries:
        save_breweries_to_database(breweries)
    else:
        print("Nenhuma cervejaria encontrada.")

if __name__ == '__main__':
    main()
