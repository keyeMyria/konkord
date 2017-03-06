$(function(){
	if( $('.js-show-all-filter-option').length ){
		$('.js-show-all-filter-option').click(function(){
			if( $(this).hasClass('showed') ){
				hidePopularFilters( $(this) );
			}else{
				showPopularFilters($(this));
			}
		});
	}

	$(".js-sticky").sticky({topSpacing:0});

	var $easyzoom = $('.easyzoom').easyZoom();
	var api = $easyzoom.data('easyZoom');
	$('.js-sub-image').click(function(){
		api.teardown();
		api._init();

		replaceMainImage( $(this) );
	});

	$('.easyzoom a, .js-popup-link').magnificPopup({
	  type: 'image',
	  closeOnContentClick: true,
	  fixedContentPos: true,
	  mainClass: 'mfp-no-margins mfp-with-zoom', 
	  image: {
	    verticalFit: true
	  },
	  zoom: {
	    enabled: true,
	    duration: 300 
	  }
	});

	$('.js-tabs').easytabs({
		animate: false,
	});


	$('.js-add-review-button').magnificPopup({
		type: "inline",
		callbacks: {
		    open: function() {
		     	var $reviews = $('#reviews_with_chains.reviews');
		     	    content_id = $reviews.data('content-id'),
		     	    content_type_id = $reviews.data('content-type-id');
		     		load_review_form(content_type_id, content_id, 'reviews');
		    },

		  }
	});

	$('.js-analogous-list').slick({
		slidesToShow: 4,
		dots: true,
		speed: 1000,
		autoplay: true,
		autoplaySpeed: 5000,
		slidesToScroll: 4,
		prevArrow: '<button type="button" class="slick-arrow slick-prev" data-text="‹"></button>',
		nextArrow: '<button type="button" class="slick-arrow slick-next" data-text="›"></button>',
		draggable: false

	});

	initSpinner( $('.js-size-value input.js-product-amount') );
	
	$('.js-size-value input').spinner({
		min: 0,
		max: 500,
		change: function( event, ui ) {
			$(this).spinner('value', parseInt($(this).spinner('value'), 10) || 0);
		},
		stop: function( event, ui ) {
			if( parseInt( $(this).val(), 10) ){
				$('.js-size-list_error').slideUp();
			}
		}
	
	});


	$('.js-size-name').click(function(){

		var $self = $(this),
			isActiveSize = $self.hasClass('active'),
			$chooseAmountInput = $self.parent().find('.js-product-amount'),
			sizeAamount = parseInt($chooseAmountInput.val() ),
			$placeAmount = $self.find('.js-size-amount');

		if ( isActiveSize ) {
			hideSizesList($self, sizeAamount, $placeAmount, sizeAamount);
		}else{
			showSizesList( $self, $placeAmount );
		}

	});
	$('.js-product-amount').keyup(function(){
		if( parseInt( $(this).val(), 10) ){
			$('.js-size-list_error').slideUp();
		}
	}).change(function(){
		if( parseInt( $(this).val(), 10) ){
			$('.js-size-list_error').slideUp();
		}
	});



});

function initSpinner(input){
		input.spinner({
		min: 0,
		max: 500,
		change: function( event, ui ) {
			$(this).spinner('value', parseInt($(this).spinner('value'), 10) || 0);
		},
		stop: function( event, ui ) {
			if( parseInt( $(this).val(), 10) ){
				$('.js-size-list_error').slideUp();
			}
		}
	
	});
}

function showSizesList(sizeWrap, placeAmount){
	sizeWrap.addClass('active');
	placeAmount.hide();
}

function hideSizesList(obj, sizeAamount, $placeAmount, sizeAamount){
	obj.removeClass('active');

	if ( sizeAamount ){
		setSizesAmount( $placeAmount, sizeAamount, obj, "add" );
	}else{
		setSizesAmount( $placeAmount, "", obj, "remove" );
	}

	$placeAmount.show();
}

function setSizesAmount(placeAmount, sizeAamount, sizeWrap, action){
	placeAmount.text(sizeAamount);

	if( action == 'add' ){
		sizeWrap.addClass('choosen');
	}else if( action == "remove"){
		sizeWrap.removeClass('choosen')
	}
}

function replaceMainImage(obj){
	$('.js-huge-image').attr( 'src', obj.data('huge-image') );
	$('.js-huge-image').parent().attr( 'href', obj.data('mega-huge-image') );
}


function hidePopularFilters(obj){
	obj.removeClass('showed')
	.text( obj.data('show') )
	.closest('.js-filter-has-popular').find('.filter-option-wrapp[data-popular="False"]').hide();
}

function showPopularFilters(obj){
	obj.addClass('showed')
	.text( obj.data('hide') )
	.closest('.js-filter-has-popular').find('.filter-option-wrapp[data-popular="False"]').show();
}

function getReviewsAmount(){
	return $('.js-variant-reviews .js-one-review').length;
}

function setReviewsAmount(){
	$('.js-reviews-amount span:last').text( getReviewsAmount() );
}

function getAverageRating(){
	var ratingSum = 0,
		$reviewsArr = $('.js-variant-reviews .js-one-review meta[itemprop="ratingValue"]'),
		average = 0;

	$reviewsArr.each(function(){
		ratingSum += parseInt( $(this).attr('content') ); 
	});

	if(ratingSum){
		average = ratingSum / $reviewsArr.length;
	}

	return average;
}
function setAverageRating(){
	var width;
	width = getAverageRating() * 10;
	if( width ){
		$('.js-less-rating').width( width ).removeClass('empty');
	}
}


