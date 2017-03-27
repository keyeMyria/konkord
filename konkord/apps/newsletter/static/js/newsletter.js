$(function () {
    var $subscribeForm = $('#subscribe-form');
    $.ajax({
        url: $subscribeForm.attr('action'),
        type: 'GET',
        success: function (res) {
            $subscribeForm.html(res['html']);
        }
    });
    $subscribeForm.submit(function (e) {
        var $form = $(this);
        e.preventDefault();
        $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: $form.serialize(),
            success: function (res) {
                $form.html(res.html);
                var error = $('.js-newsletter-error').text().trim();
                if(res.message) {
                    alertify.notify(res.message, 'success', 500);
                }

                if ( error ){
                    alertify.notify(error, 'error', 500);
                }
            }
        })
    })
});