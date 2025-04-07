from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import hashlib
import time
import argparse
from enum import Enum

app = Flask(__name__)
CORS(app)
