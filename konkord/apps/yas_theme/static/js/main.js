$(function(){

	if( $(window).scrollTop() > 100 ){
		$('.js-scrollup').fadeIn();
	}


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

	var mainImage = new MainImageAttributes($('.js-huge-image'));
	mainImage.setAttrHeight();
	mainImage.setAttrWidth();

	$('.js-sub-image').click(function(){
		var mainImage = new MainImageAttributes($('.js-huge-image'));

		mainImage.removeAttrs();
		
		replaceMainImage( $(this) );

		mainImage.setAttrHeight();
		mainImage.setAttrWidth();
	});
	if( window.innerWidth > CONSTANTS.maxExtrasmallScreen ){
		$('.easyzoom a').imgZoom({
			origin: "href",
			boxWidth: "300",
			boxHeight: "500"
		});
	}
	
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
		var mainImage = new MainImageAttributes($('.js-huge-image'));

		mainImage.removeAttrs();

		mainImage.setAttrHeight();
		mainImage.setAttrWidth();

	}else{
		$(".js-sticky").sticky({
			topSpacing:0,

		});
		$('.js-sticky-titles').unstick();
	}

	$(window).resize(function(){
		var mainImage = new MainImageAttributes($('.js-huge-image'));

		mainImage.removeAttrs();

		mainImage.setAttrHeight();
		mainImage.setAttrWidth();

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
			$('#main').animate( {scrollTop: $('#main').innerHeight()},500 );
		if ( isActiveSize ) {
			hideSizesList($self, sizeAamount, $placeAmount, sizeAamount);
		}else{
			showSizesList( $self, $placeAmount );
		}

	});

	$('.js-faq-text').click(function(){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		}else{
			$(this).addClass('active');
		}
	});

	$('.js-product-amount').keyup(function(){
		if( parseInt( $(this).val(), 10) ){
			removeShadowFromListOfSizes();
		}
	}).change(function(){
		if( parseInt( $(this).val(), 10) ){
			removeShadowFromListOfSizes();
		}
	});
	

	$('.js-scrollup').click(function(){
		$('html, body').animate({scrollTop: 0}, 500);
	});


	$('.js-filter-name').click(function(){
		showHideFilterContent( $(this) );
	});

	checkVisibilityOfFilters();

	$('input[name="phone"]').mask('38 (000) 000-00-00',{placeholder: "38 (066) 123-45-67"});

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
				removeShadowFromListOfSizes();
			}
		}
	
	});
}

function removeShadowFromListOfSizes(){	
	$('.sizes-list').removeClass('with-shadow');
}

function addShadowTolistsOfShadow(){
	$('.sizes-list').addClass('with-shadow');
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
	var $hugeImage = $('.js-huge-image');
	$hugeImage.attr( 'src', obj.data('huge-image') );
	$hugeImage.attr( 'href', obj.data('mega-huge-image') );
	$hugeImage.parent().attr( 'href', obj.data('mega-huge-image') );
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

function clearAllSizesOnProduct(){
	$('.js-size').each(function(){
		var blockAmount = $(this).find('.js-size-name'),
			input = $(this).find('.js-size-value input'),
			amountPlace = $(this).find('.js-size-amount');

			input.val(0);

			hideSizesList(blockAmount, false, amountPlace);


	});
}

function MainImageAttributes(imageObj){

	function getImageWidth(){
		return parseInt(imageObj.width());
	}

	function getImageHeight(){
		return parseInt(imageObj.height());
	}

	this.setAttrHeight = function(){
		imageObj.bind('oanimationend animationend webkitAnimationEnd', function() { 
			imageObj.attr('height', getImageHeight()); 
		});
	}

	this.setAttrWidth = function(){
		imageObj.bind('oanimationend animationend webkitAnimationEnd', function() { 
			imageObj.attr('width', getImageWidth() );
		});
	}
	this.removeAttrs = function(){
		imageObj.attr({
			'width': "",
			"height": ""
		});	
	} 

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

		$('.easyzoom a').unbind('mouseenter');

	}else{
		$('.js-sticky-titles').unstick();
		
		$('.easyzoom a').unbind('mouseenter');
		$('.easyzoom a').imgZoom({
			origin: "href",
			boxWidth: "300",
			boxHeight: "500"
		});
	}
});

$(window).scroll(function(){
	if( $(window).scrollTop() > 100 ){
		$('.js-scrollup').fadeIn();
	}else{
		$('.js-scrollup').fadeOut();
	}
});
function translate(text){
	if( TRANSLATIONS[text] && TRANSLATIONS[text][CONSTANTS.languageForTranslations] ){
		return TRANSLATIONS[text][CONSTANTS.languageForTranslations];
	}else{
		return text;
	}
}

! function(a) {
    function f(a, b) {
        if (!(a.originalEvent.touches.length > 1)) {
            a.preventDefault();
            var c = a.originalEvent.changedTouches[0],
                d = document.createEvent("MouseEvents");
            d.initMouseEvent(b, !0, !0, window, 1, c.screenX, c.screenY, c.clientX, c.clientY, !1, !1, !1, !1, 0, null), a.target.dispatchEvent(d)
        }
    }
    if (a.support.touch = "ontouchend" in document, a.support.touch) {
        var e, b = a.ui.mouse.prototype,
            c = b._mouseInit,
            d = b._mouseDestroy;
        b._touchStart = function(a) {
            var b = this;
            !e && b._mouseCapture(a.originalEvent.changedTouches[0]) && (e = !0, b._touchMoved = !1, f(a, "mouseover"), f(a, "mousemove"), f(a, "mousedown"))
        }, b._touchMove = function(a) {
            e && (this._touchMoved = !0, f(a, "mousemove"))
        }, b._touchEnd = function(a) {
            e && (f(a, "mouseup"), f(a, "mouseout"), this._touchMoved || f(a, "click"), e = !1)
        }, b._mouseInit = function() {
            var b = this;
            b.element.bind({
                touchstart: a.proxy(b, "_touchStart"),
                touchmove: a.proxy(b, "_touchMove"),
                touchend: a.proxy(b, "_touchEnd")
            }), c.call(b)
        }, b._mouseDestroy = function() {
            var b = this;
            b.element.unbind({
                touchstart: a.proxy(b, "_touchStart"),
                touchmove: a.proxy(b, "_touchMove"),
                touchend: a.proxy(b, "_touchEnd")
            }), d.call(b)
        }
    }
}(jQuery);