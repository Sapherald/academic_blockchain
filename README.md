# SL01 - Student Learning Records Module

This module implements the Student Learning Records (SL01) component for the Transparent And Efficient Academic Management System Using Blockchain Technology. It allows storing key milestones like quiz scores and assignment grades as blockchain transactions.

## Project Structure

- `ProgressTracker.sol`: Smart contract that stores student learning records
- `student_learning_records.py`: Python interface to interact with the blockchain contract
- `compile_contract.py`: Helper script to compile the smart contract
- `README.md`: This documentation file

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for running a local blockchain like Ganache)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/academic-blockchain-sl01.git
   cd academic-blockchain-sl01
   ```

2. Install the required Python packages:
   ```
   pip install web3 py-solc-x
   ```

3. Install and run Ganache (local blockchain for development):
   ```
   npm install -g ganache-cli
   ganache-cli
   ```
   Or download and run the Ganache UI application from [trufflesuite.com/ganache](https://trufflesuite.com/ganache/)

## Setup Steps

1. Compile the smart contract:
   ```
   python compile_contract.py
   ```
   This will generate `contract_abi.json` and `contract_bytecode.txt` files

2. Deploy the contract to your blockchain:
   ```
   python student_learning_records.py --deploy --address YOUR_ETHEREUM_ADDRESS --key YOUR_PRIVATE_KEY
   ```
   Replace `YOUR_ETHEREUM_ADDRESS` and `YOUR_PRIVATE_KEY` with your actual Ethereum address and private key from Ganache

## Usage

### Add an Educator
```
python student_learning_records.py --add-educator EDUCATOR_ADDRESS --address ADMIN_ADDRESS --key ADMIN_PRIVATE_KEY
```

### Add a Student Record
```
python student_learning_records.py --add-record --address EDUCATOR_ADDRESS --key EDUCATOR_PRIVATE_KEY --student STUDENT_ADDRESS --course "CS101" --grade 85 --activity "Quiz" --description "Midterm Quiz on Blockchain Basics"
```

### Get Student Records
```
python student_learning_records.py --get-records STUDENT_ADDRESS
```

## Extending the Project

This module can be extended in several ways:
- Create a web interface using Flask or Django
- Add batch import/export functionality
- Implement more advanced analytics on student performance
- Connect with other modules like VS01 (visualization dashboard)

## Smart Contract Details

The `ProgressTracker` contract includes:
- Storage of student records with course ID, timestamp, grade, activity type, and description
- Access control for educators and administrators
- Functions to add and retrieve student records
- Event emission when records are added

## Security Considerations

- Never hard-code private keys in your application
- Use .env files or secure environment variables for sensitive information
- Consider adding more access control mechanisms for production use
- Implement proper input validation before submitting transactions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
