function setUserData() {
    $.ajax({
        url: CONSTANTS.siteLanguage + '/user-data/',
        type: "POST",
        success: function (res) {
            if(res['status'] == 200) {
                var userBlock = $('.js-user-block');
                if(res['data']['user_authenticated']) {
                    var accountLink = $('<a>', {
                        class: 'mr5 header-username-wrapp df',
                        href: userBlock.data('account-url')
                    });
                    accountLink.append($('<i>', {class: 'dib glyphicon glyphicon-user mr5'}));
                    accountLink.append($('<span>', {class: 'dib username', text: res['data']['username']}));

                    var logoutLink = $('<a>', {href: userBlock.data('logout-url')});
                    logoutLink.append($('<span>', {class: 'glyphicon glyphicon-log-out'}));
                    userBlock.append(accountLink);
                    userBlock.append(logoutLink);
                } else {
                    userBlock.append($('<a>', {href: userBlock.data('login-url'), text: userBlock.data('login-text')}));
                }
            }
        }
    })
}

$(function () {
    setUserData();
});