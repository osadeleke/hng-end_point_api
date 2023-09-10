from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

stageTwo = Flask(__name__)
CORS(stageTwo)

# SQLite database configuration
DB_NAME = 'database.db'

# Create a database table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create a new person
@stageTwo.route('/api', methods=['POST'])
def create_person():
    try:
        data = request.get_json()
        name = data['name']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO persons (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Person created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Get all persons
@stageTwo.route('/api', methods=['GET'])
def get_all_persons():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persons")
    persons = cursor.fetchall()
    conn.close()

    person_list = []
    for person in persons:
        person_dict = {
            'id': person[0],
            'name': person[1],
        }
        person_list.append(person_dict)

    return jsonify(person_list)

# Get a specific person by ID
@stageTwo.route('/api/<string:person_name>', methods=['GET'])
def get_person(person_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persons WHERE name=?", (person_name,))
    person = cursor.fetchone()
    conn.close()

    if person:
        person_dict = {
            'id': person[0],
            'name': person[1],
        }
        return jsonify(person_dict)
    else:
        return jsonify({'message': 'Person not found'}), 404

# Update a specific person by ID
@stageTwo.route('/api/<string:person_name>', methods=['PUT'])
def update_person(person_name):
    try:
        data = request.get_json()
        name = data['name']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE persons SET name=? WHERE name=?", (name, person_name))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Person updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete a specific person by ID
@stageTwo.route('/api/<string:person_name>', methods=['DELETE'])
def delete_person(person_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM persons WHERE name=?", (person_name,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Person deleted successfully'})

if __name__ == '__main__':
    create_table()
    stageTwo.run(debug=True)
