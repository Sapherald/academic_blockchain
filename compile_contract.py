import json
import solcx
from pathlib import Path

def compile_contract():
    print("Installing solc compiler...")
    solcx.install_solc('0.8.17')
    
    print("Compiling ProgressTracker.sol...")
    contract_path = Path(__file__).parent / "ProgressTracker.sol"
    
    # Ensure the contract file exists
    if not contract_path.exists():
        with open(contract_path, 'w') as file:
            file.write("""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProgressTracker {
    struct Record {
        string courseID;
        uint256 timestamp;
        uint8 grade; // Grade out of 100
        string activityType; // e.g., "Quiz", "Assignment", "Project"
        string description; // Additional details about the activity
    }
    
    mapping(address => Record[]) public studentRecords;
    mapping(address => bool) public authorizedEducators;
    address public admin;
    
    event RecordAdded(address indexed student, string courseID, uint8 grade, string activityType);
    
    constructor() {
        admin = msg.sender;
        authorizedEducators[msg.sender] = true;
    }
    
    modifier onlyAuthorized() {
        require(authorizedEducators[msg.sender] || msg.sender == admin, "Not authorized");
        _;
    }
    
    function addEducator(address _educator) public {
        require(msg.sender == admin, "Only admin can add educators");
        authorizedEducators[_educator] = true;
    }
    
    function removeEducator(address _educator) public {
        require(msg.sender == admin, "Only admin can remove educators");
        authorizedEducators[_educator] = false;
    }
    
    function addRecord(
        address _student,
        string memory _courseID,
        uint8 _grade,
        string memory _activityType,
        string memory _description
    ) public onlyAuthorized {
        require(_grade <= 100, "Grade must be between 0 and 100");
        
        studentRecords[_student].push(Record({
            courseID: _courseID,
            timestamp: block.timestamp,
            grade: _grade,
            activityType: _activityType,
            description: _description
        }));
        
        emit RecordAdded(_student, _courseID, _grade, _activityType);
    }
    
    function getStudentRecords(address _student) public view returns (
        string[] memory courseIDs,
        uint256[] memory timestamps,
        uint8[] memory grades,
        string[] memory activityTypes,
        string[] memory descriptions
    ) {
        Record[] memory records = studentRecords[_student];
        uint256 length = records.length;
        
        courseIDs = new string[](length);
        timestamps = new uint256[](length);
        grades = new uint8[](length);
        activityTypes = new string[](length);
        descriptions = new string[](length);
        
        for (uint256 i = 0; i < length; i++) {
            courseIDs[i] = records[i].courseID;
            timestamps[i] = records[i].timestamp;
            grades[i] = records[i].grade;
            activityTypes[i] = records[i].activityType;
            descriptions[i] = records[i].description;
        }
        
        return (courseIDs, timestamps, grades, activityTypes, descriptions);
    }
    
    function getStudentRecordCount(address _student) public view returns (uint256) {
        return studentRecords[_student].length;
    }
}""")
    
    # Compile the contract
    compiled_sol = solcx.compile_files(
        [contract_path],
        output_values=['abi', 'bin'],
        solc_version='0.8.17'
    )
    
    contract_id = f"{contract_path}:ProgressTracker"
    contract_interface = compiled_sol[contract_id]
    
    abi = contract_interface['abi']
    bytecode = contract_interface['bin']
    
    # Save ABI
    with open(Path(__file__).parent / "contract_abi.json", 'w') as f:
        json.dump(abi, f)
        
    # Save bytecode
    with open(Path(__file__).parent / "contract_bytecode.txt", 'w') as f:
        f.write(bytecode)
    
    print("Contract compiled successfully!")
    print(f"ABI saved to: {Path(__file__).parent / 'contract_abi.json'}")
    print(f"Bytecode saved to: {Path(__file__).parent / 'contract_bytecode.txt'}")

if __name__ == "__main__":
    compile_contract()
