import os
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-key-change-this-before-deploying")


@app.route("/")
def home():
    return render_template("home.html")


# ---------- word counter ----------

@app.route("/word-counter", methods=["GET", "POST"])
def word_counter():
    result = None
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("myfile")
        if not uploaded_file or uploaded_file.filename == "":
            error = "Please choose a text file to upload."
        else:
            try:
                content = uploaded_file.read().decode("utf-8", errors="ignore")
                words = content.split()
                lines = content.splitlines()
                result = {
                    "filename": uploaded_file.filename,
                    "words": len(words),
                    "lines": len(lines),
                    "chars": len(content),
                }
            except Exception as exc:
                error = f"Could not read that file: {exc}"

    return render_template("word_counter.html", result=result, error=error)


# ---------- calculator ----------

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None

    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            if operation == "add":
                result = add(num1, num2)
            elif operation == "subtract":
                result = subtract(num1, num2)
            elif operation == "multiply":
                result = multiply(num1, num2)
            elif operation == "divide":
                result = divide(num1, num2)
        except (ValueError, KeyError):
            result = "Please enter valid numbers."

    return render_template("calculator.html", result=result)


# ---------- number guessing game ----------
# the secret number and guess count live in the session (a signed cookie),
# since there's no server-side storage to keep them in between requests

@app.route("/guessing-game", methods=["GET", "POST"])
def guessing_game():
    if "secret_number" not in session or request.args.get("new") == "1":
        session["secret_number"] = random.randint(1, 100)
        session["attempts"] = 0

    feedback = None
    won = False

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
        except (ValueError, KeyError):
            feedback = "Enter a whole number between 1 and 100."
        else:
            if guess < 1 or guess > 100:
                feedback = "Enter a number between 1 and 100."
            else:
                session["attempts"] += 1
                secret = session["secret_number"]
                if guess < secret:
                    feedback = "Too low, try again."
                elif guess > secret:
                    feedback = "Too high, try again."
                else:
                    feedback = f"Correct! It was {secret}."
                    won = True

    return render_template(
        "guessing_game.html",
        feedback=feedback,
        won=won,
        attempts=session.get("attempts", 0),
    )


# ---------- to-do list ----------
# tasks live in the session too, so no database is needed

@app.route("/todo-list", methods=["GET", "POST"])
def todo_list():
    if "tasks" not in session:
        session["tasks"] = []

    if request.method == "POST":
        action = request.form.get("action")
        tasks = session["tasks"]

        if action == "add":
            description = request.form.get("description", "").strip()
            if description:
                tasks.append({"description": description, "completed": False})

        elif action == "toggle":
            index = int(request.form.get("index", -1))
            if 0 <= index < len(tasks):
                tasks[index]["completed"] = not tasks[index]["completed"]

        elif action == "delete":
            index = int(request.form.get("index", -1))
            if 0 <= index < len(tasks):
                tasks.pop(index)

        session["tasks"] = tasks
        session.modified = True
        return redirect(url_for("todo_list"))

    return render_template("todo_list.html", tasks=session.get("tasks", []))


if __name__ == "__main__":
    app.run(debug=True)
