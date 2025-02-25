import os
from database import db

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Store filename instead of content

    def load_content(self):
        """Load lesson content from file"""
        file_path = os.path.join("lessons", self.filename)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return "Lesson content not found."
