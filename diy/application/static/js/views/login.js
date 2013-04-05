
login = function(){
    var username = $('#login_username')[0].value;
    var passwd = $('#login_passwd')[0].value;
    $.ajax({
        type: 'POST',
        url: '/user/login',
        data: {username :username, password : passwd},
        success: function(data, statustext, jqXHR){
        },
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        alert(errorThrown);
    });
}

loginDialog = function(){
    $.Dialog({
        'title': 'Login',
        'content': '<input id="login_username" type="text"><input id="login_passwd" type="password">',
        'draggable': true,
        'overlay': true,
        'closeButton': true,
        'buttonAlign': 'right',
        'position': {
            'zone': 'center'
        },
        'buttons': {
            'register': {
                'action': function(){}
            },
            'login': {
                'action': login
            }
        }
    });
}
