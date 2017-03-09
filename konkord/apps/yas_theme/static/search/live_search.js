$(document).ready(function(){

	var $searchInput = $('.js-search-query'),
		$searchResultBlock = $('.js-live-search-results');

	$searchInput.keyup(function(){
		var query = $(this).val().trim();
		var url = $(this).closest('form').attr('action');
		if(query != "" ){
			delay(function(){
				$.ajax({
					url: url,
					method:'POST',
					type: 'json',
					data: {'query': query},
					success: function(response){
						if ( response.products.length){

							$searchResultBlock.html('');
							var product,
								productBlock,
								image;

							for (var i=0; i<response.products.length; i++){

								product = response.products[i];
								if ( product.image ){
									image = product.image;
								}else{
									image = '/static/img/noimages/no-image-60.png'
								}

								productBlock = '<div class="align-items-center df live-search-results-item">';
								productBlock += '<div class="live-search-results-item--image-wrapp">';
								productBlock += '<img src="' + image + '" class="js-live-search-results-item--image live-search-results-item--image">';
								productBlock += '</div>';
								productBlock +=	'<div class="live-search-results-item--info-wrapp df flex-wrap cw-100 justify-content-between align-items-center">';
								productBlock += '<span class="js-live-search-results-item--name live-search-results-item--name cw-60"><a href="' + product.url + '">' + product.name + '</a></span>';
								productBlock += '<div class="live-search-results-item-prices df align-items-end cw-35 flex-direction-column">';
								productBlock += '<span class="js-live-search-results-item--price live-search-results-item--wholesale-price"> Wholesale: ' + product.price + ' грн</span>';
								if ( product.sale ){
									productBlock += '<span class="live-search-results-item--retail-sale-price tar df justify-content-center align-items-end">';
									productBlock += '<span>Retail: </span>';
									productBlock += '<span class="df flex-direction-column ml5">';
									productBlock += '<span class="old-price">' + product.retail_price + ' грн</span>';
									productBlock += '<span class="sale-price">' + product.sale_price + ' грн</span>';
									productBlock += '</span>';
									productBlock += '</span>';
								}else{
									productBlock += '<span class="live-search-results-item--retail-price tar df justify-content-center align-items-end">';
									productBlock += '<span>Retail: </span><span class="ml5">' + product.retail_price + ' грн</span>';
									productBlock += '</span>';
								}
								productBlock += '</div>';
								productBlock += '</div>';
								productBlock += '</div>';

								$searchResultBlock.append(productBlock);
							}

							all_results = $('<a />')
							.attr('href', url + '?query=' + response.query)
							.text('all results (' + response.total_count + ')')
							.addClass('live-search-all-results');

							$searchResultBlock.append(all_results);
							$searchResultBlock.slideDown();
						}else{
							var noResults = $('<span />').text( "Nothing found");

							$searchResultBlock.html("")
							.append(noResults);
							$searchResultBlock.slideDown();
						}
					}
				})
			}, 500);
		}else{

		}
	})
	.blur(function(){
		delay(function(){	
			$searchResultBlock.slideUp();
		},500);
	});

})
var delay = (function() {
	var timer = 0;
	return function(callback, ms) {
		clearTimeout(timer);
		timer = setTimeout(callback, ms);
	};
})();