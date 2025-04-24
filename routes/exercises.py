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
            "starter_code": "",
            "solution": "'name' in locals() and isinstance(name, str)"
        },
        {
            "id": 2,
            "question": "Print 'Hello, world!' to the console.",
            "starter_code": "",
            "solution": "'Hello, world!' in output"
        },
        {
            "id": 3,
            "question": "Create two variables, 'a' and 'b', and set them to 5 and 10. Print their sum.",
            "starter_code": "",
            "solution": "a == 5 and b == 10 and str(a + b) in output"
        }
    ],
    2: [
        {
            "id": 1,
            "question": "Write a program that checks if a number is positive, negative, or zero. Store the number in a variable called `num`. Print 'Positive', 'Negative', or 'Zero' based on the value of `num`.",
            "starter_code": "",
            "solution": "'num' in locals() and (('Positive' in output and num > 0) or ('Negative' in output and num < 0) or ('Zero' in output and num == 0))"
        },
        {
            "id": 2,
            "question": "Write a for loop that prints the numbers 1 through 5, each on a new line.",
            "starter_code": "",
            "solution": "all(str(n) in output for n in range(1, 6))"
        },
        {
            "id": 3,
            "question": "Write a function called `is_even` that returns `True` if a number is even, and `False` if it is odd.",
            "starter_code": "",
            "solution": "'is_even' in locals() and is_even(2) == True and is_even(3) == False"
        },
        {
            "id": 4,
            "question": "Write a lambda function called `square` that takes a number and returns its square. Print the result of calling `square(4)`.",
            "starter_code": "",
            "solution": "'square' in locals() and callable(square) and square(4) == 16 and '16' in output and getattr(square, '__name__', '') == '<lambda>'"
        }
    ],
    3: [
        {
            "id": 1,
            "question": "Write a loop that goes through the list 'number_list' and prints whether each number is even or odd. The variable 'number_list' is already defined for you.",
            "starter_code": "# The variable 'number_list' is already defined for you.",
            "solution": "all(f\"{x} is even\" in output if x % 2 == 0 else f\"{x} is odd\" in output for x in number_list)"
        },
        {
            "id": 2,
            "question": "Create two dictionaries called 'apple' and 'orange' with the keys 'taste' and 'texture'. Assign each an appropriate value.",
            "starter_code": "",
            "solution": "('taste' in apple and 'texture' in apple and 'taste' in orange and 'texture' in orange)"
        },
        {
            "id": 3,
            "question": "The variable 'numbers' is already defined for you as a list. Write code that prints the unique numbers in 'numbers' using a set.",
            "starter_code": "# The variable 'numbers' is already defined for you.",
            "solution": "set(map(int, output.replace('{', '').replace('}', '').replace(',', ' ').split())) == set(numbers)"
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

