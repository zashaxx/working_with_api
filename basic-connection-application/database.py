import sqlite3
import hashlib


def init_database():
    conn = sqlite3.connect("clients.db")  # connects to the database
    cursor = conn.cursor()  # opens the created database

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS client (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) 
    """
        # only creates table if it does not already exist
    )

    conn.commit()  # saves changes
    conn.close()  # closes the connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # hashes password using sha256


def register_user(username, password):
    try:
        conn = sqlite3.connect("clients.db")  # connects to the database
        cursor = conn.cursor()  # opens the connected database

        password_hash = hash_password(
            password
        )  # hashes the provided password to store in database

        cursor.execute(
            "INSERT INTO client (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )  # inserts username and hashed password into the client table

        conn.commit()  # saves changes
        conn.close()  # closes the connection
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        return (
            False,
            "Username already exists!",
        )  # handles case where username already exists
    except Exception as e:
        return False, f"Error: {str(e)}"


def verify_user(username, password):
    try:
        conn = sqlite3.connect("clients.db")  # connects to the database
        cursor = conn.cursor()  # opens the connected database

        password_hash = hash_password(password)  # hashes the provided password
        cursor.execute(
            "SELECT * FROM client WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        )

        user = cursor.fetchone()  # fetches the first matching record
        conn.close()

        if user:
            return True, "Authentication successful!"
        else:
            return False, "Invalid credentials!"
    except Exception as e:
        return False, f"Error: {str(e)}"
