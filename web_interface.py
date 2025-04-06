"""
Web interface for Student Learning Records (SL01)
A simple Flask application to interact with the blockchain-based learning records system.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from pathlib import Path
import json
from student_learning_records import StudentLearningRecords

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize blockchain connection
try:
    sl = StudentLearningRecords(blockchain_provider="http://localhost:8545")
    sl.load_contract_from_file()
except Exception as e:
    print(f"Blockchain connection error: {e}")
    sl = None

# Create templates directory if it doesn't exist
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(exist_ok=True)

# Create base template
base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Student Learning Records{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .container { max-width: 900px; margin-top: 30px; }
        .flash-messages { margin: 20px 0; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">SL01 - Student Learning Records</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/deploy">Deploy Contract</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/add-educator">Add Educator</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/add-record">Add Record</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/view-records">View Records</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Create index template
index_template = """{% extends "base.html" %}

{% block title %}SL01 - Student Learning Records{% endblock %}

{% block content %}
    <div class="card">
        <div class="card-header">
            <h1>Student Learning Records (SL01)</h1>
        </div>
        <div class="card-body">
            <h5 class="card-title">Blockchain-based Academic Records Management</h5>
            <p class="card-text">
                This system stores key milestones like quiz scores and assignment grades as blockchain transactions.
                Use the navigation menu to perform various operations.
            </p>
            
            <div class="alert alert-info">
                <h4>Current Status:</h4>
                <p>
                    {% if contract_status %}
                        <strong>Contract Deployed at:</strong> {{ contract_address }}<br>
                        <strong>Connected to:</strong> {{ blockchain_provider }}
                    {% else %}
                        <strong>Contract not deployed.</strong> Please deploy the contract first.
                    {% endif %}
                </p>
            </div>
            
            <h3>Getting Started</h3>
            <ol>
                <li>Deploy the contract (if not already deployed)</li>
                <li>Add educators who can add records</li>
                <li>Add student learning records</li>
                <li>View student records</li>
            </ol>
        </div>
    </div>
{% endblock %}
"""

# Create deploy template
deploy_template = """{% extends "base.html" %}

{% block title %}Deploy Contract{% endblock %}

{% block content %}
    <div class="card">
        <div class="card-header">
            <h1>Deploy ProgressTracker Contract</h1>
        </div>
        <div class="card-body">
            {% if contract_status %}
                <div class="alert alert-info">
                    <strong>Contract already deployed at:</strong> {{ contract_address }}
                </div>
                <p>If you deploy a new contract, the old one will no longer be used by this application.</p>
            {% endif %}
            
            <form method="post">
                <div class="mb-3">
                    <label for="address" class="form-label">Admin Address</label>
                    <input type="text" class="form-control" id="address" name="address" required 
                           placeholder="0x...">
                    <div class="form-text">The Ethereum address that will be the admin of the contract</div>
                </div>
                <div class="mb-3">
                    <label for="private_key" class="form-label">Private Key</label>
                    <input type="password" class="form-control" id="private_key" name="private_key" required>
                    <div class="form-text">Private key for signing the deployment transaction</div>
                </div>
                <button type="submit" class="btn btn-primary">Deploy Contract</button>
            </form>
        </div>
    </div>
{% endblock %}
"""
