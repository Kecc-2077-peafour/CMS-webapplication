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
var down = false;
function togglenoti(boxId) {
    var box = document.getElementById(boxId);
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
     print('gather them notification ids,orders  ma xam');
     var notificationElements = document.querySelectorAll('.notification-item');
     var notificationIds = Array.from(notificationElements).map(function(element) {
         return element.dataset.notificationId;
     });
     return notificationIds;
 }
 
 function markNotificationsAsSeen(notificationIds) {
     print('notificxation laii seen garana janey order ma xam');
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
function confirmOrder(button) {
    var orderId = button.getAttribute('data-order-id');
    var csrfToken = getCookie('csrftoken');
    fetch(confirmOrderurl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify ({
            'order_id':orderId,
            'status':'in-progress',
        }),
    })
    .then(response => {
        if (!response.ok) {
            console.log('unsucessful');
        }
        console.log('sucessfull');
        location.reload();
    })
    console.log('staff clicked confirmed the order');
}