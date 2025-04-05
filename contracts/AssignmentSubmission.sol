// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AcademicMilestones {
    
    // Structure to store a student's record
    struct Record {
        string courseID;
        uint256 timestamp;
        uint8 grade; // Grade out of 100
        string activityType; // "Quiz", "Assignment", etc.
    }

    // Mapping of student address to their records
    mapping(address => Record[]) private studentRecords;

    // Address of the contract owner (admin/educator)
    address public owner;

    // Modifier to restrict access
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this.");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /// @notice Add a performance record for a student
    /// @param _student Address of the student
    /// @param _courseID ID of the course
    /// @param _grade Grade received (0-100)
    /// @param _activityType Type of activity (e.g., Quiz, Assignment)
    function addRecord(
        address _student,
        string memory _courseID,
        uint8 _grade,
        string memory _activityType
    ) public onlyOwner {
        require(_grade <= 100, "Grade must be between 0 and 100");
        studentRecords[_student].push(Record({
            courseID: _courseID,
            timestamp: block.timestamp,
            grade: _grade,
            activityType: _activityType
        }));
    }

    /// @notice Retrieve all records of a student
    /// @param _student Address of the student
    /// @return Array of Record structs
    function getStudentRecords(address _student) public view returns (Record[] memory) {
        return studentRecords[_student];
    }

    /// @notice Transfer ownership of the contract
    /// @param _newOwner Address of the new owner
    function transferOwnership(address _newOwner) public onlyOwner {
        owner = _newOwner;
    }
}
