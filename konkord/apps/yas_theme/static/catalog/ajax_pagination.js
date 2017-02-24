$('.js-load-more').on('click', function(){
    var $link = $(this);
    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: {
            'page': $(this).data('next-page')
        },
        success: function(data){
            parsed_data = $.parseJSON(data)
            $('.products-wrap').append(parsed_data['products']).append($link);
            if (parsed_data['next_page']) {
                $link.data('next-page', parsed_data['next_page'])
                $('.pagination-bottom li.active').last().next().addClass('active')
            } else {
                $link.hide()
            }
        },
    })
})