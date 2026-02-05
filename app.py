from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Always use absolute path (VERY IMPORTANT for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    # 🔥 ENSURE TABLE EXISTS ON EVERY REQUEST
    ensure_table()

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        return redirect("/")

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()

    return render_template("index.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):
    ensure_table()
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    ensure_table()
    name = request.form["name"]
    conn = get_db()
    conn.execute("UPDATE users SET name = ? WHERE id = ?", (name, id))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run()
