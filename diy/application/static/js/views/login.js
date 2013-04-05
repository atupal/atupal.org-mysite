
loginDialog = function(){
    $.Dialog({
        'title': 'Login',
        'content': '<button>Login</button>',
        'draggable': true,
        'overlay': true,
        'closeButton': true,
        'buttonAlign': 'right',
        'position': {
            'zone': 'center'
        },
        'buttons': {
            'button1': {
                'action': function(){}
            },
            'button2': {
                'action': function(){}
            }
        }
    });
}
