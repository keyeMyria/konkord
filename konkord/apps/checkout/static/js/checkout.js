var calculateTotalCartPrice = function () {
    var totalPrice = 0;
    totalPrice += parseFloat($('.cart-price').text());
    totalPrice += parseFloat($('.js-payment-price').text());
    $('.total-cart-price').text(totalPrice);
};

var openModalCart = function () {
    $.magnificPopup.open({
        type: 'ajax',
        items: {
            src: '/checkout/cart/detail' // TODO: rewrite to reverse
        },
        ajax: {
          settings: {
            type: 'GET'
          }
        }
    })
};

var processPaymentMethod = function (id) {
    if(!id) {
        $('.js-payment-price').text(0);
        calculateTotalCartPrice();
    } else {
        $.ajax({
            url: '/checkout/payment-method/detail', // TODO: rewrite to reverse
            type: 'POST',
            data: {'method': id},
            dataType: 'json',
            success: function (res) {
                if(res['status'] == 200) {
                    $('.js-payment-price').text(res['data']['price']);
                    calculateTotalCartPrice();
                }
            }
        });
    }
};

var deleteCartItems = function ($items) {
    var ids = [];
    for(var i=0; i < $items.length; i++) {
        ids.push($($items[i]).val());
    }
    $.ajax({
       url: '/checkout/cart/delete-items', // TODO: rewrite to reverse
       type: 'POST',
       data: {'items': JSON.stringify(ids)},
       dataType: 'json',
       success: function (res) {
           if(res['status'] == 200) {
               if(res['data']['total_in_cart']) {
                   for(var i=0; i < $items.length; i++) {
                       $($items[i].closest('.cart-item')).remove();
                   }
                   $('.cart-price').text(res['data']['total_cart_price']);
                   calculateTotalCartPrice();
               } else { // cart empty, close modal cart
                   if($('.checkout-form').length){
                       window.location.href = '/';
                   } else {
                       $.magnificPopup.close();
                   }
               }
           }
       }
    });
};

var updateCartItems = function ($items) {
    var update_data = [];
    for(var i=0; i < $items.length; i++) {
        var $item = $($items[i]);
        update_data.push([$item.attr('name'), $item.val()]);
    }
    $.ajax({
       url: '/checkout/cart/update', // TODO: rewrite to reverse
       type: 'POST',
       data: {'update_data': JSON.stringify(update_data)},
       dataType: 'json',
       success: function (res) {
           if(res['status'] == 200) {
               if(res['data']['total_in_cart']) {
                   for(var i=0; i < $items.length; i++) {
                       var $item = $($items[i]);
                       if(!res['data']['items'][parseInt($item.attr('name'))]){
                            $item.closest('.cart-item').remove();
                       } else {
                           $item.val(res['data']['items'][$item.attr('name')]);
                       }
                   }
                   $('.cart-price').text(res['data']['total_cart_price']);
                   calculateTotalCartPrice();
               } else { // cart empty, close modal cart
                   if($('.checkout-form').length){
                       window.location.href = '/';
                   } else {
                       $.magnificPopup.close();
                   }
               }
           }
       }
    });
};

var deleteCart = function () { // TODO use this to delete user cart
    $.ajax({
       url: '/checkout/cart/delete', // TODO: rewrite to reverse
       type: 'POST',
       success: function (res) {
           if(res['status'] == 200) {
               if($('.checkout-form').length){
                   window.location.href = '/';
               } else {
                   $.magnificPopup.close();
               }
           }
       }
    });
};

$(function () {
    // product buy button
   $('#buy-product-form').submit(function (e) {
       e.preventDefault();
       var data = {'products': []};
       var $products = $(this).find('.product-amount');
       for(var i=0; i<$products.length; i++){
           var product = $products[i];
           if($(product).val()) {
               data['products'].push([$(product).attr('name'), $(product).val()]);
           }
       }
       data['products'] = JSON.stringify(data['products']);
       $.ajax({
           url: $(this).attr('action'), // TODO: rewrite to reverse if possible
           type: 'POST',
           data: data,
           dataType: 'json',
           success: function (res) {
               console.log(res);
               if(res['status'] == 200) {
                   openModalCart();
               }
           }
       });
   });

   // remove items from cart
    $(document).on('click', '.remove-cart-item', function () {
        deleteCartItems($(this));
    });
    $('#id_payment_method').change(function () {
        processPaymentMethod($(this).val())
    })
});
