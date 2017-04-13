$('.js-load-more').on('click', function(){
    var link = $(this);
    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: {
            'next_page': $(this).data('next-page')
        },
        success: function(data){
            var parsed_data = $.parseJSON(data);
            link.before(parsed_data['products']);
            if (parsed_data['next_page']) {
                link.data('next-page', parsed_data['next_page'])
            } else {
                link.hide()
            }
        },
    })
})