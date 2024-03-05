

// Function to enable editing
function enableEdit() {
    console.log('edit editing function');
    if (editingAllowed) {
        console.log('editing allowed if');
        var cells = document.querySelectorAll('.table-hover td');
        cells.forEach(function(cell, index) {
            // Skip first two columns (index 0 and 1)
            if (index > 1) {
                cell.contentEditable = true;
            }
        });
    }
}


// Function to save edited data
function saveData() {
    editingAllowed = false;
    var cells = document.querySelectorAll('.table-hover td');
    cells.forEach(function(cell) {
        cell.contentEditable = false;
    });
    var table = document.getElementById('table-fill');
    var rows = table.rows;
    var data = [];
    // Iterate through the cells of the table
    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].cells;
        var studentId = rows[i].cells[1].getAttribute('data-student-id');
        // Iterate through the cells of each row starting from index 2
        for (var j = 2; j < cells.length; j++) {
            var cell = cells[j];
            var originalValue = cell.getAttribute('data-original-value');
            var currentValue = cell.textContent;
            var subjectId = cell.getAttribute('data-subject-id');  // Assuming data-entry-id is the subjectId
            var marksId = cell.getAttribute('data-marks-id');  // Assuming data-entry-id is the subjectId
            console.log('student: marks',studentId,subjectId,marksId,originalValue,currentValue);
            // Check if the value has changed
            if (originalValue !== currentValue) {
                data.push({
                    'studentId': studentId,
                    'subjectId': subjectId,
                    'marksId':marksId,
                    'previousData': originalValue,
                    'presentData': currentValue
                });
            }
        }
    }
    console.log('Collected Data:', data);
    fetch(editresultUrl, {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ 
            data: data,
        }),
    })
    .then(response => {
        if (response.ok) {
            // Handle success
            alert('Edited successfully!');
            // You can also perform additional actions or update the UI as needed
        } else if (response.status === 400) {
            // Handle bad request
            alert('Invalid Data: Please enter valid data');
        } else {
            // Handle other errors
            alert('An unexpected error occurred');
        }
    })
}
function enableEditing() {
    console.log('enable editing function');
    editingAllowed = true;
    enableEdit();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}