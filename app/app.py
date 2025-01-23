from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database configuration from environment variables
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "dbname": os.getenv("DB_NAME", "mydb"),
}

def get_db_connection():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(**db_config)
    return conn

@app.route("/")
def home():
    return "Welcome to the Dockerized Flask App!"

@app.route("/initdb")
def init_db():
    """Initialize the database with a sample table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return "Database initialized!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/users")
def get_users():
    """Fetch all users from the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/add/<name>")
def add_user(name):
    """Add a new user to the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (%s);", (name,))
        conn.commit()
        cur.close()
        conn.close()
        return f"User '{name}' added!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
