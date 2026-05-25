from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# Home page
@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()

    conn.close()

    return render_template('index.html', notes=notes)

# Add note
@app.route('/add_note', methods=['POST'])
def add_note():

    data = request.get_json()

    note = data.get('note')

    if note == "":
        return jsonify({"message": "Empty note"}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note Saved Successfully"})


if __name__ == '__main__':
    app.run(debug=True)