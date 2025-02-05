from app.models import db
from app.models.response import Response
from app.models.statement import StatementChoice

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(10), nullable=False)
    team = db.Column(db.String(50))
    action_type = db.Column(db.String(4))
    
    responses = db.relationship('Response', backref='student', lazy=True)
    
    def calculate_action_type(self):
        category_counts = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        responses = Response.query.filter_by(student_id=self.id).all()

        for response in responses:
            choice = StatementChoice.query.filter_by(
                statement_id=response.statement_id,
                choice_number=response.choice_number
            ).first()
            if choice:
                category_counts[choice.choice_result] += 1

        action_type = (
            'E' if category_counts['E'] > category_counts['I'] else 'I'
        ) + (
            'S' if category_counts['S'] > category_counts['N'] else 'N'
        ) + (
            'T' if category_counts['T'] > category_counts['F'] else 'F'
        ) + (
            'J' if category_counts['J'] > category_counts['P'] else 'P'
        )

        self.action_type = action_type
        db.session.commit()

    def __repr__(self):
        return f'<Student {self.student_number}: {self.name}>'