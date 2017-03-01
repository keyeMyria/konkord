$('.js-load-more').on('click', function(){
    var $link = $(this);
    $.ajax({
        type: "POST",
        url: $(this).data('url'),
        data: {
            'next_page': $link.data('next-page')
        },
        success: function(data){
            var parsed_data = $.parseJSON(data);
            $('.products-wrap .category-product-item').last().after(parsed_data['products']);
            if (parsed_data['next_page']) {
                $link.data('next-page', parsed_data['next_page']);
            } else {
                $('.pagination').find('.next-page, .last-page').remove();
                $link.hide();
            }
            $('.pagination-bottom li.active').last().next().addClass('active');
        }
    })
});