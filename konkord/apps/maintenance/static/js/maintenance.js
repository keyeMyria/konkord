$(function() {
    $.ajax({
        method: 'POST',
        url: '/maintenance/messages/',
        dataType: 'JSON',
        success: function (data) {
            $('#maintenance-block-wrapper').html(data.html);
        }
    })
});