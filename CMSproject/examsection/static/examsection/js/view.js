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
// Flag to indicate whether editing is allowed
var editingAllowed = false;

// Function to enable editing
function enableEdit() {
    if (editingAllowed) {
        var cells = document.querySelectorAll('.table-hover td');
        cells.forEach(function(cell) {
            cell.contentEditable = true;
        });
    }
}

// Function to disable editing
function disableEdit() {
    var cells = document.querySelectorAll('.table-hover td');
    cells.forEach(function(cell) {
        cell.contentEditable = false;
    });
}

// Function to save edited data
function saveData() {
    disableEdit();
    editingAllowed = false; // Disable editing after saving
}

// Add event listener to the edit button
document.addEventListener('DOMContentLoaded', function() {
    var editButton = document.querySelector('.editButton');
    editButton.addEventListener('click', function() {
        enableEditing();
    });

    // Add event listener to the save button
    var saveButton = document.querySelector('.saveButton');
    saveButton.addEventListener('click', function() {
        saveData();
    });

    // Add event listeners to table cells
    var cells = document.querySelectorAll('td');
    cells.forEach(function(cell) {
        cell.addEventListener('click', function() {
            enableEdit();
        });
    });

    // Call disableEdit initially to ensure editing is disabled by default
    disableEdit();
});

// Function to enable editing only if the editing is allowed
function enableEditing() {
    editingAllowed = true;
    enableEdit();
}

// Function to handle click for edit button
function editButtonClick() {
    enableEditing();
}

// Function to handle click for click button
function handleClick() {
    alert("You clicked the button!");
}