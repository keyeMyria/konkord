// cart and checkout
$(function () {
    // product buy button
    setTotalProductInCart();

    initSpinnerInCart();
    if ( CONSTANTS.pageType =="checkout" || ( CONSTANTS.pageType == "orderdetail" ) )
    calculateTotalCartPrice();

    $('.js-buy-button').click(function(){
        var counter = 0; 
        $('.js-product-amount').each(function(){

            counter += parseInt( $(this).val(), 10 ) ;
        });
        if(counter){
            $('.js-buy-product-form').submit();
        }else{

            $('.js-tabs').easytabs('select', '#main');

            $('#main').animate( {scrollTop: $('#main').innerHeight()},500 );

            var message = $('.js-size-list_error').text().trim();

            addShadowTolistsOfShadow();

            if ( $('.ajs-visible').length) return;

            alertify.notify(message, 'error', 5);

        }
    });

    $('.js-clear-cart').click(function(){
        deleteCartItems(null, true);
    });

   // remove items from cart
    $(document).on('click', '.js-remove-cart-item', function (e) {
        e.preventDefault();
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

    $('#id_voucher').change(function () {
       processVoucher($(this).val());
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
                if(res['status'] == 200) {
                    openModalCart();

                    clearAllSizesOnProduct();
                }
            }
        });
    });
});


function calculateTotalCartPrice() {
    var $items = $('.' + CONSTANTS.pageType + ' .js-items-group'),
    totalPrice = 0;



    $items.each(function(){

        var priceForOne = getPriceForOneInGroup( $(this) ),
            groupItemsAmount = getCartGroupAmount( $(this) ),
            totalGroupPrice = priceForOne * groupItemsAmount;

            setGroupTotalPrice( $(this), totalGroupPrice );

            totalPrice += totalGroupPrice
    });

    totalPrice += getShippingPrice();

    totalPrice += getPaymentPrice();

    totalPrice += getVoucherPrice();

    setCartTotalPrice( totalPrice );

};

function getCartGroupAmount(groupProducts){
    var groupItemsAmount = 0;

    groupProducts.find('.js-cart-item-amount').each(function(){
        if ( CONSTANTS.pageType == 'orderdetail' || CONSTANTS.pageType == 'thankyoupage' ){
            groupItemsAmount += parseInt( $(this).text() );
        }else{
            groupItemsAmount += parseInt( $(this).val() );
        }
    });

    return groupItemsAmount; 
}

function setGroupTotalPrice( groupWrapp, price ){
    groupWrapp.find('.js-group-total-prce').text( price.toFixed(2) );
}

function getPriceForOneInGroup( groupProducts ){
    var price = parseFloat(groupProducts.find('.js-price-for-one').text());

    return price;
}

function setCartTotalPrice( price ){
    $('.js-total-cart-price span').text( price.toFixed(2) );
}

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
            ajaxContentAdded: function() {
                    
                initSpinnerInCart();

                $('.js-cart-item-amount').keyup(function(){
                    updateCartItems($(this));
                });

                calculateTotalCartPrice();

                setTotalProductInCart();

                bindCloseModalCartButton();

                disableScrollingPage();
            },

            close: function(){
                enableScrollingPage();
            }
        }
    });
};

function deleteCartItems($items, clearAll) {
    var ids = [];

    if( clearAll ){
        ids = "ALL";    
    }else{
        for(var i=0; i < $items.length; i++) {
            ids.push( $( $items[i]).data('item-id') );
        }
    }


    $.ajax({
        url: CONSTANTS.siteLanguage + '/checkout/cart/delete-items', // TODO: rewrite to reverse
        type: 'POST',
        data: {'items': JSON.stringify(ids)},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200) {
                if(res['data']['total_in_cart']) {
                    for(var i=0; i < $items.length; i++) {
                        var itemId = $($items[i]).data('item-id');

                        if( $($items[i]).parent().siblings('.js-cart-remove-item-wrapp').length ){
                            $('.for-remove-' + itemId ).remove();
                        }else{
                            $($items[i]).closest('.js-items-group').remove();
                        }

                    }
                    $('.cart-price span').text(res['data']['total_cart_price']);

                    setVoucherPrice( res['data']['total_cart_price'] );

                    calculateTotalCartPrice();

                    setTotalProductInCart();

                } else { // cart empty, close modal cart
                    setTotalProductInCart();
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
        url: CONSTANTS.siteLanguage + '/checkout/cart/update', // TODO: rewrite to reverse
        type: 'POST',
        data: {'update_data': JSON.stringify(update_data)},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200) {
                if(res['data']['total_in_cart']) {
                    for(var i=0; i < $items.length; i++) {
                        var $item = $($items[i]);

                        if(!res['data']['items'][parseInt($item.attr('name'))]){
                            var itemId = $($item).attr('name');

                            if( $($item).closest('.js-cart-number-item').siblings('.js-cart-number-item').length ){
                                $('.for-remove-' + itemId ).remove();
                            }else{
                                $($item).closest('.js-items-group').remove();
                            }

                        } else {
                            $item.val(res['data']['items'][$item.attr('name')]);
                        }
                    }
                    $('.cart-price span').text(res['data']['total_cart_price']);

                    setVoucherPrice( res['data']['total_cart_price'] );

                    calculateTotalCartPrice();

                    setTotalProductInCart();

                } else { // cart empty, close modal cart
                        setTotalProductInCart();
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
        url: CONSTANTS.siteLanguage + '/checkout/shipping-method/cities', // TODO: rewrite to reverse
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
        url: CONSTANTS.siteLanguage + '/checkout/shipping-method/city-offices', // TODO: rewrite to reverse
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
            'price_selector': '.js-payment-price span'
        },
        'shipping': {
            'url': '/checkout/shipping-method/detail',
            'price_selector': '.js-shipping-price span'
        }
    };
    var method_id = id;
    if(!id) {
        $(methodsData[method].price_selector).text(0);
        calculateTotalCartPrice();
        setTotalProductInCart()
    } else {
        $.ajax({
            url: CONSTANTS.siteLanguage + methodsData[method].url, // TODO: rewrite to reverse
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
                    setTotalProductInCart()
                }
            }
        });
    }
};

function initSpinnerInCart(){
    $('.js-cart-number-item:not(.ui-spinner-input)  input').spinner({
        min: 0,
        max: 500,
        change: function( event, ui ) {
            $(this).spinner('value', parseInt($(this).spinner('value'), 10) || 0);
            updateCartItems($(this));
        },
        stop: function( event, ui ) {
            if( parseInt( $(this).val(), 10) ){
                removeShadowFromListOfSizes();
                updateCartItems($(this));
            }
        }
    
    });
}

function setTotalProductInCart(){
    $.post( CONSTANTS.siteLanguage + '/checkout/cart/detail/json', function(obj){
        var $cart = $('.js-cart');
        if (obj.status == 200){
            var totalInCart = obj.data.total_in_cart;
            if (!totalInCart) {
                totalInCart = 0;
                disabledLinkToCart( $cart );
            }else{
                enabledLinkTocart( $cart );
            }
            $cart.find('span').text( totalInCart );

        }else{

            disabledLinkToCart( $cart );
        }
    });
}

function enabledLinkTocart( obj ){
    $(obj).closest('a').removeClass('pointer-events-none');
    $('.js-clear-cart').show();
}

function disabledLinkToCart( obj ){
    $(obj).closest('a').addClass('pointer-events-none');    
    $('.js-clear-cart').hide();
}


function bindCloseModalCartButton(){   
    $('.js-continue-shopping').click(function(e){
        e.preventDefault();

        $.magnificPopup.close();
    });
}

var processVoucher = function (voucherNumber) {
    $.ajax({
        url: CONSTANTS.siteLanguage + '/checkout/voucher/json',
        method: 'POST',
        data: {'voucher': voucherNumber},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200){

                var $voucher = $('#id_voucher');
                var $helpBlock = $voucher.closest('.form-group').find('.help-block');
                if(!$helpBlock.length) {
                  $voucher.after($('<span class="help-block"><div class="help-block">' + res['data']['message'] + '</div></span>'));
                } else {
                  $helpBlock.find('.help-block').text(res['data']['message']);
                }
                if(res['data']['voucher_effective']) {
                  $voucher.closest('.form-group').removeClass('has-error').addClass('has-success');

                  $('.js-voucher-discount .js-voucher-price').text('-' + res['data']['discount']);
                  $('.js-voucher-discount .js-voucher-name').text(res['data']['voucher_name']);

                  $('.js-voucher-discount').data('voucher-type', res['data']['voucher_type']);
                  $('.js-voucher-discount').data('voucher-value', res['data']['voucher_value']);
                } else {
                  if(!res['data']['voucher_number']){
                      $helpBlock.remove();
                      $voucher.closest('.form-group').removeClass('has-success').removeClass('has-error');
                  } else {
                    $voucher.closest('.form-group').removeClass('has-success').addClass('has-error');
                  }
                  $('.js-voucher-discount .js-voucher-price').text(0);
                  $('.js-voucher-discount .js-voucher-name').text($('.js-voucher-discount .js-voucher-name').data('voucher-alternate-text'));
                }

                calculateTotalCartPrice();
            }
        }
    });
}

function getShippingPrice(){
    var shippingPrice = parseFloat($('.js-shipping-price span').text());
    if ( isNaN(shippingPrice) ) {
        shippingPrice = 0;
    }

    return shippingPrice;
}

function getPaymentPrice(){
    var paymentPrice = parseFloat($('.js-payment-price span').text());
    if ( isNaN(paymentPrice) ) {
        paymentPrice = 0;
    }

    return paymentPrice;
}

function getVoucherPrice(){
    var voucherPrice = parseFloat($('.js-voucher-discount .js-voucher-price').text());
    if ( isNaN(voucherPrice) ) {
        voucherPrice = 0;
    }

    return voucherPrice;
}

function setVoucherPrice(price){
    var $voucherWrapp = $('.js-voucher-discount'),
        voucherType = $voucherWrapp.data('voucher-type'),
        voucherValue = parseFloat($voucherWrapp.data('voucher-value')),
        voucherPrice;

    if ( voucherType == "percentage" ){
        voucherPrice = parseFloat(price) * voucherValue / 100;

        $voucherWrapp.find('.js-voucher-price').text( -voucherPrice );
    }

}
