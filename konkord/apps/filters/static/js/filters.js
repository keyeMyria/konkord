$(function() {
    $("#slider-range").slider({
      range: true,
      min: $( "#amount" ).attr('min'),
      max: $( "#amount" ).attr('max'),
      values: [ $( "#amount" ).data('init-min'), $( "#amount" ).data('init-max') ],
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.values[ 0 ] + ".." + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val($("#slider-range").slider( "values", 0 ) +
      ".." + $("#slider-range").slider( "values", 1 ) );
} );
function submitForm(){
    var filters = {};
    $('.filter-checkbox:checked').each(function () {
        if($(this).attr('name') in filters) {
            filters[$(this).attr('name')] += ',' + $(this).val();
        } else {
            filters[$(this).attr('name')] = $(this).val();
        }
    });
    if($('#amount').val()) {
        filters[$('#amount').attr('name')] = $('#amount').val();
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
    window.location.href=url+params;
}