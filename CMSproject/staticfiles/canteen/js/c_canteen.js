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
    progressBar: true,
    positionClass: 'toast-bottom-right',
    preventDuplicates: false,
    onclick: null,
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
        // box.style.width = '220px';
    }
 }

var currentItem = null; // To store the reference to the currently selected item

function openQuantityPopup(button) {
    currentItem = button.parentNode; // Store the reference to the clicked button's parent (item) for later use
    var quantityPopup = currentItem.querySelector('.quantity-popup');

        // Show the quantity popup
        document.getElementById("quantityPopup").style.display = "block";
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

function orderItem(url) {
    console.log("order item function call vayo");
    var quantity = document.getElementById("quantityInput").value;
    var itemName = currentItem.querySelector('.itemName').innerText;
    // Check if the quantity is valid
    if (!isNaN(quantity) && parseInt(quantity) > 0) {
        toastr.success("You ordered " + quantity + " " + itemName + "(s).");
        console.log('THE ORDER WAS PLACED');
        closePopup();
        var created_at = new Date();
        var customerID = currentItem.dataset.customerId;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                item_id: currentItem.dataset.itemId,
                quantity: quantity,
                customer_id: customerID,
                created_at: created_at,
            }),
        })
        .then(response => {
            if (response.ok) {
                return response.json(); 
                 // Assuming your server returns JSON data
            } else {
                console.error('Failed to place order',response);
                throw new Error('Failed to place order');
            }
        })
        .then(data => {
            var orderInfo = document.createElement('div');
            orderInfo.classList.add('orders'); 
        
            // Set the inner HTML of the orderInfo div with the order details
            orderInfo.innerHTML = `
                <p>Order: ${data.item_name}</p>
                <img src="${data.item_image}" alt="${data.item_name} Image">
                <p>Quantity: ${data.quantity}</p>
                <p>Created At: ${data.created_at}</p>
                <p>Customer: ${data.customer_name}</p>
                <img src="${data.customer_image}" alt="${data.customer_name} Image">
                <p>User Type: ${data.user_type}</p>
                <button onclick="confirmOrder(data,'{% url 'confirm_order' %}')">Confirm Order</button>
                <button onclick="rejectOrder(data)">Reject Order</button>
            `;
        
            // Assuming you have a container with ID 'displayOrder' in your HTML
            var displayOrder = document.getElementById('displayOrder');
            displayOrder.appendChild(orderInfo);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }
    else {
       toastr.error('Please ender a valid quantity.');
    }}


function confirmOrder(data,url){
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            item_id: data.item_id,
            quantity: data.quantity,
            customer_id: data.customer_id,
            created_at: data.created_at,
            status:'in-progress'
        }),
    })
    .then(response => {
        //reload the page 
    })
}

function closePopup(){
    var quantityPopup = currentItem.querySelector('.quantity-popup');
    quantityPopup.style.display = "none";
}