// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AcademicRecordSystem {
    struct Record{
        string courseID;
        uint256 timestamp;
        uint8 score;        // Score out of 100
        string grade;       // "A", "B", "C", "D", "E", "F"
        string recordType;  // "Quiz", "Assignment", "Exam", etc.
        string description; // Brief description of the milestone
    }
    
    // Mapping from student address to their records
    mapping(address => Record[]) public studentRecords;
    
    // Mapping of authorized educators
    mapping(address => bool) public authorizedEducators;
    address public admin;
    
    // Events
    event RecordAdded(address indexed student, string courseID, uint8 score, string grade, string recordType);

    constructor() {
        admin = msg.sender;
        authorizedEducators[msg.sender] = true;
    }

   modifier onlyAuthorized() {
        require(authorizedEducators[msg.sender] || msg.sender == admin, "Only authorized educators can perform this action");
        _;
    }    

    // Add a new educator
    function addEducator(address _educator) public {
        require(msg.sender == admin, "Only admin can add educators");
        authorizedEducators[_educator] = true;
    }
    
    // Revoke educator access
    function revokeEducator(address _educator) public {
        require(msg.sender == admin, "Only admin can remove educators");
        authorizedEducators[_educator] = false;
    }
    
    // Add a new academic record
    function addRecord(
        address _student,
        string memory _courseID,
        uint8 _score,
        string grade,
        string memory _recordType,
        string memory _description
    ) public onlyAuthorized {
        require(_score <= 100, "Score must be between 0 and 100");
        
        studentRecords[_student].push(Record({
            courseID: _courseID,
            timestamp: block.timestamp,
            score: _score,
            grade: _grade,
            recordType: _recordType,
            description: _description,
        }));
        
        emit RecordAdded(_student, _courseID, _recordType, _score, _grade);
    }


    // Student can view their result
    function getStudentRecords(address_student)public view returns (
        string[]memory courseIDs,
        string[]memory timestamps,
        string[]memory scores,
        string[]memory grades, 
        string[]recordTypes,
        string[]memory descriptions,
    ){

    Record[] memory records = studentRecords[_student];
    uint256 length = records.length;

    courseIDs = new string[](length);
    timestamps = new uint256[](length);
    scores = new uint8[](length);
    grades = new string[](length);
    activityTypes = new string[](length);
    descriptions = new string[](length);

 for (uint256 i = 0; i < length; i++) {
            courseIDs[i] = records[i].courseID;
            timestamps[i] = records[i].timestamp;
            scores[i] = records[i].score;
            grades[i] = records[i].grade;
            activityTypes[i] = records[i].activityType;
            descriptions[i] = records[i].description;
        }
        
        return (courseIDs, timestamps, scores, grades, activityTypes, descriptions);
    }
    
    function getStudentRecordCount(address _student) public view returns (uint256) {
        return studentRecords[_student].length;
    }
}
