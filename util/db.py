# 1. Import necessary libraries
import sqlite3 as sql
import json

conn: sql.Connection = None
# 1. Update the `create_database_and_table` function to create a "users" table
def create_database_and_tables():
    global conn
    conn = sql.connect("messages.db")
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS messages
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, sender_id TEXT, message TEXT)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users
                   (user_id TEXT PRIMARY KEY, last_output TEXT)"""
    )
    conn.commit()
    return conn


create_database_and_tables()


# 2. Update the `save_message_to_database` function to handle separate tables for messages and users
def save_message_to_database(user_id, message, sender_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (user_id, sender_id, message) VALUES (?, ?, ?)",
        (user_id, sender_id, message),
    )
    conn.commit()


def update_user_last_output(user_id, output):
    output_as_json = json.dumps(output)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO users (user_id, last_output) VALUES (?, ?)",
        (user_id, output_as_json),
    )
    conn.commit()

def get_last_msgs(user_id, n=5):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user_id, n),
    )
    msgs = cur.fetchall()
    return msgs

def get_last_context(user_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT last_output FROM users WHERE user_id = ?",
        (user_id,),
    )
    context = cur.fetchone()
    if context:
        return json.loads(context[0])
    else:
        return None
