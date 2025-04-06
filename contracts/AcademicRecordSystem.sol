// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AcademicRecordSystem {
    address public admin;
    
    struct MilestoneRecord {
        string courseID;
        uint256 timestamp;
        uint8 score;        // Score out of 100
        string recordType;  // "Quiz", "Assignment", "Exam", etc.
        string description; // Brief description of the milestone
        bool verified;      // Whether this record has been verified by an educator
    }
    
    // Mapping from student address to their records
    mapping(address => MilestoneRecord[]) public studentRecords;
    
    // Mapping of authorized educators
    mapping(address => bool) public authorizedEducators;
    
    // Events
    event RecordAdded(address indexed student, string courseID, string recordType, uint8 score);
    event RecordVerified(address indexed student, uint256 recordIndex);
    event EducatorAuthorized(address indexed educator);
    event EducatorRevoked(address indexed educator);
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    modifier onlyEducator() {
        require(authorizedEducators[msg.sender] || msg.sender == admin, "Only authorized educators can perform this action");
        _;
    }
    
    constructor() {
        admin = msg.sender;
        authorizedEducators[msg.sender] = true;
    }
    
    // Add a new educator
    function authorizeEducator(address _educator) public onlyAdmin {
        authorizedEducators[_educator] = true;
        emit EducatorAuthorized(_educator);
    }
    
    // Revoke educator access
    function revokeEducator(address _educator) public onlyAdmin {
        authorizedEducators[_educator] = false;
        emit EducatorRevoked(_educator);
    }
    
    // Add a new academic record
    function addRecord(
        address _student,
        string memory _courseID,
        uint8 _score,
        string memory _recordType,
        string memory _description
    ) public onlyEducator {
        require(_score <= 100, "Score must be between 0 and 100");
        
        studentRecords[_student].push(MilestoneRecord({
            courseID: _courseID,
            timestamp: block.timestamp,
            score: _score,
            recordType: _recordType,
            description: _description,
            verified: true  // Auto-verified if added by an educator
        }));
        
        emit RecordAdded(_student, _courseID, _recordType, _score);
    }
    
    // Student can submit their own record (needs verification)
    function submitRecord(
        string memory _courseID,
        uint8 _score,
        string memory _recordType,
        string memory _description
    ) public {
        require(_score <= 100, "Score must be between 0 and 100");
        
        studentRecords[msg.sender].push(MilestoneRecord({
            courseID: _courseID,
            timestamp: block.timestamp,
            score: _score,
            recordType: _recordType,
            description: _description,
            verified: false  // Needs verification
        }));
        
        emit RecordAdded(msg.sender, _courseID, _recordType, _score);
    }
    
    // Educator verifies a student-submitted record
    function verifyRecord(address _student, uint256 _recordIndex) public onlyEducator {
        require(_recordIndex < studentRecords[_student].length, "Record does not exist");
        studentRecords[_student][_recordIndex].verified = true;
        emit RecordVerified(_student, _recordIndex);
    }
    
    // Get all records for a student
    function getStudentRecords(address _student) public view returns (MilestoneRecord[] memory) {
        return studentRecords[_student];
    }
    
    // Get record count for a student
    function getRecordCount(address _student) public view returns (uint256) {
        return studentRecords[_student].length;
    }
    
    // Get a specific record
    function getRecord(address _student, uint256 _index) public view returns (
        string memory courseID,
        uint256 timestamp,
        uint8 score,
        string memory recordType,
        string memory description,
        bool verified
    ) {
        require(_index < studentRecords[_student].length, "Record does not exist");
        MilestoneRecord memory record = studentRecords[_student][_index];
        
        return (
            record.courseID,
            record.timestamp,
            record.score,
            record.recordType,
            record.description,
            record.verified
        );
    }
}