from app import app, db
from models.lesson import Lesson
import os

def reset_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add structured lessons
        lesson_files = [
            ("Lesson 1: Introduction to Python", "01_intro.txt"),
            ("Lesson 2: Variables & Data Types", "02_variables.txt"),
            ("Lesson 3: User Input & Output", "03_input_output.txt"),
            ("Lesson 4: Basic Math Operations", "04_math_operations.txt"),
            ("Lesson 5: Conditional Statements", "05_conditionals.txt"),
            ("Lesson 6: Loops (While & For)", "06_loops.txt"),
            ("Lesson 7: Functions & Parameters", "07_functions.txt"),
            ("Lesson 8: Lists", "08_lists.txt"),
            ("Lesson 9: Dictionaries", "09_dictionaries.txt"),
            ("Lesson 10: Sets & Tuples", "10_sets_tuples.txt"),
            ("Lesson 11: Importing Modules", "11_importing_modules.txt"),
            ("Lesson 12: Using the Math Library", "12_math_library.txt"),
            ("Lesson 13: Working with Random Numbers", "13_random_numbers.txt"),
            ("Lesson 14: Building a Simple Calculator", "14_calculator_project.txt"),
            ("Lesson 15: Creating a To-Do List", "15_todo_project.txt"),
            ("Lesson 16: Common Errors & Debugging", "16_debugging.txt"),
            ("Lesson 17: Writing Test Cases", "17_testing.txt"),
            ("Lesson 18: Handling Exceptions", "18_exceptions.txt"),
        ]

        for title, filename in lesson_files:
            db.session.add(Lesson(title=title, filename=filename))

        db.session.commit()
        print("✅ Database has been reset!")

if __name__ == "__main__":
    reset_database()
