# Mini Programs

Four small programs behind one home page:

- Word Counter — upload a .txt file, get word/line/character counts
- Calculator — add, subtract, multiply, divide two numbers
- Number Guessing Game — guess a number between 1 and 100
- To-Do List — add, complete, and remove tasks

Built with Flask. Game state and to-do tasks are stored in the session
(a signed cookie) instead of a database, since there's nothing here that
needs real persistence, and it keeps the app fully stateless for
serverless hosting.

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000/

## Deploy on Vercel

1. Push this folder to a GitHub repo.
2. Go to vercel.com -> New Project -> import the repo.
3. Vercel detects the Flask app automatically from requirements.txt and app.py.
4. Add one environment variable: SECRET_KEY (any random string).
5. Click Deploy.
