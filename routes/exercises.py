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
            "solution": "is_correct = 'name' in locals() and isinstance(name, str)\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 2,
            "question": "Print 'Hello, world!' to the console.",
            "starter_code": "",
            "solution": "is_correct = 'Hello, world!' in output\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 3,
            "question": "Create two variables, 'a' and 'b', and set them to 5 and 10. Print their sum.",
            "starter_code": "",
            "solution": "is_correct = a == 5 and b == 10 and str(a + b) in output\nglobals()['is_correct'] = is_correct"
        }
    ],
    2: [
        {
            "id": 1,
            "question": "Write a program that checks if a number is positive, negative, or zero. Store the number in a variable called `num`. Print 'Positive', 'Negative', or 'Zero' based on the value of `num`.",
            "starter_code": "",
            "solution": "is_correct = 'num' in locals() and (('Positive' in output and num > 0) or ('Negative' in output and num < 0) or ('Zero' in output and num == 0))\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 2,
            "question": "Write a for loop that prints the numbers 1 through 5, each on a new line.",
            "starter_code": "",
            "solution": "is_correct = all(str(n) in output for n in range(1, 6))\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 3,
            "question": "Write a function called `is_even` that returns `True` if a number is even, and `False` if it is odd.",
            "starter_code": "",
            "solution": "is_correct = 'is_even' in locals() and is_even(2) == True and is_even(3) == False\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 4,
            "question": "Write a lambda function called `square` that takes a number and returns its square. Print the result of calling `square(4)`.",
            "starter_code": "",
            "solution": "is_correct = 'square' in locals() and callable(square) and square(4) == 16 and '16' in output and getattr(square, '__name__', '') == '<lambda>'\nglobals()['is_correct'] = is_correct"
        }
    ],
    3: [
        {
            "id": 1,
            "question": "Write a loop that goes through the list 'number_list' and prints whether each number is even or odd. The variable 'number_list' is already defined for you.",
            "starter_code": "# The variable 'number_list' is already defined for you.",
            "solution": "is_correct = all(f\"{x} is even\" in output if x % 2 == 0 else f\"{x} is odd\" in output for x in number_list)\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 2,
            "question": "Create two dictionaries called 'apple' and 'orange' with the keys 'taste' and 'texture'. Assign each an appropriate value.",
            "starter_code": "",
            "solution": "is_correct = ('taste' in apple and 'texture' in apple and 'taste' in orange and 'texture' in orange)\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 3,
            "question": "The variable 'numbers' is already defined for you as a list. Write code that prints the unique numbers in 'numbers' using a set.",
            "starter_code": "# The variable 'numbers' is already defined for you.",
            "solution": "is_correct = set(map(int, output.replace('{', '').replace('}', '').replace(',', ' ').split())) == set(numbers)\nglobals()['is_correct'] = is_correct"
        }
    ],
    4: [
        {
            "id": 1,
            "question": "Use the math library to calculate and print the value of π squared.",
            "starter_code": "import math\n",
            "solution": "imported_math = 'import math' in user_code\ncheck = abs(float(output.strip()) - 9.869604401089358) < 0.01\nis_correct = imported_math and check\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 2,
            "question": "Use the random library to simulate rolling two six-sided dice and print their total.",
            "starter_code": "import random\n",
            "solution": "imported_random = 'import random' in user_code\nval = output.strip()\ncheck = val.isdigit() and 2 <= int(val) <= 12\nis_correct = imported_random and check\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 3,
            "question": "Use the datetime library to calculate how many days are left until the end of this year.",
            "starter_code": "import datetime\n",
            "solution": "imported_datetime = 'import datetime' in user_code\nval = output.strip()\nfrom datetime import date\nend_of_year = date(date.today().year, 12, 31)\ndays_left = (end_of_year - date.today()).days\ncheck = val.isdigit() and abs(int(val) - days_left) <= 1\nis_correct = imported_datetime and check\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 4,
            "question": "Use math.sqrt to find and print the square root of 144.",
            "starter_code": "import math\n",
            "solution": "imported_math = 'import math' in user_code\ncheck = abs(float(output.strip()) - 12.0) < 0.01\nis_correct = imported_math and check\nglobals()['is_correct'] = is_correct"
        },
        {
            "id": 5,
            "question": "Use random.choice to randomly select an item from the list my_list = ['apple', 'banana', 'cherry'] and print it.",
            "starter_code": "import random\nmy_list = ['apple', 'banana', 'cherry']\n",
            "solution": "imported_random = 'import random' in user_code\nval = output.strip()\ncheck = val in ['apple', 'banana', 'cherry']\nis_correct = imported_random and check\nglobals()['is_correct'] = is_correct"
        }
    ],
    5: [
        {
            "id": 1,
            "question": "Write a program that asks the user for two numbers and prints their division. Use try/except to handle division by zero and invalid input.\n(note: input() will automatically be tested with division by zero)",
            "starter_code": "# Write your code here",
            "solution": "has_try = 'try' in user_code\n"
                        "has_except = 'except' in user_code\n"
                        "output_has_number = any(char.isdigit() for char in output)\n"
                        "error_handled = ('zero' in output.lower() or 'invalid' in output.lower() or 'error' in output.lower()) and 'Traceback' not in output\n"
                        "is_correct = has_try and has_except and (output_has_number or error_handled)\n"
                        "globals()['is_correct'] = is_correct"
        },
        {
            "id": 2,
            "question": "Fix the bug in this code so it runs without errors:\n\nnumbers = [1, 2, 3]\nprint(numbers[3])",
            "starter_code": "numbers = [1, 2, 3]\nprint(numbers[3])",
            "solution": "no_error = 'Error' not in output and 'Traceback' not in output\nany_number = any(char.isdigit() for char in output)\nhas_try = 'try' in user_code\nhas_except = 'except' in user_code\nis_correct = no_error and (any_number or (has_try and has_except))\nglobals()['is_correct'] = is_correct"
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

