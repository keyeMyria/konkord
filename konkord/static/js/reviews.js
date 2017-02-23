function load_reviews_with_chains(content_type_id, content_id, reviews_type, exclude_variants){
    var data = {
        'content_type_id': content_type_id,
        'content_id': content_id,
        'reviews_type': reviews_type,
        'group_by_parent': $('.questions-group-by-parent').data('value'),
        'exclude_variants': exclude_variants
    };
    if(reviews_type == 'short_comment')
        data['is_short_comment_filter'] = 1;
    else
        data['is_short_comment_filter'] = 0;
    $.ajax({
        url: "/reviews/all-reviews-by-type",
        type: "POST",
        dataType: "json",
        data: data,
        success: function(msg){
            $('#reviews_with_chains.'+reviews_type).loadOverStart().html(msg['html']).loadOverStop();
        }
    });
}
function add_review(reviews_type){
    $.ajax({
        url: "/reviews/add-review",
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
            }
        }
    });
}
function add_reply(reviews_type, review_id){
    var form_id = '#review_with_chains_form_' + review_id;
    var reply_form_block = '#reply_form_' + review_id;
    $.ajax({
        url: "/reviews/add-reply", // TODO change to reverse
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
            } else {
                $(reply_form_block).loadOverStart().html(msg['html']).loadOverStop();
            }
        }
    });
}
function load_review_form(content_type_id, content_id, reviews_type){
    $.ajax({
        url: "/reviews/add-review", // TODO change to reverse
        type: "GET",
        dataType: "json",
        data: {
            'content_type_id': content_type_id,
            'content_id': content_id,
            'reviews_type': reviews_type
        },
        success: function(msg){
            $('#reviewed_with_chains_form.' + reviews_type).loadOverStart().html(msg['html']).loadOverStop();
        }
    });
}

$(function(){
    var urlReadyHash = window.location.hash.replace('#review=', '');
    if(urlReadyHash.length){
        waitForSetsOfProducts(50,function(){
            if($('.variant-reviews').length){

               $('.variant-reviews')[0].scrollIntoView();
            }else{
                $('.model-reviews')[0].scrollIntoView();
            }

        });
    }
    var $reviews = $('ul.js-all-reviews li');
    if($reviews.length && $('#short-comment-filter').data('filter'))
        $('a[href="#product-questions"] span:last-child').text('($reviews.length)');
});




function waitForSetsOfProducts(ms, callback){
    while(! $('body.product .set-item').length ){
        setTimeout(function(){

            waitForSetsOfProducts(ms, callback);
        }, ms);
        return;
    }
    callback();
}
var focusOnReview = function(reviewId) {
    var $focusReview = $('.js-all-reviews li#review-' + reviewId);
    if ($focusReview.closest('#product-questions').length) {
        $('[href="#product-questions"]').click();
        if ($focusReview.length) {
            $('#product-questions').find('.js-all-reviews > li').hide();
            $('#product-questions .show-more-reviews').hide();
            $('#product-questions .show-all-reviews').hide();
            $('#product-questions .js-all-reviews li#review-' + reviewId).removeAttr('style');
            $('#product-questions .js-all-reviews li#review-' + reviewId).after('<span class="show-all-reviews dashed-bottom">Показать все вопросы</span>');
            $('#product-questions .show-all-reviews').click(function () {
                $(this).addClass('js-review-ajax-load').text("");
                setTimeout(function () {
                    $('#product-questions .js-review-ajax-load').remove();
                    $('#product-questions #reviews_with_chains ul.js-all-reviews > li').removeAttr('style');
                    $('#product-questions .show-all-reviews').remove();
                }, 500);
            });
        }
    } else {
        $('.review-count').click();
        if ($focusReview.length) {
            $('#product-reviews .js-all-reviews > li').hide();
            $('#product-reviews .show-more-reviews').hide();
            $('#product-reviews .show-all-reviews').hide();
            $('#product-reviews .js-all-reviews li#review-' + reviewId).removeAttr('style');
            $('#product-reviews .js-all-reviews li#review-' + reviewId).after('<span class="show-all-reviews dashed-bottom">Показать все отзывы</span>');
            $('#product-reviews .show-all-reviews').click(function () {
                $(this).addClass('js-review-ajax-load').text("");
                setTimeout(function () {
                    $('#product-reviews .js-review-ajax-load').remove();
                    $('#product-reviews #reviews_with_chains ul.js-all-reviews > li').removeAttr('style');
                    $('#product-reviews .show-all-reviews').remove();
                }, 500);
            });
        }
    }
};



$(function(){
    $('.open-reviews.short_comment').click(function(){
        $('#reviewed_with_chains_form.short_comment').slideToggle('slow');
    });
    $('.open-reviews.reviews').click(function(){
        $('#reviewed_with_chains_form.reviews').slideToggle('slow');
    });
    var $comments = $('#reviews_with_chains.short_comment');
    var $reviews = $('#reviews_with_chains.reviews');
    var content_id = $reviews.data('content-id');
    var content_type_id = $reviews.data('content-type-id');
    load_reviews_with_chains(content_type_id, content_id, 'short_comment', $comments.data('exclude-variants'));
    load_reviews_with_chains(content_type_id, content_id, 'reviews', $reviews.data('exclude-variants'));
    load_review_form(content_type_id, content_id, 'short_comment');
    load_review_form(content_type_id, content_id, 'reviews');

    $('.focus-on-review').unbind().click(function(){
        focusOnReview($(this).data('reviewId'));
        $('#reviews_with_chains')[0].scrollIntoView();
    });

    $('#reviews_with_chains ul.js-all-reviews > li[style] + .show-more-reviews').hide();
    $('#reviews_with_chains ul.js-all-reviews > li').last().next().remove();
    $('.show-more-reviews').click(function(){
        $(this).unbind();
        $(this).addClass('js-review-ajax-load').text("");
        setTimeout(function(){
            $('.js-review-ajax-load').remove();
            $($('#reviews_with_chains ul.js-all-reviews > li[style]')[0]).removeAttr('style');
            $($('#reviews_with_chains ul.js-all-reviews > li[style]')[0]).removeAttr('style');
            $('#reviews_with_chains ul.js-all-reviews > li + .show-more-reviews:visible ').hide();
            $('#reviews_with_chains ul.js-all-reviews > li[style] + .show-more-reviews:hidden ').first().show();
        },500);
    });

    $('.show-all-reviews').click(function(){
        $(this).addClass('js-review-ajax-load').text("");
        setTimeout(function(){
            $('.js-review-ajax-load').remove();
            $('#reviews_with_chains ul.js-all-reviews > li').removeAttr('style');
        },500);
    });
    $('.js-review-comment').each( function() {
        var commentsHeight = $( this ).height();
    });
    if( $( '.js-review-advantage' ).length ){
        $( '.js-review-advantage' ).each( function() {
            var advantageHeight = $( this ).height();
            if( advantageHeight > 60 ){
                $( this ).addClass('short').after('<div class="clearfix"><a class="js-more-info pull-left dashed-bottom">Показать полностью</a></div>');
            }
        });
    }
    if($('.js-answer' ).length ){
        $( '.js-answer' ).each( function() {
            var advantageHeight = $( this ).height();
            if( advantageHeight > 60 ){
                $( this ).addClass('short').after('<div class="clearfix"><a class="js-more-info pull-left dashed-bottom">Показать полностью</a></div>');
            }
        });
    }
    if( $('.js-review-cons') ) {
        $('.js-review-cons').each( function() {
            var consHeight = $( this ).height();
            if( consHeight > 60 ){
                $( this ).addClass('short').after('<div class="clearfix"><a class="js-more-info pull-left dashed-bottom">Показать полностью</a></div>');
            }
        });
    }
    $('.js-more-info').click(function(){
        $(this).parent().prev().toggleClass('short');
        if($(this).parent().prev().hasClass('short')){
            $(this).text("Показать полностью");
        }else{
            $(this).text("Свернуть");
        };
    });




    $('.add_reply_link').click(function(event){
        event.preventDefault();


        var review_id = $(this).attr('review_id');
        var reviews_type = $(this).attr('reviews_type');
        console.log(reviews_type)
        reply_form = '#reply_form_' + review_id;
        $.ajax({
            url: "{% url 'reviewed_with_chains_add_reply' %}",
            type: "GET",
            dataType: "json",
            data: {
                'review_id': review_id,
                'reviews_type': reviews_type
            },
            success: function(msg){
                $(reply_form).loadOverStart();
                $(reply_form).html(msg['html']);
                $(reply_form).loadOverStop();
            }
        });
    });
    $('.rating_yes').click(function(event){
        event.preventDefault();
        var review_id = $(this).attr('review_id');
        span_yes = $(this).find('span');
        span_no = $(this).parent().find('.rating_no').find('span');
        $.ajax({
            url: "{% url 'reviewed_with_chains_rating' %}",
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
            url: "{% url 'reviewed_with_chains_rating' %}",
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

    var urlHash = window.location.hash.replace('#', '')
    if(urlHash.length){
        var hashParams = urlHash.split(';');
        for(var i=0;i<hashParams.length;i++){
            if(hashParams[i].indexOf('review=')==0){
                focusOnReview(hashParams[i].split('=')[1]);
                if($('.variant-reviews').length){
                   $('.variant-reviews')[0].scrollIntoView();
                }else{
                    $('.model-reviews')[0].scrollIntoView();
                }

                break;
            }
        }
    }
    var crutchUrlReadyHash = window.location.hash.replace('#', '');
        if(crutchUrlReadyHash.length){
            if (crutchUrlReadyHash == "variant-reviews") {
                $('.review-count').click();
            }
    };
});