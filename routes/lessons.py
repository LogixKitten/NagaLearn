from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db
from models.lesson import Lesson
from models.progress import LessonProgress
import markdown

lessons_bp = Blueprint("lessons", __name__)

@lessons_bp.route("/lessons")
@login_required
def view_lessons():
    lessons = Lesson.query.all()
    progress = LessonProgress.query.filter_by(user_id=current_user.id).all()
    
    progress_dict = {p.lesson_id: p for p in progress}

    return render_template("lessons.html", lessons=lessons, progress_dict=progress_dict)

@lessons_bp.route("/lesson/<int:lesson_id>")
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    # Ensure previous lesson is completed before accessing this one
    if lesson_id > 1:
        prev_progress = LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id - 1).first()
        if not prev_progress or not prev_progress.completed:
            flash("Complete the previous lesson first!", "error")
            return redirect(url_for("lessons.view_lessons"))

    # Load lesson content
    lesson_content = markdown.markdown(lesson.load_content(), extensions=["extra"])

    # Get progress data for the user
    progress = LessonProgress.query.filter_by(user_id=current_user.id).all()
    progress_dict = {p.lesson_id: p for p in progress}

    return render_template("lesson.html", lesson=lesson, content=lesson_content, progress_dict=progress_dict)

@lessons_bp.route("/complete_lesson/<int:lesson_id>", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Check if the lesson is already marked as complete
    progress = LessonProgress.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()

    if not progress:
        new_progress = LessonProgress(user_id=current_user.id, lesson_id=lesson_id, completed=True)
        db.session.add(new_progress)
        db.session.commit()
        flash(f"'{lesson.title}' marked as complete!", "success")

    return redirect(url_for("lessons.view_lessons"))
