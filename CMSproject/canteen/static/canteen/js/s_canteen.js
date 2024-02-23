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

    }
 }

function addmenuItem() {
    console.log('retriving the addded data menu');
    var itemName = document.getElementById("itemsName").value;
    var itemPrice = document.getElementById("itemsPrice").value;
    var itemDescription = document.getElementById("itemsDescription").value;
    var itemImageInput = document.getElementById("itemsImageInput");

    // Check if a file is selected
    if (itemImageInput.files.length > 0) {
        var itemImage = URL.createObjectURL(itemImageInput.files[0]);
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Prepare the data for the fetch request
        var formData = new FormData();
        formData.append('itemsName', itemName);
        formData.append('itemsPrice', itemPrice);
        formData.append('itemsDescription', itemDescription);
        formData.append('itemsImageInput', itemImageInput.files[0]);
        var url = document.querySelector('button[data-url]').dataset.url;
        // Send the data to the server using fetch
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('sucessful promise');
            console.log(data);
            var newItem = document.createElement("div");
            newItem.className = "item";
            newItem.innerHTML = `
                <img src="${itemImage}" alt="${itemName}">
                <div class="itemName">${itemName}</div>
                <div class="itemDescription">${data.item.description}</div>
                <div class="itemPrice"> Rs. ${itemPrice} /- </div>
                <button onclick="deleteItem(this, '{% url 'delete_menuItem' %}')">Delete Item</button>
                <button onclick="AddToSpecial(this)" data-urls="{% url 'add_specialItem' %}" >Add to Specials</button>
            `;
            document.getElementById("menus").appendChild(newItem);
            // Clear input fields after adding the item
            document.getElementById("itemsName").value = "";
            document.getElementById("itemsPrice").value = "";
            document.getElementById("itemsDescription").value = "";
            itemImageInput.value = ""; // Clear the file input
        })
        .catch(error => {
            console.log('unsucessful promise');
            console.error('Error:', error);
        });
    } else {
        toastr.error('Please select an image for the item.');
    }
}

function AddToSpecial(button) {
    console.log('adding the menu to special..');
    var itemDiv = button.parentNode;
    // get item details
    var itemName = itemDiv.querySelector(".itemName").textContent;
    var itemPrice = itemDiv.querySelector(".itemPrice").textContent;
    var itemDescription = itemDiv.querySelector(".itemDescription").textContent;
    var itemImageSrc = itemDiv.querySelector("img").src;
    var urls = button.dataset.urls;
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(urls, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken, 
        },
        body: JSON.stringify({
            itemName: itemName,
            special: true
        })
    })
    .then(response => {
        if (response.ok) {
            console.log('sucessful promise');
            var newItem = document.createElement("div");
            newItem.classList.add("item");
            newItem.innerHTML = `
                <img src="${itemImageSrc}" alt="${itemName}">
                <div class="itemName">${itemName}</div>
                <div class="itemDescription">${itemDescription}</div>
                <div class="itemPrice">${itemPrice}</div>
                <button onclick="deleteItem(this, '{% url 'delete_specialItem' %}')">Delete special Item</button>
            `;

            // add new item to the menuItemsContainer
            var specialItemsContainer = document.getElementById("specialItemsContainer");
            specialItemsContainer.appendChild(newItem);
            button.textContent = "Added!";
        } 
        else {
            console.log('unsucessful promise');
            throw new Error('Failed to update special status');
        }
    })
    // add new item to the menuItemsContainer
    var menuItemsContainer = document.getElementById("menuItemsContainer");
    menuItemsContainer.appendChild(newItem);
    button.textContent = "Added!";
    toastr.success(`${itemName} is added to special!`);

}

function deleteItem(button, url) {
    console.log('deleting the menu');
    var item = button.parentNode;
    var itemID = item.dataset.itemId;
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            item_id: itemID,
        }),
    })
    .then(response => {
        if (response.ok) {
            console.log('sucessful promise');
            item.parentNode.removeChild(item);
            location.reload();
        } else {
            console.log('unsucessful promise');
            console.error('Failed to delete item');
        }
    });
}

// function orderItem(button) {
//     // add your ordering logic here
//     var itemName = button.parentNode.querySelector(".itemName").innerText;
//     var itemPrice = button.parentNode.querySelector(".itemPrice").innerText;

//     toastr.success(`Ordered ${itemName} for ${itemPrice}`, 'Order Placed');
// } 

