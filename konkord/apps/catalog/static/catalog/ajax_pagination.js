$('.js-load-more').on('click', function(){
    var link = $(this);
    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: {
            'page': $(this).data('next-page')
        },
        success: function(data){
            parsed_data = $.parseJSON(data)
            link.before(parsed_data['products'])
            if (parsed_data['pagination']['has_next']) {
                link.data('next-page', parsed_data['pagination']['next'])
            } else {
                link.hide()
            }
        },
    })
})