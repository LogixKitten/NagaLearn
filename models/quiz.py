from database import db

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # "multiple_choice", "true_false", "short_answer"
    
    # Multiple Choice Fields
    option_a = db.Column(db.String(255), nullable=True)
    option_b = db.Column(db.String(255), nullable=True)
    option_c = db.Column(db.String(255), nullable=True)
    option_d = db.Column(db.String(255), nullable=True)
    
    # Correct Answer (Can store A/B/C/D, True/False, or text for short answers)
    correct_answer = db.Column(db.String(255), nullable=False)

    lesson = db.relationship('Lesson', backref=db.backref('quiz_questions', lazy=True))
