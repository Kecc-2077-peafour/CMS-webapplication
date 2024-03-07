// Initialize Toastr
toastr.options = {
    closeButton: true,
    debug: false,
    // other options...
};

// Function to enable editing
function enableEdit() {
    if (editingAllowed) {
        document.querySelectorAll('.table-hover td').forEach(function (cell, index) {
            // Skip first two columns (index 0 and 1)
            if (index > 1) {
                cell.contentEditable = true;
            }
        });
    }
}

// Function to disable editing
function disableEdit() {
    document.querySelectorAll('.table-hover td').forEach(function (cell) {
        cell.contentEditable = false;
    });
}

// Function to collect edited data
function collectEditedData() {
    var data = [];
    var validationErrors = [];

    var table = document.getElementById('table-fill');
    var rows = table.rows;

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].cells;
        var studentId = rows[i].cells[1].getAttribute('data-student-id');

        for (var j = 2; j < cells.length; j++) {
            var cell = cells[j];
            var originalValue = cell.getAttribute('data-original-value');
            var currentValue = cell.textContent;
            var subjectId = cell.getAttribute('data-subject-id');
            var marksId = cell.getAttribute('data-marks-id');

            if (originalValue !== currentValue) {
                var numericValue = parseFloat(currentValue);

                if (isNaN(numericValue) || numericValue < 0 || numericValue > 100) {
                    validationErrors.push('Invalid marks for Student ID: ' + studentId);
                } else {
                    data.push({
                        'studentId': studentId,
                        'subjectId': subjectId,
                        'marksId': marksId,
                        'previousData': originalValue,
                        'presentData': currentValue
                    });
                }
            }
        }
    }

    // Display validation error only once
    if (validationErrors.length > 0) {
        toastr.error(validationErrors[0]);
        return [];
    }

    console.log('Collected Data:', data);
    return data;
}

// Function to handle fetch response
function handleResponse(response) {
    if (response.ok) {
        var data = collectEditedData();

        // Display success message only when data is less than 100
        if (data.length > 0 && parseFloat(data[0].presentData) < 100) {
            toastr.success('Successfully saved!');
            updateTableData();
        }
    } else if (response.status === 400) {
        toastr.error('Invalid Data: Please enter valid data');
    } else {
        toastr.error('An unexpected error occurred');
    }
}

// Function to handle fetch errors
function handleError(error) {
    console.error('Fetch error:', error);
    toastr.error('An unexpected error occurred');
}

// Function to save edited data
function saveData() {
    editingAllowed = false;
    disableEdit();
    var data = collectEditedData();

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
        .then(handleResponse)
        .catch(handleError);
}

// Function to enable editing
function enableEditing() {
    console.log('enable editing function');
    editingAllowed = true;
    enableEdit();
}

// Function to get cookie value
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

// Function to update table data after successful save
function updateTableData() {
    var table = document.getElementById('table-fill');
    var rows = table.rows;

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].cells;

        for (var j = 2; j < cells.length; j++) {
            var cell = cells[j];
            var marksId = cell.getAttribute('data-marks-id');
            var editedData = findEditedData(marksId);

            if (editedData) {
                cell.textContent = editedData.presentData;
                cell.setAttribute('data-original-value', editedData.presentData);
            }
        }
    }
}

// Function to find edited data by marksId
function findEditedData(marksId) {
    var data = collectEditedData();
    return data.find(item => item.marksId === marksId);
}
