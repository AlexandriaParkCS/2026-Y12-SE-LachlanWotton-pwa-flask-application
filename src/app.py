import logging
import json

from flask import Flask, jsonify, url_for
from flask import render_template
from flask import request
from flask import redirect
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header

import sqlite3
# OR
# from ormdb import OrmDb

log = logging.getLogger(__name__)
logging.basicConfig(
    filename="./runtime/log/app.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format=" %(asctime)s %(message)s",
)


# OR
# orm_db = OrmDb("../runtime/db/orm.db")

app = Flask(__name__)
app.secret_key = b"G6z115u8WnfQ0UIJ"  # To get a unique basic 16 key: https://acte.ltd/utils/randomkeygen

csrf = CSRFProtect(app)

# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)

@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    return render_template("/index.html")

@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")

@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return render_template("/dashboard.html")

@app.route("/task_viewer.html", methods=["GET"])
def task_viewer():
    return render_template("/task_viewer.html")

@app.route("/return_data/<query>", methods=["GET"])
def return_data(query):
    db = sqlite3.connect("./runtime/db/sql.db")
    cursor = db.cursor()
    if query == '*':
        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        # Get column names from the cursor description
        columns = [description[0] for description in cursor.description]
        # Convert the list of tuples (rows) into a list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]
        response = results
        app.logger.info(response)
        with open("dump.json", "w") as f:
            json.dump(results, f, indent=4)
    else:
        cursor.execute("SELECT * FROM tasks WHERE course = ?", query)
        rows = cursor.fetchall()
        # Get column names from the cursor description
        columns = [description[0] for description in cursor.description]
        # Convert the list of tuples (rows) into a list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]
        response = results
        app.logger.info(response)
        with open("dump.json", "w") as f:
            json.dump(results, f, indent=4)
    db.close()
    return response

@app.route("/task_maker.html", methods=["POST", "GET"])
def task_maker():
    db = sqlite3.connect("./runtime/db/sql.db")
    cursor = db.cursor()
    if request.method == "POST":
        name = request.form["name"]
        due = request.form["dueDate"]
        course = request.form["course"]
        type = request.form["type"]
        format = request.form["format"]
        marks = request.form["marks"]
        weighting = request.form["weighting"]
        cursor.execute("INSERT INTO tasks(name, due_date, course, type, format, earned_marks, total_marks, percent, weighting) VALUES (?, ?, ?, ?, ?, 0, ?, 0, ?)", [name, due, course, type, format, marks, weighting] )
        db.commit()
        db.close()
        return redirect(url_for('task_viewer'))
    else:
        db.close()
        return render_template("/task_maker.html")

@app.route("/form.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        email = request.form["email"]
        text = request.form["text"]
        app.logger.info(f"<From(email={email}, text='{text}')>")
        return render_template("/form.html")
    else:
        return render_template("/form.html")

# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data)
    return "done"

if __name__ == "__main__":
    # app.logger.debug("Started")
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host="0.0.0.0", port=5000)
