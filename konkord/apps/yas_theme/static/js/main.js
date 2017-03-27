$(function(){
	if( $('.js-show-all-filter-option').length ){
		$('.js-show-all-filter-option').click(function(e){
			e.preventDefault();
			
			if( $(this).hasClass('showed') ){
				hidePopularFilters( $(this) );
			}else{
				showPopularFilters($(this));
			}
		});
	}



	var $easyzoom = $('.easyzoom').easyZoom();
	
	var api = $easyzoom.data('easyZoom');
	$('.js-sub-image').click(function(){
		if (api){	
			api.teardown();
		}
		if( window.innerWidth > CONSTANTS.maxExtrasmallScreen ){
			if (api){
				api._init();
			}
		}

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

	if( window.innerWidth <= CONSTANTS.maxExtrasmallScreen ){

		$('.js-sticky-titles').sticky({
			topSpacing: 0
		});
		if (api){
			api.teardown();
		}
	}else{
		$(".js-sticky").sticky({
			topSpacing:0,

		});
		$('.js-sticky-titles').unstick();
		if (api){
			api._init();
		}
	}

	$(window).resize(function(){
		if( window.innerWidth <= CONSTANTS.maxExtrasmallScreen ){
			if (api){
				api.teardown();
			}
		}else{
			if (api){
				api._init();
			}
		}

	});

	$('.js-img-gallery-pop-up').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
		fixedContentPos: true,
		mainClass: 'mfp-no-margins mfp-with-zoom',
		gallery:{
		  enabled:true
		}, 
		image: {
		  verticalFit: true
		},
		zoom: {
		  enabled: true,
		  duration: 300 
		}
	});

	$('.js-popup-link-without-gallery').magnificPopup({
		type: 'image',
		closeOnContentClick: true,
	})

	$('.js-tabs').easytabs({
		animate: false,
	});


	$('.js-add-review-button').magnificPopup({
		type: "inline",
		midClick: true,
		closeBtnInside: false,
		callbacks: {
		    open: function() {
		     	var $reviews = $('#reviews_with_chains.reviews');
		     	    content_id = $reviews.data('content-id'),
		     	    content_type_id = $reviews.data('content-type-id');
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
	
	$('.js-size-name').click(function(){

		var $self = $(this),
			isActiveSize = $self.hasClass('active'),
			$chooseAmountInput = $self.parent().find('.js-product-amount'),
			sizeAamount = parseInt($chooseAmountInput.val() ),
			$placeAmount = $self.find('.js-size-amount');
			// $('#main').animate({scrollTop: 2000},"300);
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


	$('.js-filter-name').click(function(){
		showHideFilterContent( $(this) );
	});

	checkVisibilityOfFilters();

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

function showHideFilterContent( obj ){
	obj.closest('.js-filter-wrapper').toggleClass('opened ')
	.find('.js-filter-options-wrapper').slideToggle();
}

function checkVisibilityOfFilters(){
	if ($(document).width() <= CONSTANTS.maxExtrasmallScreen){
		$('.js-filter-options-wrapper').hide();
		$('.js-filter-wrapper').removeClass('opened');

	}else{
		$('.js-filter-options-wrapper').show();
		$('.js-filter-wrapper').addClass('opened');
	}
}

function disableScrollingPage(){
    $('body, html').addClass('scroll-none');
}

function enableScrollingPage(){
    $('body, html').removeClass('scroll-none');
}

$(window).resize(function(){
	checkVisibilityOfFilters();

	$(".js-sticky").sticky({
		topSpacing:0,
		
	});

	if( window.innerWidth <= CONSTANTS.maxExtrasmallScreen ){
		$('.js-sticky-titles').sticky({
			topSpacing: 0
		});
		$(".js-sticky").unstick();
	}else{
		$('.js-sticky-titles').unstick();
	}

});

