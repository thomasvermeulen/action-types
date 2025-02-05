from app.models import db

class Statement(db.Model):
    __tablename__ = 'statements'
    
    id = db.Column(db.Integer, primary_key=True)
    statement_number = db.Column(db.Integer, unique=True, nullable=False)
    
    choices = db.relationship('StatementChoice', backref='statement', lazy=True)
    responses = db.relationship('Response', backref='statement', lazy=True)
    
    def __repr__(self):
        return f'<Stelling {self.statement_number}>'

class StatementChoice(db.Model):
    __tablename__ = 'statement_choices'
    
    id = db.Column(db.Integer, primary_key=True)
    statement_id = db.Column(db.Integer, db.ForeignKey('statements.id'), nullable=False)
    choice_number = db.Column(db.Integer, nullable=False)
    choice_text = db.Column(db.String(200), nullable=False)
    choice_result = db.Column(db.String(1), nullable=False)
    
    def __repr__(self):
        return f'<Keuze {self.choice_number} voor stelling {self.statement_id}>'