
clip = function() {
    ace_url = 'http://d1n0x3qji82z53.cloudfront.net/src-min-noconflict/ace.js';
    //ace_url = '/static/js/ace-src/ace.js';
    $.getScript(ace_url, function(data, textStatus, jqxhr){
        console.log(textStatus);
        var editor = ace.edit('editor');
        editor.setTheme('ace/theme/monokai');
        editor.getSession().setMode('ace/mode/c_cpp');
    })
    .fail(function(jqxhr, settings, exception){
        console.log(exception);
    });
}
