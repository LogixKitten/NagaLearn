from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from database import db
from models.user import User
from routes.auth import auth_bp
from routes.lessons import lessons_bp
from routes.quiz import quiz_bp
from routes.exercises import exercises_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretjenny8675309"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route (Landing Page)
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("lessons.view_lessons"))  # Redirect logged-in users to lessons
    return render_template("index.html")  # Show landing page for guests


app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(lessons_bp, url_prefix="/")
app.register_blueprint(quiz_bp, url_prefix="/")
app.register_blueprint(exercises_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)
