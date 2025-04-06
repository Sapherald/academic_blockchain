import json
import time
from web3 import Web3
from pathlib import Path
import os
from datetime import datetime

class StudentLearningRecords:
    def __init__(self, blockchain_provider="http://localhost:8545", contract_address=None):
        """
        Initialize the StudentLearningRecords system.
        
        Args:
            blockchain_provider (str): URL of the blockchain provider (default is local Ganache)
            contract_address (str): Address of the deployed ProgressTracker contract
        """
        self.w3 = Web3(Web3.HTTPProvider(blockchain_provider))
        
        # Check connection
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to the blockchain provider")
        
        # Load contract ABI
        abi_path = Path(__file__).parent / "contract_abi.json"
        if not abi_path.exists():
            raise FileNotFoundError(f"Contract ABI file not found at {abi_path}")
        
        with open(abi_path, 'r') as file:
            self.contract_abi = json.load(file)
        
        # Load contract
        self.contract_address = contract_address
        if contract_address:
            self.contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )
        else:
            self.contract = None
            
        print(f"Connected to blockchain at {blockchain_provider}")
        if self.contract:
            print(f"Contract loaded at address {contract_address}")
    
    def deploy_contract(self, account_address, private_key):
        """
        Deploy the ProgressTracker contract to the blockchain.
        
        Args:
            account_address (str): The address of the account deploying the contract
            private_key (str): Private key of the account for signing transactions
            
        Returns:
            str: The address of the deployed contract
        """
        account_address = self.w3.to_checksum_address(account_address)
        
        # Create contract
        ProgressTracker = self.w3.eth.contract(
            abi=self.contract_abi,
            bytecode=self._get_contract_bytecode()
        )
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(account_address)
        transaction = ProgressTracker.constructor().build_transaction({
            'from': account_address,
            'nonce': nonce,
            'gas': 4000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        print("Waiting for contract deployment...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get contract address
        contract_address = tx_receipt['contractAddress']
        print(f"Contract deployed at: {contract_address}")
        
        # Set as the current contract
        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=self.contract_abi
        )
        
        # Save the contract address for future reference
        with open(Path(__file__).parent / "contract_address.txt", 'w') as file:
            file.write(contract_address)
        
        return contract_address
    
    def _get_contract_bytecode(self):
        """Get the bytecode for the ProgressTracker contract"""
        bytecode_path = Path(__file__).parent / "contract_bytecode.txt"
        if not bytecode_path.exists():
            raise FileNotFoundError(f"Contract bytecode file not found at {bytecode_path}")
        
        with open(bytecode_path, 'r') as file:
            return file.read().strip()
    
    def add_educator(self, admin_address, admin_private_key, educator_address):
        """
        Add an educator who can add student records.
        
        Args:
            admin_address (str): Address of the admin account
            admin_private_key (str): Private key of the admin account
            educator_address (str): Address of the educator to add
        """
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        admin_address = self.w3.to_checksum_address(admin_address)
        educator_address = self.w3.to_checksum_address(educator_address)
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(admin_address)
        txn = self.contract.functions.addEducator(educator_address).build_transaction({
            'from': admin_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(txn, admin_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Added educator {educator_address}")
        
        return tx_receipt
    
    def add_record(self, educator_address, educator_private_key, student_address, 
                  course_id, grade, activity_type, description=""):
        """
        Add a learning record for a student.
        
        Args:
            educator_address (str): Address of the educator adding the record
            educator_private_key (str): Private key of the educator
            student_address (str): Address of the student
            course_id (str): ID of the course
            grade (int): Grade score (0-100)
            activity_type (str): Type of activity (Quiz, Assignment, Project, etc.)
            description (str): Additional description of the activity
            
        Returns:
            dict: Transaction receipt
        """
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        educator_address = self.w3.to_checksum_address(educator_address)
        student_address = self.w3.to_checksum_address(student_address)
        
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(educator_address)
        txn = self.contract.functions.addRecord(
            student_address, course_id, grade, activity_type, description
        ).build_transaction({
            'from': educator_address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_txn = self.w3.eth.account.sign_transaction(txn, educator_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Added record for student {student_address}: {activity_type} in {course_id} with grade {grade}")
        
        return tx_receipt
    
    def get_student_records(self, student_address):
        """
        Get all learning records for a student.
        
        Args:
            student_address (str): Address of the student
            
        Returns:
            list: List of student records with formatted data
        """
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        student_address = self.w3.to_checksum_address(student_address)
        
        # Call the contract function
        course_ids, timestamps, grades, activity_types, descriptions = self.contract.functions.getStudentRecords(
            student_address
        ).call()
        
        # Format the records
        records = []
        for i in range(len(course_ids)):
            record = {
                'courseID': course_ids[i],
                'timestamp': timestamps[i],
                'date': datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d %H:%M:%S'),
                'grade': grades[i],
                'activityType': activity_types[i],
                'description': descriptions[i]
            }
            records.append(record)
        
        return records
    
    def get_record_count(self, student_address):
        """
        Get the number of records for a student.
        
        Args:
            student_address (str): Address of the student
            
        Returns:
            int: Number of records
        """
        if not self.contract:
            raise ValueError("Contract not loaded")
        
        student_address = self.w3.to_checksum_address(student_address)
        return self.contract.functions.getStudentRecordCount(student_address).call()
    
    def load_contract_from_file(self):
        """Load the contract address from a file if available"""
        address_path = Path(__file__).parent / "contract_address.txt"
        if address_path.exists():
            with open(address_path, 'r') as file:
                self.contract_address = file.read().strip()
                self.contract = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                return True
        return False


# Simple CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Student Learning Records (SL01)")
    parser.add_argument("--provider", default="http://localhost:8545", help="Blockchain provider URL")
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--address", help="Ethereum address for transaction sender")
    parser.add_argument("--key", help="Private key for signing transactions")
    parser.add_argument("--add-educator", help="Add an educator address")
    parser.add_argument("--add-record", action="store_true", help="Add a student record")
    parser.add_argument("--student", help="Student address")
    parser.add_argument("--course", help="Course ID")
    parser.add_argument("--grade", type=int, help="Grade (0-100)")
    parser.add_argument("--activity", help="Activity type (Quiz, Assignment, etc.)")
    parser.add_argument("--description", help="Activity description")
    parser.add_argument("--get-records", help="Get records for a student address")
    
    args = parser.parse_args()
    
    try:
        sl = StudentLearningRecords(args.provider)
        
        # Try to load existing contract
        if not args.deploy and not sl.contract:
            sl.load_contract_from_file()
        
        if args.deploy and args.address and args.key:
            sl.deploy_contract(args.address, args.key)
        
        elif args.add_educator and args.address and args.key:
            sl.add_educator(args.address, args.key, args.add_educator)
        
        elif args.add_record and args.address and args.key and args.student and args.course and args.grade is not None and args.activity:
            sl.add_record(
                args.address, args.key, args.student, 
                args.course, args.grade, args.activity, 
                args.description or ""
            )
        
        elif args.get_records:
            records = sl.get_student_records(args.get_records)
            print(f"\nStudent Records for {args.get_records}:")
            print("-" * 80)
            for i, record in enumerate(records, 1):
                print(f"Record #{i}:")
                print(f"  Course: {record['courseID']}")
                print(f"  Date: {record['date']}")
                print(f"  Activity: {record['activityType']}")
                print(f"  Grade: {record['grade']}")
                if record['description']:
                    print(f"  Description: {record['description']}")
                print()
        
        else:
            print("Use --help to see available commands")
    
    except Exception as e:
        print(f"Error: {e}")
