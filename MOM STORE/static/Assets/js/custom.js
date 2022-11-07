var about_edit = document.getElementById('edit');
var total_order = document.getElementById('total_order');


var order_grids = document.querySelectorAll('.order-grid');
var about_quantity = document.querySelectorAll('.quantity');
var item_price = document.querySelectorAll('.item-price');
var about_total = document.querySelectorAll('.total');
var del_Btn = document.querySelectorAll('.delete-button')




del_Btn.forEach(function(item) {
    // iterate and add the event handler to it
    item.addEventListener("click", function(e) {
        e.target.parentNode.parentNode.remove();

        calculateTotal();

    });

})
about_quantity.forEach(about_quantitys => {

    about_quantitys.addEventListener('change', calculateTotal);


});



function calculateTotal() {
    // I called them again so that is they are deleted in the front end, they current number get updated
    var order_grids = document.querySelectorAll('.order-grid');
    var about_quantity = document.querySelectorAll('.quantity');
    var about_total = document.querySelectorAll('.total');

    var i = 0;
    // This calculates each order total * quantity
    for (var i = 0; i < order_grids.length; i++) {
        console.log(order_grids.length)
        quantity = about_quantity[i].value;
        price = item_price[i].textContent;

        total = quantity * price;

        about_total[i].textContent = total;


        // console.log(total)
    }

    total = 0;

    // This adds all the orders totals
    for (var i = 0; i < order_grids.length; i++) {

        total += Number(about_total[i].textContent);

    }

    total_order.textContent = total;

}