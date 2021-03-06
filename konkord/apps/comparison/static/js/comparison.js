var highlightComparisonProducts = function () {
    $.ajax({
        url: '/comparison/products',
        type: 'POST',
        success: function (res) {
            if(res['status'] == 200) {
                if(res['data']['comparison'].length) {
                    $('.js-comparison-link').show();
                    for(var i=0; i<res['data']['comparison'].length; i++) {
                        $('.js-comparison-icon-' + res['data']['comparison'][i]).addClass('js-in-comparison').unbind();
                    }
                }
            }
        }
    })
};

var addComparisonProduct = function (product) {
    $.ajax({
        url: '/comparison/add',
        type: 'POST',
        data: {product: product},
        success: function (res) {
            if(res['status'] == 200) {
                 $('.js-comparison-icon-' + product).addClass('js-in-comparison').unbind();
            }
        }
    })
};



var removeComparisonProducts = function (products, clear) {
    var data = {
        products: products,
        clear: clear
    };
    $.ajax({
        url: '/comparison/remove',
        type: 'POST',
        data: {data: JSON.stringify(data)},
        dataType: 'json',
        success: function (res) {
            if(res['status'] == 200) {
                if(!res['data']['comparison'].length) {
                    window.location.href = '/'
                } else {
                    for(var i=0; i<products.length; i++) {
                        $('.js-comparison-' + products[i]).remove();
                    }
                }
            }
        }
    });

};

$(function () {
    highlightComparisonProducts();
    $('.js-comparison-add-product').click(function (e) {
        e.preventDefault();
        addComparisonProduct($(this).data('product-id'));
    });
    $('.js-comparison-remove-product').click(function (e) {
        e.preventDefault();
        removeComparisonProducts([$(this).data('comparison-id')], false);
    });
    $('.js-clear-comparison').click(function (e) {
        e.preventDefault();
        removeComparisonProducts([], true);
    })
});