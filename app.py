from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_skills():
    conn = sqlite3.connect("skills.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM skills ORDER BY id DESC")
    skills = cur.fetchall()

    conn.close()
    return skills


def get_skill(skill_id):
    conn = sqlite3.connect("skills.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM skills WHERE id = ?",
        (skill_id,)
    )

    skill = cur.fetchone()

    conn.close()
    return skill


def add_skill(name, status):
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO skills (name, status) VALUES (?, ?)",
        (name, status)
    )

    conn.commit()
    conn.close()


def update_skill(skill_id, name, status):
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    cur.execute(
        "UPDATE skills SET name = ?, status = ? WHERE id = ?",
        (name, status, skill_id)
    )

    conn.commit()
    conn.close()


def delete_skill(skill_id):
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM skills WHERE id = ?",
        (skill_id,)
    )

    conn.commit()
    conn.close()

def delete_selected_skills(selected_ids):
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    placeholders = ",".join(["?"] * len(selected_ids))

    cur.execute(
        f"DELETE FROM skills WHERE id IN ({placeholders})",
        selected_ids
    )

    conn.commit()
    conn.close()

@app.route("/delete_selected", methods=["POST"])
def delete_selected():
    selected_ids = request.form.getlist("selected_ids")

    if not selected_ids:
        return redirect("/")

    delete_selected_skills(selected_ids)

    return redirect("/")


@app.route("/")
def index():
    skills = get_skills()
    return render_template("index.html", skills=skills)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    status = request.form["status"]

    add_skill(name, status)

    return redirect("/")


@app.route("/edit/<int:skill_id>")
def edit(skill_id):
    skill = get_skill(skill_id)
    return render_template("edit.html", skill=skill)


@app.route("/update/<int:skill_id>", methods=["POST"])
def update(skill_id):
    name = request.form["name"]
    status = request.form["status"]

    update_skill(skill_id, name, status)

    return redirect("/")


@app.route("/delete/<int:skill_id>", methods=["POST"])
def delete(skill_id):
    delete_skill(skill_id)
    return redirect("/")

def delete_all_skills():
    conn = sqlite3.connect("skills.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM skills")

    conn.commit()
    conn.close()

@app.route("/delete_all", methods=["POST"])
def delete_all():
    delete_all_skills()
    return redirect("/")

init_db()

if __name__ == "__main__":
    app.run(debug=True)