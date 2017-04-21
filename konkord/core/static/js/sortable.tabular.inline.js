django.jQuery(function () {
	var sortableTabularInline = function () {
		var init = function () {
			var sortableInlines = $('.inline-related:has(td.field-position):has(input[name$=-MAX_NUM_FORMS][value=0])');
			sortableInlines.find('td.field-position input').hide().after('<i class="icon-move pull-left"></i>');
			if(sortableInlines.find('input[name$=-INITIAL_FORMS]').val() <= 1){
				return;
			}
            sortableInlines.find('.form-row.has_original .field-position').css('cursor', 'move');

			sortableInlines.find('h2').append('<span class="description">Note: Drag &amp; drop rows to reorder. Save new inline row first</span>')

			sortableInlines.sortable({
				axis: 'y',
				items: '.form-row.has_original',
				handle: '.field-position',
				cursor: 'move',
				update: function (event, ui) {
					$('.inline-related .form-row.has_original').each(function (i) {
						$('input[id$=position]', this).val(i + 1);
					});
				},
			});
		};
		init();
	};

	sortableTabularInline();

});