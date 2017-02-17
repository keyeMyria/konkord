$(function () {
    var $subscribeForm = $('#subscribe-form');
    $.ajax({
        url: $subscribeForm.attr('action'),
        type: 'GET',
        success: function (res) {
            console.log(res);
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
                if(res.message) {
                    alertify.success(res.message);
                }
            }
        })
    })
});