
import sqlite3
import hashlib

# Function to hash the password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a database and a users table
def create_db_and_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create a table for users if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

# Function to create a new user account (Sign Up)
def signup():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    username = input("Enter a new username: ")
    password = input("Enter a new password: ")
    

    # Hash the password
    hashed_password = hash_password(password)
    
    try:
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("Signup successful! You can now log in.")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    
    conn.close()

# Function to login an existing user
def login():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # Hash the input password
    hashed_password = hash_password(password)
    
    # Query the database to check if the user exists
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    
    if user:
        print("Login successful!")

        return True
    else:
        print("Login failed. Incorrect username or password.")
        return False

    conn.close()

# Main function to choose between signup and login
def main():
    # Create the database and table if they don't exist
    create_db_and_table()
    
    while True:
        choice = input("Do you want to (1) Sign up or (2) Login? (q to quit): ").strip().lower()
        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()

