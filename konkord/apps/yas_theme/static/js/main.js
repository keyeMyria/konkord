$(function(){
	if( $('.js-show-all-filter-option').length ){
		$('.js-show-all-filter-option').click(function(){
			showHidePopularFilters($(this));
		});
	}
});
function showHidePopularFilters(obj){
	if( obj.hasClass('showed') ){
		obj.removeClass('showed');
		obj.closest('.js-filter-has-popular').find('.filter-option-wrapp[data-popular="False"]').hide();
		obj.text( obj.data('show') );
	}else{
		obj.addClass('showed');
		obj.closest('.js-filter-has-popular').find('.filter-option-wrapp[data-popular="False"]').show();
		obj.text( obj.data('hide') );
	}
}