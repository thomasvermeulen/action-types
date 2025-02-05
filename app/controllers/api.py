from flask import Blueprint, jsonify, request
from app.models import db
from app.models.student import Student
from app.models.statement import Statement, StatementChoice
from app.models.response import Response

bp = Blueprint('api', __name__)

@bp.route('/student/<int:student_number>/statement', methods=['GET'])
def get_statement(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return jsonify({'error': 'Student niet gevonden'}), 404
    
    answered_statements = Response.query.filter_by(student_id=student.id).all()
    answered_numbers = [r.statement_id for r in answered_statements]
    
    next_statement = Statement.query.filter(~Statement.id.in_(answered_numbers if answered_numbers else [0])).order_by(Statement.statement_number).first()
    
    if not next_statement:
        return jsonify({'message': 'Alle stellingen voltooid'}), 200
        
    choices = next_statement.choices
    return jsonify({
        'statement_number': next_statement.statement_number,
        'statement_choices': [
            {
                'choice_number': choice.choice_number,
                'choice_text': choice.choice_text
            } for choice in choices
        ]
    })

@bp.route('/student/<int:student_number>/statement/<int:statement_number>', methods=['POST'])
def save_statement(student_number, statement_number):
    try:
        student = Student.query.filter_by(student_number=student_number).first()
        if not student:
            return jsonify({'error': 'Student niet gevonden'}), 404
            
        statement = Statement.query.filter_by(statement_number=statement_number).first()
        if not statement:
            return jsonify({'error': 'Stelling niet gevonden'}), 404
            
        data = request.get_json()
        if not data or 'statement_choice' not in data:
            return jsonify({'error': 'Keuze ontbreekt'}), 400
            
        choice_number = data['statement_choice']
        
        choice = StatementChoice.query.filter_by(
            statement_id=statement.id, 
            choice_number=choice_number
        ).first()
        if not choice:
            return jsonify({'error': f'Ongeldig keuzenummer {choice_number}'}), 400
        
        existing_response = Response.query.filter_by(
            student_id=student.id,
            statement_id=statement.id
        ).first()
        
        if existing_response:
            return jsonify({'error': 'Antwoord bestaat al voor deze stelling'}), 400
            
        response = Response(
            student_id=student.id,
            statement_id=statement.id,
            choice_number=choice_number
        )
        
        db.session.add(response)
        db.session.commit()

        total_statements = Statement.query.count()
        answered_statements = Response.query.filter_by(student_id=student.id).count()

        if answered_statements == total_statements:
            student.calculate_action_type()
            return jsonify({'result': 'ok', 'action_type': student.action_type})

        return jsonify({'result': 'ok'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Fout bij opslaan antwoord: {str(e)}")
        return jsonify({'error': 'Opslaan mislukt'}), 500

@bp.route('/statements/<int:student_number>', methods=['GET'])
def get_student_statements(student_number):
    student = Student.query.filter_by(student_number=student_number).first()
    if not student:
        return jsonify({'error': 'Student niet gevonden'}), 404
    
    responses = Response.query.filter_by(student_id=student.id).all()
    
    statements_data = []
    for response in responses:
        statement = Statement.query.get(response.statement_id)
        if statement:
            choices = StatementChoice.query.filter_by(statement_id=statement.id).order_by(StatementChoice.choice_number).all()
            selected_choice = next((c for c in choices if c.choice_number == response.choice_number), None)
            
            statements_data.append({
                'statement_number': statement.statement_number,
                'choices': [f"{c.choice_number}. {c.choice_text}" for c in choices],
                'selected': f"Gekozen: {selected_choice.choice_text if selected_choice else 'Onbekend'}"
            })
    
    return jsonify({
        'statements': [
            f"Stelling {s['statement_number']}\n" +
            "\n".join(s['choices']) +
            f"\n{s['selected']}"
            for s in statements_data
        ]
    })