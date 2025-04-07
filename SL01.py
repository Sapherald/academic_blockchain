from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import hashlib
import time
import argparse
from enum import Enum

app = Flask(__name__)
CORS(app)

class GradeStatus(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"

class ActivityType(Enum):
    QUIZ = "Quiz"
    ASSIGNMENT = "Assignment"
    MIDTERM = "Midterm"
    FINAL_EXAM = "Final Exam"
    PROJECT = "Project"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.authorized_addresses = set()
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions.copy(),
            'previous_hash': previous_hash,
            'hash': ''
        }
        block['hash'] = self.hash_block(block)
        self.chain.append(block)
        self.transactions = []
        return block

def add_transaction(self, data):
        transaction = {
            'student_id': data['student_id'],
            'student_name': data.get('student_name', ''),
            'course_id': data.get('course_id', ''),
            'instructor_name': data.get('instructor_name', ''),
            'activity_type': data.get('activity_type', ''),
            'score': data.get('score', 0),
            'max_score': data.get('max_score', 100),
            'percentage': data.get('percentage', 0),
            'grade': data.get('grade', ''),
            'comments': data.get('comments', ''),
            'timestamp': time.time(),
            'signature': data.get('signature', ''),
            'record_type': data['record_type']
        }
        self.transactions.append(transaction)
        return self.last_block['index'] + 1

def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
 @property
    def last_block(self):
        return self.chain[-1]

    def add_authorized(self, address):
        self.authorized_addresses.add(address)

    def is_authorized(self, address):
        return address in self.authorized_addresses

    def get_student_records(self, student_id, course_id=None):
        """Get all academic records for a specific student, optionally filtered by course"""
       records = []
        for block in self.chain:
            for tx in block['transactions']:
                if tx.get('record_type') == 'AcademicRecord' and tx['student_id'] == student_id:
                    if course_id is None or tx.get('course_id') == course_id:
                        records.append(tx)
        return sorted(records, key=lambda x: x['timestamp'])

    def calculate_course_average(self, student_id, course_id):
        records = self.get_student_records(student_id, course_id)
        if not records:
            return 0.0
        
        total_score = 0
        total_weight = 1
        
      # Assign weights based on activity type
            if record.get('activity_type') == ActivityType.QUIZ.value:
                weight = 0.1
            elif record.get('activity_type') == ActivityType.ASSIGNMENT.value:
                weight = 0.2
            elif record.get('activity_type') == ActivityType.MIDTERM.value:
                weight = 0.3
            elif record.get('activity_type') == ActivityType.FINAL.value:
                weight = 0.4
            elif record.get('activity_type') == ActivityType.PROJECT.value:
                weight = 0.3
            
            percentage = record.get('percentage', 0)
            total_score += percentage * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return round(total_score / total_weight, 1)

def get_letter_grade(self, percentage):
        if percentage >= 90:
            return GradeLevel.A.value
        elif percentage >= 80:
            return GradeLevel.B.value
        elif percentage >= 70:
            return GradeLevel.C.value
        elif percentage >= 60:
            return GradeLevel.D.value
        else:
            return GradeLevel.F.value

blockchain = Blockchain()
blockchain.add_authorized("0xTeacher1")

@app.route('/add_milestone', methods=['POST'])
def add_milestone():
    data = request.get_json()
    required = ['student_id', 'record_type', 'course_id', 'activity_type', 'score', 'max_score']

    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400

    if data['record_type'] != 'AcademicRecord':
        return jsonify({'error': 'Invalid record_type for SL01'}), 400

    instructor = data.get('instructor_name', '')
    if not blockchain.is_authorized(instructor):
        return jsonify({'error': f"Unauthorized instructor address: {instructor}"}), 403

    if data.get('activity_type') not in [s.value for s in ActivityType]:
        return jsonify({'error': 'Invalid activity type'}), 400
    
    # Calculate percentage
    score = float(data.get('score', 0))
    max_score = float(data.get('max_score', 100))
    
    if max_score <= 0:
        return jsonify({'error': 'Max score must be greater than zero'}), 400
    
    percentage = (score / max_score) * 100
    data['percentage'] = round(percentage, 1)
    
    # Add letter grade
    data['grade'] = blockchain.get_letter_grade(percentage)

    index = blockchain.add_transaction(data)
    blockchain.create_block(blockchain.last_block['hash'])
    return jsonify({
        'message': f'Academic milestone added and mined into Block {index}',
        'percentage': data['percentage'],
        'grade': data['grade']
    }), 201

@app.route('/mine', methods=['GET'])
def mine():
    previous_hash = blockchain.last_block['hash']
    block = blockchain.create_block(previous_hash)
    return jsonify(block), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/student_records', methods=['GET'])
def student_records():
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')
    
    if not student_id:
        return jsonify({'error': 'Missing student_id parameter'}), 400
    
    records = blockchain.get_student_records(student_id, course_id)
    
    return jsonify({'student_id': student_id, 'course_id': course_id, 'records': records}), 200

@app.route('/course_average', methods=['GET'])
def course_average():
    student_id = request.args.get('student_id')
    course_id = request.args.get('course_id')
    
    if not student_id or not course_id:
        return jsonify({'error': 'Missing student_id or course_id'}), 400
    
    average = blockchain.calculate_course_average(student_id, course_id)
    letter_grade = blockchain.get_letter_grade(average)
    
    return jsonify({
        'student_id': student_id,
        'course_id': course_id,
        'average': average,
        'letter_grade': letter_grade
    }), 200

@app.route('/all_milestones', methods=['GET'])
def all_milestones():
    milestones = []
    for block in blockchain.chain:
        for tx in block['transactions']:
            if tx.get('record_type') == 'AcademicRecord':
                milestones.append({
                    'student_id': tx['student_id'],
                    'student_name': tx.get('student_name', ''),
                    'course_id': tx.get('course_id', ''),
                    'activity_type': tx.get('activity_type', ''),
                    'score': tx.get('score', 0),
                    'max_score': tx.get('max_score', 100),
                    'percentage': tx.get('percentage', 0),
                    'grade': tx.get('grade', ''),
                    'instructor_name': tx.get('instructor_name', ''),
                    'timestamp': tx['timestamp']
                })
    return jsonify({'milestones': milestones}), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_form')
def add_form():
    return render_template('add_milestone.html')

@app.route('/view_records')
def view_records():
    return render_template('view_records.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    print(f"✅ Blockchain SL01 started at port {args.port}")
    app.run(host='0.0.0.0', port=args.port)
