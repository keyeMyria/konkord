$(document).ready(function(){
	$('#search-query').keyup(function(){
		var query = $(this).val();
		var url = $(this).parents('form').attr('action');
		delay(function(){
			$.ajax({
				url: url,
				method:'POST',
				type: 'json',
				data: {'query': query},
				success: function(response){
					$('#live-search-results').html('')
					for (var i=0; i<response['products'].length; i++){
						var product = response['products'][i];
						console.log(product)
						var product_block = $('<div />');
						product_block.addClass('col-xs-12');
						var image = $('<img />');
						image.attr('src', product['image']);
						var name = $('<span />');
						name.text(product['name'])
						var price = $('<span />')
						price.text(product['price'])
						product_block.append(image, name, price)
						$('#live-search-results').append(product_block)
					}
					all_results = $('<a />');
					all_results.attr('href', url + '?query=' + response['query'])
					all_results.text('all results (' + response['total_count'] + ')')
					$('#live-search-results').append(all_results)
					$('#live-search-results').show()
				}
			})
		}, 500)
	})
})
var delay = (function() {
	var timer = 0;
	return function(callback, ms) {
		clearTimeout(timer);
		timer = setTimeout(callback, ms);
	};
})();