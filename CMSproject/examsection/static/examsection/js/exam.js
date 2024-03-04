// toastr.options = {
//     closeButton: true,
//     debug: false,
//     newestOnTop: false,
//     progressBar: true,
//     positionClass: 'toast-bottom-right',
//     preventDuplicates: false,
//     onclick: null,
//     showDuration: '300',
//     hideDuration: '1000',
//     timeOut: '5000',
//     extendedTimeOut: '1000',
//     showEasing: 'swing',
//     hideEasing: 'linear',
//     showMethod: 'fadeIn',
//     hideMethod: 'fadeOut'
// };

const aside = document.getElementsByClassName("aside")[0];
const main = document.getElementsByClassName("main")[0];
const navbarHeight = document.getElementsByClassName("navbar")[0].clientHeight;
const windowHeight = window.innerHeight;
const profileOptions = document.getElementsByClassName("profileOptions")[0];

function adjustHeight(){
    aside.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.height = (windowHeight - navbarHeight) + 'px';
    main.style.maxHeight = (windowHeight - navbarHeight) + 'px';

}
adjustHeight();

function showProfileOptions(){
    if (profileOptions.style.display === '' || profileOptions.style.display === 'none'){
        profileOptions.style.display = 'block';
    }
    else{
        profileOptions.style.display = 'none';
    }
}
 var box = document.getElementById('batta');
 var down = false;
 function togglenoti()
 {
    if(down){
       box.style.height = '0px';
       box.style.opacity = 0;
       down = false; 
    }
    else{
        box.style.opacity=1;
        down = true;
        box.style.height = '400px';
    
    }
 }
function openFilterModal() {
    console.log('opened the filer form');
    document.getElementById("filterModal").style.display = "flex";
}

function closeFilterModal() {
    console.log('closed the filter form');
    document.getElementById("filterModal").style.display = "none";
}

function handleOptionClick(option) {
    console.log('handle options selected');
    let selectedOption = option;
    console.log(selectedOption);
    if (selectedOption === 'course_Info') {
        openCourseModal();
    } 
    else {
        openFilterModal();
    }
    console.log('yo chalxa ra?');
    document.getElementById('goButton').setAttribute('data-selected-option', selectedOption);
}
//GO button
function applyFilters() {
    var filterMetadata = get_filter_metadata();
    var formData = new FormData();
    let selectedOption = document.getElementById('goButton').getAttribute('data-selected-option');
    console.log('Filter Metadata:', filterMetadata);
    Object.entries(filterMetadata).forEach(([key, value]) => {
        formData.append(key, value);
    });
    console.log('FormData Entries:');
    for (const [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
}
    // Add CSRF token to the headers
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    switch (selectedOption) {
        case 'add_result':
            console.log(addResultUrl);
            fetchAddResult(formData);
            break;
        case 'view_result':
            console.log(viewResultUrl);
            fetchViewResult(formData);
            break;
        case 'student_analysis':
            break;
        case 'course_Info':
            console.log(courseInfoUrl);
            fetchcourseInfo(formData);
            break;
        case 'student_view_result':
            console.log(viewmyResultUrl);
            fetchstudentResult(formData);
            break;
        case 'teacher_add_result':
            console.log(teacheraddResultUrl);
            fetchteacheradd(formData);
            break;
        case 'teacher_view_result':
            console.log(teacherviewResultUrl);
            fetchteacherview(formData);
    }
}
function fetchAddResult(formData) {
    fetch(addResultUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok){
            console.log('unsucessful promise');
            throw new Error(errorMessage);
        }
        else{
            console.log('successful promise');
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        var successMessage = 'Adding result of ' + data.data.exam_type + ' batch: ' + data.data.batch_number + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty;
        console.log(successMessage);
        window.location.href =`/examsection/addresult/${data.data.semester}/${data.data.batch_number}/${data.data.faculty}/${data.data.exam_type}/`;
    })
    .catch(error => {
        toastr.warning(error);
        closeFilterModal();
    })
    .finally(() => {
        closeFilterModal();
    });
}
function fetchViewResult(formData) {
    fetch(viewResultUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            console.log('unsucessfull promise');
            throw new Error('Network response was not ok');
        }
        console.log('successful promise');
        return response.json();
    })
    .then(data => {
        console.log(data);
        var successMessage = 'showing result of ' + data.data.exam_type + ' batch: ' + data.data.batch_number + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty;
        console.log(successMessage);
        let url = '/examsection/viewresult/?';
        if (data.data.semester) {
            url += `semester=${data.data.semester}&`;
        }
        if (data.data.batch_number !== null) {
            url += `batch=${data.data.batch_number}&`;
        }
        if (data.data.faculty) {
            url += `faculty=${data.data.faculty}&`;
        }
        if (data.data.exam_type) {
            url += `exam_type=${data.data.exam_type}&`;
        }
        // Remove the trailing "&" if present
        url = url.slice(0, -1);
        console.log('Redirecting to:', url);
        window.location.href = url;          
    }) 
    .catch(error => {
        if (error.response && error.response.data && error.response.data.errors) {
            console.error('Validation Errors:', error.response.data.errors);
        } else {
            console.error('Fetch error:', error);
        }
        closeCourseModal();  // Close the modal in either case
    })
    .finally(() => {
        closeFilterModal();
    });
}
function fetchcourseInfo(formData) {
    fetch(courseInfoUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            console.log('unsucessful promise');
            throw new Error('Network response was not ok');
        }
        console.log('sucessful promise');
        return response.json();
    })
    .then(data => {
        console.log(data);
        var successMessage = 'showing result of ' + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty;
        console.log(successMessage);
        let url = '/examsection/viewcourseInfo/?';
        if (data.data.semester) {
            url += `semester=${data.data.semester}&`;
        }
        if (data.data.faculty) {
            url += `faculty=${data.data.faculty}&`;
        }
        // Remove the trailing "&" if present
        url = url.slice(0, -1);
        console.log('Redirecting to:', url);
        window.location.href = url;          
    }) 
    .catch(error => {
        if (error.response && error.response.data && error.response.data.errors) {
            console.error('Validation Errors:', error.response.data.errors);
        } else {
            console.error('Fetch error:', error);
        }
        closeCourseModal();  // Close the modal in either case
    })
    .finally(() => {
        closeCourseModal();
    });
}
function fetchstudentResult(formData){
    console.log('url yo:', viewmyResultUrl) ;
    fetch(viewmyResultUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if(!response.ok){
            console.log('Unsuccessful promise');
            return response.json();
        }
        else if (response.ok){
            console.log('successful promise');
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            var successMessage = 'showing result of ' + data.data.exam_type + ', sem: ' + data.data.semester;
            console.log(successMessage);
            let url = '/dashboard/student/viewmyResult/?';
            if (data.data.semester) {
                url += `semester=${data.data.semester}&`;
            }
            if (data.data.exam_type) {
                url += `exam_type=${data.data.exam_type}&`;
            }
            // Remove the trailing "&" if present
            url = url.slice(0, -1);
            console.log('Redirecting to:', url);
            window.location.href = url; 
        }   
        else {
            console.error('Error:', data.error);
            alert(data.error);
        }      
    })
    .finally(() => {
        closeFilterModal();
    });
}
function fetchteacheradd(formData){
    fetch(teacheraddResultUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if(!response.ok){
            console.log('Unsuccessful promise');
            return response.json();
        }
        else if (response.ok){
            console.log('successful promise');
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            var successMessage = 'Adding result of ' + ' batch: ' + data.data.batch_number + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty + 'subject:' + data.data.subject_Name;
            console.log(successMessage);
            window.location.href =`/dashboard/teacher/addResult/${data.data.semester}/${data.data.batch_number}/${data.data.faculty}/${data.data.subject_Name}/`;
        }
        else {
            console.error('Error:', data.error);
            alert(data.error);
        } 
    })
    .finally(() => {
        closeFilterModal();
    });
} 
function fetchteacherview(formData){
    console.log('url yo:', teacherviewResultUrl) ;
    fetch(teacherviewResultUrl, {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if(!response.ok){
            console.log('Unsuccessful promise');
            return response.json();
        }
        else if (response.ok){
            console.log('successful promise');
            return response.json();
        }
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            var successMessage = 'showing result of regular' + ' batch: ' + data.data.batch_number + ', sem: ' + data.data.semester + ', faculty: ' + data.data.faculty + 'subject:' + data.data.subject_Name;
            console.log(successMessage);
            let url = '/dashboard/teacher/viewResult/?';
            if (data.data.semester) {
                url += `semester=${data.data.semester}&`;
            }
            if (data.data.faculty) {
                url += `exam_type=${data.data.faculty}&`;
            }
            if (data.data.batch) {
                url += `exam_type=${data.data.batch}&`;
            }
            if (data.data.subject) {
                url += `exam_type=${data.data.subject}&`;
            }
            // Remove the trailing "&" if present
            url = url.slice(0, -1);
            console.log('Redirecting to:', url);
            window.location.href = url; 
        }   
        else {
            console.error('Error:', data.error);
            alert(data.error);
        }      
    })
    .finally(() => {
        closeFilterModal();
    });
}

//COOKIESSSS
function getCookie(name) {
    console.log('cookies lina aako');
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            console.log('cookies ko loop');
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log('sakkyo cookies liney');
    if (cookieValue === null) {
        console.error('Cookie with name ' + name + ' not found. Cookies may be disabled.');
    }
    return cookieValue;
}

function openCourseModal() {
    console.log('opened filter for course');
     document.getElementById("courseModal").style.display = "flex"; 
}

function closeCourseModal() {
    console.log('closing course filter');
   document.getElementById("courseModal").style.display = "none";
}

function get_filter_metadata() {
    var faculty = document.getElementById('faculty');
    var semester = document.getElementById('semester');
    var examType = document.getElementById('type');
    var batchNumber = document.getElementById('batchNumber');
    var subjectName = document.getElementById('subjectName');

    var filterData = {};

    if (faculty && faculty.value != null && faculty.value.trim() !== "") {
        filterData.faculty = faculty.value;
    }

    if (semester && semester.value != null && semester.value.trim() !== "") {
        filterData.semester = semester.value;
    }

    if (examType && examType.value != null && examType.value.trim() !== "") {
        filterData.exam_type = examType.value;
    }

    if (batchNumber && batchNumber.value != null && batchNumber.value.trim() !== "") {
        filterData.batch_number = batchNumber.value;
    }
    if (subjectName && subjectName.value != null && subjectName.value.trim() !== "") {
        filterData.subject_Name = subjectName.value;
    }
    console.log('this is the filter form data returned:', filterData);
    if (Object.keys(filterData).length > 0) {
        console.log(filterData);
        return filterData;
    } else {
        console.log('No valid filter data found.');
        return null; // or return an empty object, depending on your requirements
    }
}
    
function importData() {
    var fileInput = document.getElementById('fileInput');

    fileInput.addEventListener('change', function (e) {
        var file = e.target.files[0];

        var reader = new FileReader();
        reader.onload = function (e) {
            var data = e.target.result;
            var workbook = XLSX.read(data, { type: 'binary' });
            var sheet = workbook.Sheets[workbook.SheetNames[0]];
            var jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });

            // Display data in the existing table
            displayData(jsonData);
        };

        reader.readAsBinaryString(file);
    });

    // Trigger click event on the file input to open the file selection dialog
    fileInput.click();
}

function displayData(data) {
    var table = document.getElementById('spreadsheetData');

    // Clear existing rows in the table
    while (table.rows.length > 0) {
        table.deleteRow(0);
    }

    // Add data rows including the header row
    for (var j = 0; j < data.length; j++) {
        var row = table.insertRow();
        for (var k = 0; k < data[j].length; k++) {
            var cell = row.insertCell();

            // Set the first row (index 0) to bold
            if (j === 0) {
                cell.style.fontWeight = 'bold';
            }

            cell.textContent = data[j][k];
        }
    }
}

function submitData(url) {
    var table = document.getElementById('spreadsheetData');
    var rows = table.rows;
    var data = [];

    // Iterate through the rows of the table and collect data
    for (var i = 0; i < rows.length; i++) {
        var rowData = [];
        var cells = rows[i].cells;

        // Iterate through the cells of each row
        for (var j = 0; j < cells.length; j++) {
            rowData.push(cells[j].textContent);
        }

        data.push(rowData);
    }

    console.log('Collected Data:', data);

    // Check if there is any data to submit
    if (data.length > 1) { 
        var semester = document.getElementById('submitButton').getAttribute('data-semester');
        var batch = document.getElementById('submitButton').getAttribute('data-batch');
        var faculty = document.getElementById('submitButton').getAttribute('data-faculty'); 
        var exam_type = document.getElementById('submitButton').getAttribute('data-exam_type'); //yesma admin bata huda exam_type nai aaunxa teacher bata huda subject ko value ho haiii: lazy broo
        console.log('we got the stupid data');
        fetch(url, {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ 
                data: data,
                semester:semester,
                batch:batch,
                faculty:faculty,
                exam_type:exam_type,//yesma admin bata huda exam_type nai aaunxa teacher bata huda subject ko value ho haiii: lazy broo
            }),
        })
        .then(response => {
            if (!response.ok) {
                console.log('Unsuccessful promise');
                if (response.status === 400) {
                    // Handle validation error
                    return response.json().then(errorData => {
                        toastr.warning(`Validation error: ${errorData.error}`);
                    });
                } else {
                    // Handle other errors
                    toastr.warning('Error submitting data. Please try again.');
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
            } else {
                console.log('Successful promise');
                toastr.success('Data submitted successfully!');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            toastr.error('Error submitting data. Please try again.');
        });
    } 
    else {
        toastr.warning('No data to submit. Please import a file.');
    }
}

// Delete File
function deleteFile() {
    var fileInput = document.getElementById('fileInput');
    var table = document.getElementById('spreadsheetData');

    // Clear the file input
    fileInput.value = '';

    // Remove existing rows from the table
    while (table.rows.length > 0) {
        table.deleteRow(0);
    }

    // Display delete notification
    toastr.info('File deleted successfully!');
}

toastr.options = {
    closeButton: true,
    progressBar: true,
    preventDuplicates: true,
    positionClass: 'toast-top-right',
    timeOut: 5000,
};
toastr.success('This is a success message');

