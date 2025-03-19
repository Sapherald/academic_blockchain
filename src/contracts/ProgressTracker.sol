// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProgressTracker {
    // Define the structure for a student record
    struct Record {
        string courseID;
        uint256 timestamp;
        uint8 grade; // Grade out of 100
        string activityType; // e.g., "Quiz", "Assignment", "Project"
    }
    
    // Mapping from student address to their array of records
    mapping(address => Record[]) public studentRecords;
    
    // Event to emit when a new record is added
    event RecordAdded(
        address indexed student,
        string courseID,
        uint8 grade,
        string activityType,
        uint256 timestamp
    );
    
    // Role-based access control (simple version)
    address public owner;
    mapping(address => bool) public authorizedEducators;
    
    modifier onlyOwnerOrEducator() {
        require(msg.sender == owner || authorizedEducators[msg.sender], "Not authorized");
        _;
    }
    
    // Constructor to set the contract owner
    constructor() {
        owner = msg.sender;
    }
    
    // Add or remove educators
    function setEducator(address _educator, bool _status) public {
        require(msg.sender == owner, "Only owner can manage educators");
        authorizedEducators[_educator] = _status;
    }
    
    // Add a new record for a student
    function addRecord(
        address _student,
        string memory _courseID,
        uint8 _grade,
        string memory _activityType
    ) public onlyOwnerOrEducator {
        // Validate grade range
        require(_grade <= 100, "Grade must be between 0 and 100");
        
        // Add the record to the student's records
        studentRecords[_student].push(Record({
            courseID: _courseID,
            timestamp: block.timestamp,
            grade: _grade,
            activityType: _activityType
        }));
        
        // Emit event
        emit RecordAdded(_student, _courseID, _grade, _activityType, block.timestamp);
    }
    
    // Get all records for a specific student
    function getStudentRecords(address _student) public view returns (Record[] memory) {
        return studentRecords[_student];
    }
    
    // Get the count of records for a student
    function getRecordCount(address _student) public view returns (uint256) {
        return studentRecords[_student].length;
    }
    
    // Get the average grade for a student across all records
    function getAverageGrade(address _student) public view returns (uint8) {
        Record[] memory records = studentRecords[_student];
        uint256 recordCount = records.length;
        
        if (recordCount == 0) {
            return 0;
        }
        
        uint256 total = 0;
        for (uint256 i = 0; i < recordCount; i++) {
            total += records[i].grade;
        }
        
        return uint8(total / recordCount);
    }
}