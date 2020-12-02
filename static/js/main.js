console.log("hellooo")


// var updatequantity = document.getElementsByClassName('change_quantity');

// for(var j = 0; j < updatequantity.length; j++){
//     updatequantity[j].addEventListener('click', function(){
//         var productId = this.dataset.product;
//         var action = this.dataset.action;
//         console.log('product: ', productId ,'action', action);

//         console.log("User: ", user)
//         if( user == 'AnonymousUser'){
//             console.log('not authenticated')
//         }else{
//             console.log(' authenticated')
//             updateUserOrder(productId, action)
//         }
//     }) 
// }




items = []

$.ajax({
    method : 'GET',
    url : '/cartListAPI/',
    success:function(response){
        items = response
        console.log(items)
        for(var i in items){
            addbtns(items[i])
        }
    }
})


function addbtns(obj){
   
    var row = `
    <tr class="ahmed">
                        
        <td>
            <div class="product-cart">

                <img class="cart-img" src="${obj.image}" alt="">
                
                <div class="detiles">
                    <a style="color: #212529" href="/product/${obj.id}/">
                        <h6 class='product-label' ><strong>${obj.name}</strong></h6>
                    </a>
                    <p class="product-des" >${obj.descreption}</p>
                    <button class="btn btn-sm btn btn-outline-danger" data-product=${obj.id} id="remove${obj.id}">Remove</button>
                    <button class="btn btn-sm btn btn-warning hidden" data-product=${obj.id} id="cancel${obj.id}">Cancel</button>
                    <button class="btn btn-sm btn btn-danger hidden" data-product=${obj.itemId} id="confirm${obj.id}">Confirm</button>
                </div>
                

            </div>
        </td>
        <td style="font-weight: 600;">${obj.price}L.E</td>
        <td> 
            <div class="quantity_display">  
                <button data-product=${obj.id} data-action="remove" id="minus${obj.id}"
                 class="change_quantity down" style="outline: none;">                              
                    <img src="/images/images/icons/remove.png" alt="">
                </button>
                <spam data-product=${obj.itemId} id="qty${obj.id}">${obj.quantity}</spam>
                <button data-product=${obj.id} data-action="add"  id="plus${obj.id}"
                 class="change_quantity up" style="outline: none;">
                    <img src="/images/images/icons/plus.png" alt="">
                </button>
            </div> 
        </td>

    </tr>`

    $('.cart-table').append(row)
    
    $(`#plus${obj.id}`).on('click', updatequantity)
    $(`#minus${obj.id}`).on('click', updatequantity)

    $(`#remove${obj.id}`).on('click', removeItem)
    $(`#cancel${obj.id}`).on('click', canseldeletion)
    $(`#confirm${obj.id}`).on('click', deleteItem)

    $(`#qty${obj.id}`).on('click', editqty)
    
}

function PostData(url, data){
    myurl = url
    fetch(myurl , {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken,
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body : JSON.stringify(data)
    })

    .then(function (response) {
        console.log(response.url);
        return response.json(); // But parse it as JSON this time
    })
        
    .then(data => {
        console.log('data',data);
        location.reload() // JSON data parsed by `data.json()` call
    });
}

function editqty(){
    var itemId = $(this).data('product')
    var qty = $(this).html()
    console.log(itemId)
    $(this).unbind()
    $(this).html(`<input class="qty form-control" data-product=${itemId} type="text" id="value${itemId}" value="${qty}">`)
 
    $(this).on('keydown', function(e){
        console.log("work", e)
        var itemId = $(this).data('product')
        var value = $(`#value${itemId}`).val()
        if (e.keyCode === 13 & value > 0) {  //checks whether the pressed key is "Enter"
        
            
            var data = {'id': itemId, 'value': value}
            console.log(data)
            var url = '/edit_quantity/'
            PostData(url, data)
            $(this).bind('click', editqtys)
        }

    })
}

function removeItem(){
    var itemId = $(this).data('product');
    $(`#remove${itemId}`).addClass("hidden")
    
    $(`#cancel${itemId}`).removeClass("hidden")
    $(`#confirm${itemId}`).removeClass("hidden")
}

function canseldeletion(){
    var itemId = $(this).data('product');
    $(`#remove${itemId}`).removeClass("hidden")
    
    $(`#cancel${itemId}`).addClass("hidden")
    $(`#confirm${itemId}`).addClass("hidden")
}



function deleteItem(){
    var itemId = $(this).data('product');
    console.log(itemId)
    var url = "/delete_item/"
    var data = {'id': itemId}
    PostData(url, data)
    
    
}

function updatequantity(){
    var productId = $(this).data('product');
    var action = this.dataset.action;
    var qty = 1;
    console.log('product: ', productId ,'action', action);

    console.log("User: ", user)
    if( user == 'AnonymousUser'){
        console.log('not authenticated')
    }else{
        var data = {'productId': productId, 'action': action, 'qty': qty,}
        var url = '/update_item/'
        PostData(url,data)
    }
}


$('.update-cart').on('click', updateUserOrder)

function updateUserOrder(){
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var qty = 1;
    console.log('product: ', productId ,'action', action);

    console.log("User: ", user)
    if( user == 'AnonymousUser'){
        console.log('not authenticated')
    }else{
        console.log('loggedin sending data..')
        var url = '/update_item/'
        var data = {'productId': productId, 'action': action, 'qty': qty,}
        // const data = { username: 'example' };
        PostData(url,data)
    }
}

$(`#add-qty`).on('click', addProductQty)
$(`#remove-qty`).on('click', subProductQty)
$(`#qty-val`).on('click', editProductVal)

function addProductQty(){
    console.log("working")
    var value = $(`#qty-val`).html();
    console.log(value);
    value ++
    $(`#qty-val`).html(value)
    
}
function subProductQty(){
    console.log("working")
    var value = $(`#qty-val`).html();
    console.log(value);
    if(value > 1){
        value --
        $(`#qty-val`).html(value)
    }
}

function editProductVal(){
    var qty = $(`#qty-val`).html();
    $(this).unbind()
    $(this).html(`<input class="qty form-control" type="text" 
    id="input-value" value="${qty}">`)
 
    $(this).on('keydown', function(e){
        console.log("work", e)
        var inputValue = $(`#input-value`).val()
        if (e.keyCode === 13 & inputValue > 0) {  //checks whether the pressed key is "Enter"
        
            var inputValue = $(`#input-value`).val()

            console.log(inputValue)
            $(this).html(inputValue)
            $(this).bind('click', editProductVal)
        }

    })
}

$('#add-to-cart').on('click', addToCart)

function addToCart(){
    var productId = $(this).data('product');
    var action = $(this).data('action');
    var qty = parseInt($(`#qty-val`).html());
    var data = {'productId': productId, 'action': action, 'qty': qty,}
    console.log(data)
    var url = '/update_item/'
    PostData(url, data)
}