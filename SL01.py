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
