import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

def get_items():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="jeans"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jeanData")
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return items

@app.route("/")
def home():
    items = get_items()
    return render_template("index.html", items=items)


if __name__ == "__main__":
    app.run(debug=True)
