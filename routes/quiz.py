from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db
from models.quiz import QuizQuestion
from models.progress import LessonProgress

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/quiz/<int:lesson_id>", methods=["GET", "POST"])
@login_required
def take_quiz(lesson_id):
    questions = QuizQuestion.query.filter_by(lesson_id=lesson_id).all()
    score = 0
    total = len(questions)

    if request.method == "POST":
        for question in questions:
            user_answer = request.form.get(f"question_{question.id}")

            # Check answer based on type
            if question.question_type == "multiple_choice":
                if user_answer == question.correct_answer:
                    score += 1

            elif question.question_type == "true_false":
                if user_answer.lower() == question.correct_answer.lower():
                    score += 1

            elif question.question_type == "short_answer":
                if user_answer.strip().lower() == question.correct_answer.strip().lower():
                    score += 1

        # Determine pass/fail
        passing_score = total * 0.7  # 70% to pass
        if score >= passing_score:
            flash(f"Quiz Passed! Score: {score}/{total}", "success")                 
        else:
            flash(f"Quiz Failed! Score: {score}/{total}. Try again.", "danger")

    return render_template("quiz.html", lesson_id=lesson_id, questions=questions)
