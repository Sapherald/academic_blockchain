from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup blockchain connection
def get_blockchain_connection():
    """
    Connect to the blockchain network using environment variables
    """
    # For development, use Ganache (local blockchain)
    # For production, use a proper Ethereum node or Infura
    blockchain_url = os.getenv('BLOCKCHAIN_URL', 'http://127.0.0.1:7545')  # Default to Ganache
    
    try:
        w3 = Web3(Web3.HTTPProvider(blockchain_url))
        if not w3.is_connected():
            print("Failed to connect to blockchain")
            return None
        return w3
    except Exception as e:
        print(f"Error connecting to blockchain: {e}")
        return None

def load_contract(contract_name="ProgressTracker"):
    """
    Load contract ABI and address from environment
    """
    w3 = get_blockchain_connection()
    if not w3:
        return None
    
    try:
        # Load contract ABI from compiled JSON file
        with open(f"src/contracts/{contract_name}.json", 'r') as file:
            contract_data = json.load(file)
        
        # Get contract address from environment
        contract_address = os.getenv(f'{contract_name.upper()}_ADDRESS')
        
        if not contract_address:
            print(f"Contract address for {contract_name} not found in environment")
            return None
        
        # Create contract instance
        contract = w3.eth.contract(
            address=contract_address,
            abi=contract_data['abi']
        )
        
        return contract
    except Exception as e:
        print(f"Error loading contract: {e}")
        return None

def add_student_record(student_address, course_id, grade, activity_type):
    """
    Add a student record to the blockchain
    
    Args:
        student_address (str): Ethereum address of the student
        course_id (str): Course identifier
        grade (int): Grade value (0-100)
        activity_type (str): Type of activity (Quiz, Assignment, Project)
    
    Returns:
        dict: Transaction receipt or error message
    """
    w3 = get_blockchain_connection()
    contract = load_contract()
    
    if not w3 or not contract:
        return {"success": False, "error": "Connection or contract loading failed"}
    
    try:
        # Get admin account from environment
        admin_address = os.getenv('ADMIN_ADDRESS')
        admin_private_key = os.getenv('ADMIN_PRIVATE_KEY')
        
        if not admin_address or not admin_private_key:
            return {"success": False, "error": "Admin credentials not found in environment"}
        
        # Build transaction
        transaction = contract.functions.addRecord(
            student_address,
            course_id,
            grade,
            activity_type
        ).build_transaction({
            'from': admin_address,
            'nonce': w3.eth.get_transaction_count(admin_address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Sign and send transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, admin_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return {
            "success": True,
            "tx_hash": tx_hash.hex(),
            "block_number": tx_receipt['blockNumber']
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_student_records(student_address):
    """
    Get all records for a specific student
    
    Args:
        student_address (str): Ethereum address of the student
    
    Returns:
        list: List of student records or empty list on error
    """
    w3 = get_blockchain_connection()
    contract = load_contract()
    
    if not w3 or not contract:
        print("Connection or contract loading failed")
        return []
    
    try:
        # Call the contract to get records
        records = contract.functions.getStudentRecords(student_address).call()
        
        # Format records for easier processing
        formatted_records = []
        for record in records:
            formatted_records.append({
                'courseID': record[0],
                'timestamp': record[1],
                'date': w3.from_wei(record[1], 'ether'),  # Convert timestamp to readable date
                'grade': record[2],
                'activityType': record[3]
            })
        
        return formatted_records
    
    except Exception as e:
        print(f"Error retrieving student records: {e}")
        return []