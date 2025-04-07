// milestone.js
document.addEventListener('DOMContentLoaded', function() {
    const milestoneForm = document.getElementById('milestoneForm');
    const resultBox = document.getElementById('result');

    milestoneForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading state
        resultBox.className = 'result-box';
        resultBox.innerHTML = '<p>Processing transaction... This may take a moment.</p>';
        resultBox.style.display = 'block';
        
        // Get form data
        const formData = {
            student_id: document.getElementById('student_id').value,
            student_name: document.getElementById('student_name').value,
            course_id: document.getElementById('course_id').value,
            instructor_name: document.getElementById('instructor_name').value,
            activity_type: document.getElementById('activity_type').value,
            score: parseFloat(document.getElementById('score').value),
            max_score: parseFloat(document.getElementById('max_score').value),
            comments: document.getElementById('comments').value,
            record_type: document.getElementById('record_type').value
        };
        
        // Validate input
        if (formData.max_score <= 0) {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = '<p><strong>Error:</strong> Maximum score must be greater than zero.</p>';
            return;
        }
        
        // Send data to server
        fetch('/add_milestone', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                resultBox.className = 'result-box success';
                resultBox.innerHTML = `
                    <p><strong>Success!</strong> ${data.message}</p>
                    <p>Percentage: ${data.percentage}%</p>
                    <p>Grade: ${data.grade}</p>
                `;
                
                // Reset form
                milestoneForm.reset();
            } else {
                resultBox.className = 'result-box error';
                resultBox.innerHTML = `<p><strong>Error:</strong> ${data.error}</p>`;
            }
        })
        .catch(error => {
            resultBox.className = 'result-box error';
            resultBox.innerHTML = `<p><strong>Error:</strong> ${error.message}</p>`;
        });
    });
});

// records.js
document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const searchStudentId = document.getElementById('search_student_id');
    const searchCourseId = document.getElementById('search_course_id');
    const summaryBox = document.getElementById('summary');
    const recordsContainer = document.getElementById('records-container');
    const recordsBody = document.getElementById('records-body');
    
    searchBtn.addEventListener('click', function() {
        const studentId = searchStudentId.value.trim();
        const courseId = searchCourseId.value.trim();
        
        if (!studentId) {
            alert('Please enter a Student ID');
            return;
        }
        
        // Hide previous results
        summaryBox.classList.add('hidden');
        recordsContainer.classList.add('hidden');
        
        // Fetch records
        let url = `/student_records?student_id=${studentId}`;
        if (courseId) {
            url += `&course_id=${courseId}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                if (data.records.length === 0) {
                    alert('No records found for this student');
                    return;
                }
                
                // Display records
                displayRecords(data.records);
                
                // If course ID is provided, fetch and display average
                if (courseId) {
                    fetchCourseAverage(studentId, courseId);
                }
            })
            .catch(error => {
                alert('Error fetching records: ' + error.message);
            });
    });
    
    function displayRecords(records) {
        recordsBody.innerHTML = '';
        
        records.forEach(record => {
            const date = new Date(record.timestamp * 1000).toLocaleDateString();
            let gradeClass = '';
            
            switch(record.grade) {
                case 'A': gradeClass = 'grade-a'; break;
                case 'B': gradeClass = 'grade-b'; break;
                case 'C': gradeClass = 'grade-c'; break;
                case 'D': gradeClass = 'grade-d'; break;
                case 'F': gradeClass = 'grade-f'; break;
            }
            
            recordsBody.innerHTML += `
                <tr>
                    <td>${date}</td>
                    <td>${record.course_id}</td>
                    <td>${record.activity_type}</td>
                    <td>${record.score}/${record.max_score}</td>
                    <td>${record.percentage}%</td>
                    <td class="${gradeClass}">${record.grade}</td>
                    <td>${record.instructor_name}</td>
                </tr>
            `;
        });
        
        recordsContainer.classList.remove('hidden');
    }
    
    function fetchCourseAverage(studentId, courseId) {
        fetch(`/course_average?student_id=${studentId}&course_id=${courseId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    return;
                }
                
                let gradeClass = '';
                switch(data.letter_grade) {
                    case 'A': gradeClass = 'grade-a'; break;
                    case 'B': gradeClass = 'grade-b'; break;
                    case 'C': gradeClass = 'grade-c'; break;
                    case 'D': gradeClass = 'grade-d'; break;
                    case 'F': gradeClass = 'grade-f'; break;
                }
                
                summaryBox.innerHTML = `
                    <h4>Course Summary for ${courseId}</h4>
                    <div class="summary-stats">
                        <div class="stat-item">
                            <div class="stat-value">${data.average}%</div>
                            <div class="stat-label">Course Average</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value ${gradeClass}">${data.letter_grade}</div>
                            <div class="stat-label">Letter Grade</div>
                        </div>
                    </div>
                `;
                
                summaryBox.classList.remove('hidden');
            })
            .catch(error => {
                console.error('Error fetching course average:', error);
            });
    }
});
