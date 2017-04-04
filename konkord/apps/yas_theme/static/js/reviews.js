$(function(){
    var $reviews = $('#reviews_with_chains.reviews');
        content_id = $reviews.data('content-id'),
        content_type_id = $reviews.data('content-type-id');

    $('.js-add-review-button').magnificPopup({
        type: "inline",
        midClick: true,
        closeBtnInside: false,
        callbacks: {
            open: function() {


                load_review_form(content_type_id, content_id, 'reviews');

                disableScrollingPage();

                $('body').addClass('opened-reviews-form');
            },
            close: function(){
                enableScrollingPage();

                $('body').removeClass('opened-reviews-form');
            }

        }
    });

    load_reviews_with_chains(content_type_id, content_id, 'reviews', $reviews.data('exclude-variants'));
});

function load_reply_form(review_id, reviews_type,reply_form){
    $.ajax({
        url: CONSTANTS.siteLanguage + "/reviews/add-reply",
        type: "GET",
        dataType: "json",
        data: {
            'review_id': review_id,
            'reviews_type': reviews_type
        },
        success: function(msg){
            $(reply_form).html(msg['html']);

            var id = $(reply_form).find('form').data('review-id'),
            reviewText = $('.js-review-comment-' + id).text();

            $(reply_form).find('.js-add-reply__parent-review-content').text(reviewText);

            checkPrerentReviewWidth();
        }
    });
}

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

            $('.add_reply_link').magnificPopup({
                type: "inline",
                midClick: true,
                closeBtnInside: false,
                callbacks: {
                    open: function(){

                        var event = $.magnificPopup.instance._lastFocusedEl;

                        var review_id = $(event).attr('review_id');
                        var reviews_type = $(event).attr('reviews_type');
                        var reply_form = '#reply_form_' + review_id;

                        load_reply_form(review_id, reviews_type, reply_form );

                        disableScrollingPage();

                        $('body').addClass('opened-reviews-form');
                    },
                    close: function(){
                        enableScrollingPage();

                        $('body').removeClass('opened-reviews-form');
                    }
                }
            });
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
            $('#review_with_chains_form.'+reviews_type).loadOverStart().html(msg['html']).loadOverStop();
            var $reviews = $('#reviews_with_chains.'+reviews_type);
            var content_id = $reviews.data('content-id');
            var content_type_id = $reviews.data('content-type-id');
            var exclude_variants = $reviews.data('exclude-variants');
            if (msg['added'] == true){
                load_reviews_with_chains(content_type_id, content_id, reviews_type, exclude_variants);
                $.magnificPopup.close();
                alertify.notify(msg.message, 'success', 5);
            } else{
                $('#review_with_chains_form.'+reviews_type).html(msg['html']);
                setRatingBeforeValidateForm();

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
            setRatingBeforeValidateForm();
        }
    });
}

function add_reply(reviews_type, review_id){
    var form_id = '#review_with_chains_form_' + review_id;
    var reply_form_block = '#reply_form_' + review_id;
    $.ajax({
        url: CONSTANTS.siteLanguage + "/reviews/add-reply", // TODO change to reverse
        type: "POST",
        dataType: "json",
        data: $(form_id).serialize(),
        success: function(msg){
            var $reviews = $('#reviews_with_chains.'+reviews_type);
            var content_id = $reviews.data('content-id');
            var content_type_id = $reviews.data('content-type-id');
            var exclude_variants = $reviews.data('exclude-variants');
            if (msg['added'] == true){
                load_reviews_with_chains(content_type_id, content_id, reviews_type, exclude_variants);
                $.magnificPopup.close();
                alertify.notify(msg.message, 'success', 5);
            } else {
                $(reply_form_block).html(msg['html']);
            }
        }
    });
}

function chooseRate(){

    $("#reviewed_with_chains_form").on('click','.rate',function(e) {
        e.preventDefault();

        $(this).siblings().removeClass('current-rating');
        $(this).addClass("current-rating")

        $("#reviewed_with_chains_form .rate").each(function(){
            if( $(this).hasClass('current-rating') ){
                return false
            }

            $(this).addClass('current-rating');
        });

        $("#reviewed_with_chains_form #id_score").val($(this).data("score"));
    });
}

function setRatingBeforeValidateForm(){
 
    var score = $("#reviewed_with_chains_form #id_score").val();

    if (score){
        score = parseInt(score);
        $("#reviewed_with_chains_form .rate").each(function(){
            if( parseInt($(this).data('score')) <= score ){
                $(this).addClass('current-rating');
            }

        });
    }
}

function hideParentReview(obj, speadHide){
    $('.js-add-reply__parent-review-content')
    .animate({'height': 100}, speadHide)
    .addClass('with-shadow');
    if( obj ){
        obj.text(obj.data('hidded-text'))
    }
}

function showParentReview(obj,containerHeight){
    $('.js-add-reply__parent-review-content')
    .animate({'height': containerHeight}, 400)
    .removeClass('with-shadow');
    obj.text(obj.data('showed-text'))

}

function checkPrerentReviewWidth(){
    var revirewHeidht = $('.js-add-reply__parent-review-content').height();
    if (revirewHeidht > 100){
        $('.js-add-reply__show-full-review').show();
        bindOpenHideReviewButton(revirewHeidht);
        hideParentReview(false, 0);
    }
}

function bindOpenHideReviewButton(containerHeight){
    $('.js-add-reply__show-full-review').click(function(e){
        e.preventDefault();

        if( $(this).hasClass('opened') ){
            hideParentReview( $(this), 400 );
        }else{
            showParentReview( $(this), containerHeight );
        }
        $(this).toggleClass('opened');
    })
}