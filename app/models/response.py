from app.models import db
from datetime import datetime

class Response(db.Model):
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    statement_id = db.Column(db.Integer, db.ForeignKey('statements.id'), nullable=False)
    choice_number = db.Column(db.Integer, nullable=False)
    response_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Antwoord van student {self.student_id} op stelling {self.statement_id}>'