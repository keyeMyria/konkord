django.jQuery(function () {
	var sortableChangelist = function () {
		var init = function () {
			$('#result_list input[id$="position"]').closest('td').css('cursor', 'move');
            $('#result_list input[id$="position"]').hide().after('<i class="icon-move pull-left"></i>');
			$('#result_list tbody').sortable({
				axis: 'y',
				items: 'tr',
				cursor: 'move',
                handle: '.field-position',
                update: function (event, ui) {
					var items = $(this).find('tr').get();
					$(items).each(function (i) {
						$('input[id$=position]', this).val(i + 1);
					});

					// Update row classes
					$(this).find('tr').removeClass('row1').removeClass('row2');
					$(this).find('tr:even').addClass('row1');
					$(this).find('tr:odd').addClass('row2');
				}
			});
		};
		init();
	};

	sortableChangelist();

});