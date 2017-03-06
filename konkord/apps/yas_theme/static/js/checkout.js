// cart and checkout
$(function () {
    // product buy button
    $('.js-buy-button').click(function(){
        var counter = 0; 
        $('.js-product-amount').each(function(){

            counter += parseInt( $(this).val(), 10 ) ;
        });
        if(counter){
            $('.js-buy-product-form').submit();
        }else{
            $('.js-tabs').easytabs('select', '#main');
            $('.js-size-list_error').slideDown();            
        }


    })

   // remove items from cart
    $(document).on('click', '.remove-cart-item', function () {
        deleteCartItems($(this));
    });

    $('#id_payment_method').change(function () {
        processMethod($(this).val(), 'payment');
    });

    $('#id_shipping_method').change(function () {
        processMethod($(this).val(), 'shipping');
    });

    $(document).on('change', '#id_city', function () {
        getMethodCityOffices($('#id_shipping_method').val(), $(this).val());
    });

    $('.js-buy-product-form').submit(function (e) {
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
});


function calculateTotalCartPrice() {
    var totalPrice = 0;
    totalPrice += parseFloat($('.cart-price').text());
    totalPrice += parseFloat($('.js-payment-price').text());
     //       {# for DENIS DEM4ENKO #}
     //   {# ask DENIS BORYAK about shipping price #}
    totalPrice += parseFloat($('.js-shipping-price').text());
    $('.total-cart-price').text(totalPrice);
};

function openModalCart() {
    $.magnificPopup.open({
        type: 'ajax',
        items: {
            src: '/checkout/cart/detail' // TODO: rewrite to reverse
        },
        ajax: {
          settings: {
            type: 'GET'
          }
        },
        callbacks: {
            open: function() {
                console.log($(this));
            },
            ajaxContentAdded: function() {
                initSpinner( $('.js-cart-item-amount') );
            }
        }
    })
};

function deleteCartItems($items) {
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

function updateCartItems($items) {
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


// shipping and payment

function getMethodCities(method_id) {
    $.ajax({
        url: '/checkout/shipping-method/cities', // TODO: rewrite to reverse
        type: 'POST',
        data: {'method': method_id},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200) {
                var cities = res['data']['cities'];
                var $select = $('#id_city');
                if(!$select.length) {
                    $select = $('<select id="id_city" name="city"><select/>');
                    $('#id_shipping_method').closest('.form-group').after($select);
                }
                $select.find('option').remove();
                for (var i=0;i<cities.length;i++){
                    $select.append($('<option value="' + cities[i].id +'">' +cities[i].name+ '</option>'));
                }
                $('#id_office').remove();
            }
        }
    });
};
function getMethodCityOffices(method_id, city_id) {
    $.ajax({
        url: '/checkout/shipping-method/city-offices', // TODO: rewrite to reverse
        type: 'POST',
        data: {'method': method_id, 'city': city_id},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200) {
                var offices = res['data']['offices'];
                var $select = $('#id_office');
                if(!$select.length) {
                    $select = $('<select id="id_office" name="office"><select/>');
                    $('#id_city').after($select);
                }
                $select.find('option').remove();
                for (var i=0;i<offices.length;i++){
                    $select.append($('<option value="' + offices[i].id +'">' +offices[i].address+ '</option>'));
                }
            }
        }
    });
};

function processMethod(id, method) {
    var methodsData = {
        'payment': {
            'url': '/checkout/payment-method/detail',
            'price_selector': '.js-payment-price'
        },
        'shipping': {
            'url': '/checkout/shipping-method/detail',
            'price_selector': '.js-shipping-price'
        }
    };
    var method_id = id;
    if(!id) {
        $(methodsData[method].price_selector).text(0);
        calculateTotalCartPrice();
    } else {
        $.ajax({
            url: methodsData[method].url, // TODO: rewrite to reverse
            type: 'POST',
            data: {'method': id},
            dataType: 'json',
            success: function (res) {
                if(res['status'] == 200) {
                    $(methodsData[method].price_selector).text(res['data']['price']);
                    if(method == 'shipping') {
                        getMethodCities(method_id);
                    }
                    calculateTotalCartPrice();
                }
            }
        });
    }
};
