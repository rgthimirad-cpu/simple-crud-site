from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# ✅ Render persistent disk
BASE_DIR = "/var/data"
os.makedirs(BASE_DIR, exist_ok=True)
DB_PATH = os.path.join(BASE_DIR, "data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_table():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ✅ RUN ON IMPORT (Flask 3 compatible)
ensure_table()

@app.route("/", methods=["GET", "POST"])
def home():
    ensure_table()  # 🔥 GUARANTEE table exists

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
