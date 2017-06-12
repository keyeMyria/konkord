var oldUrl = generateUrl(getParams());
$(function() {
    var $slider = $("#slider-range"),
        $amount = $(".js-amount"),
        $blockMin = $('.js-min-price-readonly .js'),
        $blockMax = $('.js-max-price-readonly .js'),
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
        $blockMin.text(ui.values[ 0 ]);
        $blockMax.text(ui.values[ 1 ]);
      },
      change: function( event, ui ) {
        if($amount.val()) {
            var amountMaxMin = parseInt( $amount.data('init-min') ) + ".." + parseInt( $amount.data('init-max') ),
                $applyButton = $(this).closest('fieldset').find('.js-apply-filter');

            if( amountMaxMin != $amount.val() ){
                $('.js-apply-filter').hide();
                $applyButton.show();
            }else{
                $applyButton.hide();
            }
        }
      }
    });
    $amount.val( $slider.slider( "values", 0 ) + ".." + $slider.slider( "values", 1 ));
    $blockMin.text($slider.slider( "values", 0 ));
    $blockMax.text($slider.slider( "values", 1 ))

} );

function submitForm(){
    var $amount = $('.js-amount'),
        filters = {};

    if($amount.val()) {
        var amountMaxMin = parseInt( $amount.data('min') ) + ".." + parseInt( $amount.data('max') );

        if( amountMaxMin != $amount.val() ){
            filters[$amount.attr('name')] = $amount.val();
        }

    }
    var url = $('#filters').data('request-url');
    var params = generateUrl(getParams(filters));
    if ( window.location.search != (params) ){
        window.location.href=url+params;
    }
}
$('.js-filter-options-wrapper.apply-by-clicking .js-filter-checkbox').change(function(){
    submitForm();
});

$('.js-filter-options-wrapper:not(.apply-by-clicking) .js-filter-checkbox').change(function(){
    $('.js-apply-filter').hide();
    $('.js-last-changed').removeClass('js-last-changed');
    $(this).addClass('js-last-changed');
    var newUrl = generateUrl(getParams()),
        $self = $(this),
        $amount = $(".js-amount"),
        amountMaxMin = parseInt( $amount.data('init-min') ) + ".." + parseInt( $amount.data('init-max') ),
        $fieldset = $(this).closest('fieldset'),
        $applyButton = $fieldset.find('.js-apply-filter');
        
    if(newUrl != oldUrl){

        if( amountMaxMin != $amount.val() ){
            $('.js-apply-filter').hide();
            $applyButton.show();
        }else{
            $applyButton.hide();
        }

        applyButtonSetPosition($self, $fieldset, $applyButton);

    }else if( amountMaxMin != $amount.val() ){
        $('.js-apply-filter').hide();
        $amount.closest('.js-filter-options-wrapper').find('.js-apply-filter').show()
    }else{
        $applyButton.hide();
        $('.js-last-changed').removeClass('js-last-changed');
    }

});

function generateUrl(obj){
    var params = ""
    Object.keys(obj).forEach(function(key) {
        var value = obj[key];
        if(params){
            params += '&'
        }
        else {
            params += '?'
        }
        params += key + '=' + value;
    });
    return params;
}

function getParams(obj){
    if (!obj) {
        var obj = {};
    }
    $('.js-filter-checkbox:checked').each(function () {
        if($(this).attr('name') in obj) {
            obj[$(this).attr('name')] += ',' + $(this).val();
        } else {
            obj[$(this).attr('name')] = $(this).val();
        }
    });
    return obj;
}

function getButtonPosition($checkbox, $fieldset , $applyButton){
    var $label = $checkbox.next(),
    buttonTop = 0,
    labelHeight = $label.outerHeight(true),
    applyButtonHeight = $applyButton.height();

    if ( labelHeight < applyButtonHeight ) {
        buttonTop -= labelHeight / 2;            
    }else if( labelHeight > applyButtonHeight ){
        buttonTop += (  labelHeight - applyButtonHeight ) / 2;
    }

    buttonTop += $label.offset().top - $fieldset.offset().top;

    return buttonTop;
}
function applyButtonSetPosition($checkbox){
        var $fieldset = $checkbox.closest('fieldset'),
        $applyButton = $fieldset.find('.js-apply-filter');
        $applyButton.show().animate({top: getButtonPosition($checkbox, $fieldset, $applyButton)});

};