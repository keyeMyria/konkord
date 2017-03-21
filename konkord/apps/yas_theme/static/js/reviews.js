function load_reviews_with_chains(content_type_id, content_id, reviews_type, exclude_variants){
    var data = {
        'content_type_id': content_type_id,
        'content_id': content_id,
        'reviews_type': reviews_type,
        'group_by_parent': $('.questions-group-by-parent').data('value'),
        'exclude_variants': exclude_variants
    };
     data['is_short_comment_filter'] = 0;
    $.ajax({
        url: CONSTANTS.siteLanguage + "/reviews/all-reviews-by-type",
        type: "POST",
        dataType: "json",
        data: data,
        success: function(msg){
            $('#reviews_with_chains').html(msg['html']);
            setAverageRating();
            setReviewsAmount();
        }
    });
}
function add_review(reviews_type){
    $.ajax({
        url: CONSTANTS.siteLanguage + "/reviews/add-review",
        type: "POST",
        dataType: "json",
        data: $('#review_with_chains_form.'+reviews_type).serialize(),
        success: function(msg){
            $('#reviewed_with_chains_form.'+reviews_type).loadOverStart().html(msg['html']).loadOverStop();
            var $reviews = $('#reviews_with_chains.'+reviews_type);
            var content_id = $reviews.data('content-id');
            var content_type_id = $reviews.data('content-type-id');
            var exclude_variants = $reviews.data('exclude-variants');
            if (msg['added'] == true){
                load_reviews_with_chains(content_type_id, content_id, reviews_type, exclude_variants);
                $.magnificPopup.close()
            }

        }
    });
}

function load_review_form(content_type_id, content_id, reviews_type){
    $.ajax({
        url: CONSTANTS.siteLanguage + "/reviews/add-review", // TODO change to reverse
        type: "GET",
        dataType: "json",
        data: {
            'content_type_id': content_type_id,
            'content_id': content_id,
            'reviews_type': reviews_type
        },
        success: function(msg){
            $('#reviewed_with_chains_form').html(msg['html']).show();
            chooseRate();
        }
    });
}


$(function(){

    var $reviews = $('#reviews_with_chains.reviews');
        content_id = $reviews.data('content-id'),
        content_type_id = $reviews.data('content-type-id');
        load_reviews_with_chains(content_type_id, content_id, 'reviews', $reviews.data('exclude-variants'));

    $('.rating_yes').click(function(event){
        event.preventDefault();
        var review_id = $(this).attr('review_id');
        span_yes = $(this).find('span');
        span_no = $(this).parent().find('.rating_no').find('span');
        $.ajax({
            url: CONSTANTS.siteLanguage + "{% url 'reviewed_with_chains_rating' %}",
            type: "POST",
            dataType: "json",
            data: {
                'review_id': review_id,
                'rating': 'yes',
            },
            success: function(msg){
                span_yes.html(msg['yes']);
                span_no.html(msg['no']);
            }
        });
    });
    $('.rating_no').click(function(event){
        event.preventDefault();
        var review_id = $(this).attr('review_id');
        span_no = $(this).find('span');
        span_yes = $(this).parent().find('.rating_yes').find('span');
        $.ajax({
            url: CONSTANTS.siteLanguage + "{% url 'reviewed_with_chains_rating' %}",
            type: "POST",
            dataType: "json",
            data: {
                'review_id': review_id,
                'rating': 'no',
            },
            success: function(msg){
                span_yes.html(msg['yes']);
                span_no.html(msg['no']);
            }
        });
    });
});

function chooseRate(){

    $("#reviewed_with_chains_form .rate").click(function(e) {
        e.preventDefault();
        $(this).siblings().removeClass('current-rating');
        $(this).addClass("current-rating")
        $("#reviewed_with_chains_form .rate").each(function(){
            if( $(this).hasClass('current-rating') ){
                return false
            }
            $(this).addClass('current-rating');
        })
        $("#reviewed_with_chains_form #id_score").val($(this).attr("data"));
    });
}