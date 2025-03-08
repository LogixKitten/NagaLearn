from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models.progress import LessonProgress
from database import db

exercises_bp = Blueprint("exercises", __name__)

# Define coding exercises
EXERCISES = {
    1: [
        {
            "id": 1,
            "question": "Create a variable called 'name' and assign it your name as a string.",
            "solution": "'name' in locals() and isinstance(name, str)"
        },
        {
            "id": 2,
            "question": "Print 'Hello, world!' to the console.",
            "solution": "'Hello, world!' in output"
        },
        {
            "id": 3,
            "question": "Create two variables, 'a' and 'b', and set them to 5 and 10. Print their sum.",
            "solution": "a == 5 and b == 10 and str(a + b) in output"
        }
    ]
}


@exercises_bp.route("/exercises/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def lesson_exercises(lesson_id):
    exercises = EXERCISES.get(lesson_id, [])

    return render_template("exercises.html", lesson_id=lesson_id, exercises=exercises)

@exercises_bp.route("/mark-lesson-complete/<int:lesson_id>", methods=["POST"])
@login_required
def mark_lesson_complete(lesson_id):
    progress = LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if progress:
        progress.completed = True
    else:
        db.session.add(LessonProgress(user_id=current_user.id, lesson_id=lesson_id, completed=True))
    
    db.session.commit()
    return jsonify({"message": "Lesson marked as complete."}), 200

