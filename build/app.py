"""
Main application entry point for Student Learning Records (SL01) module.
"""

import os
import argparse
from pathlib import Path

def setup_project():
    """Set up project structure and files"""
    # Create directory structure
    dirs = ['templates', 'static']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("Project structure created successfully")
    
    # Check if required files exist, if not, create them
    from compile_contract import compile_contract
    compile_contract()
    
    print("\nProject setup complete! You can now run the web application.")

def start_web_app():
    """Start the web application"""
    print("Starting web application...")
    
    # Import here to avoid circular imports
    from web_interface import app
    app.run(debug=True, port=5000)

def start_cli():
    """Start the command-line interface"""
    print("Starting command-line interface...")
    
    from student_learning_records import StudentLearningRecords
    sl = StudentLearningRecords()
    
    # Try to load existing contract
    if sl.load_contract_from_file():
        print(f"Loaded contract from file: {sl.contract_address}")
    else:
        print("No existing contract found. Use '--deploy' option to deploy a new contract.")
    
    print("\nUse the following commands to interact with the system:")
    print("- python student_learning_records.py --help")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SL01 - Student Learning Records")
    parser.add_argument('--setup', action='store_true', help='Set up project structure and compile contract')
    parser.add_argument('--web', action='store_true', help='Start web application')
    parser.add_argument('--cli', action='store_true', help='Start command-line interface')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_project()
    elif args.web:
        start_web_app()
    elif args.cli:
        start_cli()
    else:
        # Default action if no arguments provided
        parser.print_help()
