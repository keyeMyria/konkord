$(function() {
    var $slider = $("#slider-range"),
        $amount = $(".js-amount"),
        min = parseInt($amount.data('min')),
        max = parseInt($amount.data('max')),
        values = [ parseInt($amount.data('init-min')), parseInt($amount.data('init-max'))];
        curency = $(".js-amount").data('curency');

    $slider.slider({
      range: true,
      min: min,
      max: max,
      // step: 0.01,
      values: values,
      slide: function( event, ui ) {
        $amount.val( ui.values[ 0 ] + ".." + ui.values[ 1 ] );
      },
      change: function( event, ui ) {
        if($amount.val()) {
            var amountMaxMin = parseInt( $amount.data('init-min') ) + ".." + parseInt( $amount.data('init-max') );

            if( amountMaxMin != $amount.val() ){
                $('.js-apply-filter').show();
            }else{
                $('.js-apply-filter').hide();
            }
        }
      }
    });
    $amount.val( $slider.slider( "values", 0 ) + ".." + $slider.slider( "values", 1 ));
} );

function submitForm(){
    var filters = {},
        $amount = $('.js-amount');
    $('.filter-checkbox:checked').each(function () {
        if($(this).attr('name') in filters) {
            filters[$(this).attr('name')] += ',' + $(this).val();
        } else {
            filters[$(this).attr('name')] = $(this).val();
        }
    });
    if($amount.val()) {
        var amountMaxMin = parseInt( $amount.data('init-min') ) + ".." + parseInt( $amount.data('init-max') );

        if( amountMaxMin != $amount.val() ){
            filters[$amount.attr('name')] = $amount.val();
        }

    }
    var url = $('#filters').data('request-url');
    var params = '';
    Object.keys(filters).forEach(function(key) {
        var value = filters[key];
        if(params){
            params += '&'
        }
        else {
            params += '?'
        }
        params += key + '=' + value;
    });

    if ( window.location.search != (params) ){
        window.location.href=url+params;
    }
}

$('.filter-checkbox').change(function(){
    submitForm();
});