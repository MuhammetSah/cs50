import sqlite3
from flask import Flask, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__) 
app.secret_key = 'project-portfolio'
CORS(app, supports_credentials=True)

connection = sqlite3.connect('tickets.db')
cursor = connection.cursor()

# CREATE TABLE for SQL 
# TABLE for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL
    )
''')

# TABLE for tickets
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

connection.commit()
connection.close()

# Get all tickets
@app.route('/tickets', methods=['GET'])
def get_tickets():
    connection = sqlite3.connect('tickets.db') # Connect to the database
    connection.row_factory = sqlite3.Row # Set the row factory to sqlite3.Row to access columns by name
    cursor = connection.cursor()  # Create a cursor object to execute SQL queries
    cursor.execute('SELECT * FROM tickets') # Query to select all tickets
    tickets = cursor.fetchall() # Fetch all tickets from the database
    connection.close() # Close the database connection
    return jsonify([dict(ticket) for ticket in tickets]) # Convert the tickets to a list of dictionaries and return as JSON

# Create a new ticket
@app.route('/tickets', methods=['POST'])
def create_ticket():
    print("Session data_", dict(session))
    user_id = session.get('user_id') # Get the user_id from the session to check if the user is logged in
    if not user_id: # If the user is not logged in, return a 401 Unauthorized response
        return jsonify({'message': 'User not logged in'}), 401

    data = request.get_json() # Get the JSON data from the request body
    title = data.get('title') # Get the title of the ticket from the JSON data
    description = data.get('description') # Get the description of the ticket from the JSON data
    connection = sqlite3.connect('tickets.db') 
    cursor = connection.cursor() 
    cursor.execute('INSERT INTO tickets (user_id, title, description, status) VALUES (?, ?, ?, ?)', (user_id, title, description, 'open')) # Insert a new ticket into the tickets table with the user_id, title, description, and status set to 'open'
    connection.commit()
    connection.close()
    return jsonify({'message': 'Ticket created successfully'}), 201 # Return a 201 Created response with a success message

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username') # Get the username from the JSON data
    password = data.get('password') # Get the password from the JSON data
    connection = sqlite3.connect('tickets.db') 
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,)) # Check if the username already exists in the users table
    existing_user = cursor.fetchone() 
    if existing_user: # If the username already exists, return a 400 Bad Request response with an error message
        connection.close()
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password) # Hash the password using Werkzeug's generate_password_hash function for secure storage
    cursor.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (username, hashed_password)) # Insert the new user into the users table with the username and hashed password
    connection.commit()
    connection.close()
    return jsonify({'message': 'User created successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    connection = sqlite3.connect('tickets.db')
    connection.row_factory = sqlite3.Row # Set the row factory to sqlite3.Row to access columns by name
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,)) # Query to select the user with the given username
    existing_user = cursor.fetchone() 
    if not existing_user: # If the user does not exist, return a 401 Unauthorized response with an error message
        connection.close()
        return jsonify({'message': 'Invalid username or password'}), 401

    if not check_password_hash(existing_user['hash'], password): # If the password does not match the hashed password in the database, return a 401 Unauthorized response with an error message
        connection.close()
        return jsonify({'message': 'Invalid username or password'}), 401
    
    session['user_id'] = existing_user['id'] # Store the user_id in the session to keep the user logged in
    connection.close()
    return jsonify({'message': 'Login successful'}), 200 

# User logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) # Remove the user_id from the session to log the user out
    return jsonify({'message': 'Logout successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
