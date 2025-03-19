from flask import Flask, request, jsonify
import os
from src.utils.blockchain import add_student_record, get_student_records
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/records', methods=['POST'])
def create_record():
    """Create a new student record on the blockchain"""
    data = request.json
    
    # Validate input data
    required_fields = ['student_address', 'course_id', 'grade', 'activity_type']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate grade range
    if not 0 <= int(data['grade']) <= 100:
        return jsonify({"error": "Grade must be between 0 and 100"}), 400
    
    # Add record to blockchain
    result = add_student_record(
        data['student_address'],
        data['course_id'],
        int(data['grade']),
        data['activity_type']
    )
    
    if result.get('success'):
        return jsonify({
            "message": "Record added successfully",
            "transaction": result
        }), 201
    else:
        return jsonify({"error": result.get('error', 'Unknown error')}), 500

@app.route('/api/records/<student_address>', methods=['GET'])
def get_records(student_address):
    """Get all records for a student from the blockchain"""
    records = get_student_records(student_address)
    
    return jsonify({
        "student_address": student_address,
        "record_count": len(records),
        "records": records
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)