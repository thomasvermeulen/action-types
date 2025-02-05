import json
import os
import time
from app import create_app, db
from app.models.student import Student
from app.models.statement import Statement, StatementChoice
from app.models.teacher import Teacher

def remove_db_file(db_path, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"Successfully removed database at {db_path}")
            return True
        except PermissionError:
            if attempt < max_attempts - 1:
                print(f"Database is locked. Waiting before retry {attempt + 1}/{max_attempts}...")
                time.sleep(1)
            else:
                print("Could not remove database file - it may be in use. Continuing anyway...")
                return False

def import_data():
    app = create_app()
    
    with app.app_context():
        print("Starting data import...")
        
        db_path = os.path.join(os.path.dirname(__file__), 'app.db')
        remove_db_file(db_path)
        
        print("Creating tables...")
        db.create_all()
        
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")
        
        if not tables:
            print("No tables were created! Exiting...")
            return
            
        try:
            print("Importing statements...")
            with open('data/actiontype_statements.json', 'r', encoding='utf-8') as f:
                statements_data = json.load(f)
                
            for statement_data in statements_data:
                statement = Statement(statement_number=statement_data['statement_number'])
                db.session.add(statement)
                db.session.flush()
                
                for choice in statement_data['statement_choices']:
                    choice_obj = StatementChoice(
                        statement=statement,
                        choice_number=choice['choice_number'],
                        choice_text=choice['choice_text'],
                        choice_result=choice['choice_result']
                    )
                    db.session.add(choice_obj)
                db.session.flush()
            
            db.session.commit()
            print("Statements imported successfully")
            
            print("Importing students...")
            with open('data/students.json', 'r', encoding='utf-8') as f:
                students_data = json.load(f)
                
            for student_data in students_data:
                student = Student(
                    student_number=student_data['student_number'],
                    name=student_data['student_name'],
                    student_class=student_data['student_class']
                )
                db.session.add(student)
            
            db.session.commit()
            print("Students imported successfully")
            
            print("Creating admin user...")
            admin = Teacher(
                username='admin',
                name='Administrator',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            db.session.commit()
            print("All data imported successfully!")
            
        except Exception as e:
            print(f"Error during import: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    import_data()