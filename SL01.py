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
    EXCELLENT = "Excellent"
    GOOD = "Good"
    SATISFACTORY = "Satisfactory"
    NEEDS_IMPROVEMENT = "Needs Improvement"
    FAIL = "Fail"

class ActivityType(Enum):
    QUIZ = "Quiz"
    ASSIGNMENT = "Assignment"
    MIDTERM = "Midterm"
    FINAL_EXAM = "Final Exam"
    PROJECT = "Project"
    LAB = "Lab"

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
            'activity_type': data.get('activity_type', ''),
            'activity_name': data.get('activity_name', ''),
            'grade': data.get('grade', 0),
            'grade_status': data.get('grade_status', ''),
            'max_grade': data.get('max_grade', 100),
            'instructor_name': data.get('instructor_name', ''),
            'remarks': data.get('remarks', ''),
            'timestamp': time.time(),
            'signature': data.get('signature', '')
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
                if tx.get('student_id') == student_id:
                    if course_id is None or tx.get('course_id') == course_id:
                        records.append(tx)
        return sorted(records, key=lambda x: x['timestamp'])

    def get_course_records(self, course_id):
        """Get all academic records for a specific course"""
        records = []
        for block in self.chain:
            for tx in block['transactions']:
                if tx.get('course_id') == course_id:
                    records.append(tx)
        return sorted(records, key=lambda x: x['timestamp'])

    def calculate_student_average(self, student_id, course_id=None):
        """Calculate the average grade for a student, optionally for a specific course"""
        records = self.get_student_records(student_id, course_id)
        if not records:
            return 0.0
        
        total_score = 0
        total_weight = 0
        
        for record in records:
            grade = record.get('grade', 0)
            max_grade = record.get('max_grade', 100)
            # Simple weighting by activity type
            weight = 1.0
            if record.get('activity_type') == ActivityType.MIDTERM.value:
                weight = 2.0
            elif record.get('activity_type') == ActivityType.FINAL_EXAM.value:
                weight = 3.0
            elif record.get('activity_type') == ActivityType.PROJECT.value:
                weight = 2.5
                
            normalized_grade = (grade / max_grade) * 100
            total_score += normalized_grade * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return round(total_score / total_weight, 2)

blockchain = Blockchain()
blockchain.add_authorized("0xTeacher1")

@app.route('/add_milestone', methods=['POST'])
def add_milestone():
    data = request.get_json()
    
    # Validate required fields
    required = ['student_id', 'course_id', 'activity_type', 'grade', 'instructor_name']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate instructor is authorized
    instructor = data.get('instructor_name', '')
    if not blockchain.is_authorized(instructor):
        return jsonify({'error': f"Unauthorized instructor address: {instructor}"}), 403
    
    # Validate activity type
    if data.get('activity_type') not in [t.value for t in ActivityType]:
        return jsonify({'error': 'Invalid activity type'}), 400
    
    # Calculate grade status if not provided
    if 'grade_status' not in data:
        grade = float(data['grade'])
        max_grade = float(data.get('max_grade', 100))
        percentage = (grade / max_grade) * 100
        
        if percentage >= 90:
            data['grade_status'] = GradeStatus.EXCELLENT.value
        elif percentage >= 80:
            data['grade_status'] = GradeStatus.GOOD.value
        elif percentage >= 70:
            data['grade_status'] = GradeStatus.SATISFACTORY.value
        elif percentage >= 60:
            data['grade_status'] = GradeStatus.NEEDS_IMPROVEMENT.value
        else:
            data['grade_status'] = GradeStatus.FAIL.value
    
    # Add transaction to blockchain
    index = blockchain.add_transaction(data)
    blockchain.create_block(blockchain.last_block['hash'])
    
    return jsonify({
        'message': f'Academic milestone added and mined into Block {index}',
        'block_index': index
    }), 201

@app.route('/mine', methods=['GET'])
def mine():
    previous_hash = blockchain.last_block['hash']
    block = blockchain.create_block(previous_hash)
    return jsonify(block), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/student_records/<student_id>', methods=['GET'])
def student_records(student_id):
    course_id = request.args.get('course_id')
    records = blockchain.get_student_records(student_id, course_id)
    return jsonify({'student_id': student_id, 'records': records}), 200

@app.route('/course_records/<course_id>', methods=['GET'])
def course_records(course_id):
    records = blockchain.get_course_records(course_id)
    return jsonify({'course_id': course_id, 'records': records}), 200

@app.route('/student_average/<student_id>', methods=['GET'])
def student_average(student_id):
    course_id = request.args.get('course_id')
    average = blockchain.calculate_student_average(student_id, course_id)
    
    response = {
        'student_id': student_id,
        'average': average
    }
    
    if course_id:
        response['course_id'] = course_id
    
    return jsonify(response), 200

@app.route('/all_milestones', methods=['GET'])
def all_milestones():
    milestones = []
    for block in blockchain.chain:
        for tx in block['transactions']:
            if 'activity_type' in tx:  # Only include academic milestones
                milestones.append(tx)
    return jsonify({'milestones': milestones}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    print(f"✅ Academic Milestones Blockchain started at port {args.port}")
    app.run(host='0.0.0.0', port=args.port)
