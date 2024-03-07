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

toastr.options = {
    progressBar: false,
    positionClass: 'toast-bottom-right',
    preventDuplicates: false,
    onclick: null,
    showMethod: 'show',
    hideMethod: 'hide'
};
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
 function togglenoti(boxId) {
    // var box = document.getElementById(boxId);
    if (box) {
        if (down) {
            box.style.height = '0px';
            box.style.opacity = 0;
            down = false;
            var notificationIds = getAllNotificationIds();
            markNotificationsAsSeen(notificationIds);
        } else {
            box.style.opacity = 1;
            down = true;
            box.style.height = '400px';
        }
    } else {
        console.error("Notification box not found.");
    }
 }
 function getAllNotificationIds() {
     console.log('gather them notification ids,customer ma xam');
     var notificationElements = document.querySelectorAll('.notification-item');
     var notificationIds = Array.from(notificationElements).map(function(element) {
         return element.dataset.notificationId;
     });
     return notificationIds;
 }
 
 function markNotificationsAsSeen(notificationIds) {
     console.log('notificxation laii seen garana janey customer ma xam');
     var csrfToken = getCookie('csrftoken');
     fetch(marknotificationUrl, {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
             'X-CSRFToken': csrfToken,
         },
         body: JSON.stringify({ 'notification_ids': notificationIds }),
     })
     .then(response => {
         if (!response.ok) {
             throw new Error('Network response was not ok');
         }
         return response.json();
     })
     .then(data => {
         console.log('Notifications marked as seen:', data);
     })
     .catch(error => {
         console.error('Error marking notifications as seen:', error);
     });
 }

var currentItem = null; // To store the reference to the currently selected item

function openQuantityPopup(button) {
    currentItem = button.parentNode; // Store the reference to the clicked button's parent (item) for later use
    var quantityPopup = currentItem.querySelector('.quantity-popup');

    // Show the quantity popup
    quantityPopup.style.display = "block";
    quantityPopup.style.top = button.offsetTop + button.offsetHeight + 'px';
    quantityPopup.style.left = button.offsetLeft + 'px';
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

function orderItem(button) {
    console.log('customer just ordered');
    console.log(button.parentElement.parentElement.parentElement);
    currentItem=button.parentElement.parentElement.parentElement;
    var quantity = currentItem.querySelector("#quantityInput").value;
    console.log(quantity);
    var itemName = currentItem.getElementsByClassName('itemName')[0].innerText;
    var itemImage = currentItem.parentElement.querySelector('img').src;
    var itemId = currentItem.dataset.itemId; // assuming the dataset is on the parent element
    var customerID = button.dataset.customerId;
    var customerName = button.dataset.customerName;
    var customerImage = button.dataset.customerImage;

    // Check if the quantity is valid
    if (!isNaN(quantity) && parseInt(quantity) > 0) {
        var created_at = new Date();
        var orderDetails = {
            quantity: quantity,
            itemName: itemName,
            itemImage: itemImage,
            itemId: itemId,
            customerID: customerID,
            customerName: customerName,
            customerImage: customerImage,
            createdAt: created_at
        };
        var csrfToken = getCookie('csrftoken');
        fetch(orderurl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                orderDetails: orderDetails,
            }),
        })
        .then(response => {
            if (response.ok) {
                alert('Order placed');

            } else {
                alert(`order could not be placed`);
            }
        });
        closePopup();
    } else {
        toastr.error('Please enter a valid quantity.');
    }
}

function closePopup(){
    var quantityPopup = currentItem.querySelector('.quantity-popup');
    quantityPopup.style.display = "none";
}