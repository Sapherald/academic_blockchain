# src/blockchain_service.py

from web3 import Web3
from typing import Dict, List
import json
import os
from dotenv import load_dotenv

class BlockchainService:
    def __init__(self):
        load_dotenv()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_URL')))
        
        # Load contract ABI and address
        with open('contracts/StudentLearningRecords.json') as f:
            contract_json = json.load(f)
        self.contract = self.w3.eth.contract(
            address=os.getenv('CONTRACT_ADDRESS'),
            abi=contract_json['abi']
        )

    def record_assessment(self, 
                         student_address: str, 
                         assessment_id: str,
                         assessment_type: str,
                         score: int,
                         max_score: int,
                         metadata: str) -> Dict:
        """
        Record a new assessment for a student
        """
        try:
            tx_hash = self.contract.functions.recordAssessment(
                student_address,
                assessment_id,
                assessment_type,
                score,
                max_score,
                metadata
            ).transact({
                'from': self.w3.eth.default_account
            })
            
            # Wait for transaction to be mined
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return {
                'status': 'success',
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def get_student_assessments(self, student_address: str) -> List[Dict]:
        """
        Retrieve all assessments for a student
        """
        try:
            assessments = self.contract.functions.getStudentAssessments(
                student_address
            ).call()
            
            return [{
                'assessment_id': assessment[0],
                'assessment_type': assessment[1],
                'max_score': assessment[2],
                'score': assessment[3],
                'timestamp': assessment[4],
                'metadata': assessment[5]
            } for assessment in assessments]
        except Exception as e:
            return []

    def get_latest_assessment(self, student_address: str) -> Dict:
        """
        Get the most recent assessment for a student
        """
        try:
            assessment = self.contract.functions.getLatestAssessment(
                student_address
            ).call()
            
            return {
                'assessment_id': assessment[0],
                'assessment_type': assessment[1],
                'max_score': assessment[2],
                'score': assessment[3],
                'timestamp': assessment[4],
                'metadata': assessment[5]
            }
        except Exception as e:
            return None
