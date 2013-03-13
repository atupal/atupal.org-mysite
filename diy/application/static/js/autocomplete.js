//记录自动补全项的位置
_locate = 0;
_is_selecting = 0;
_sum = 0;



function mousePosition(ev){  
    if(ev.pageX || ev.pageY){  
        return {x:ev.pageX, y:ev.pageY};  
    }  
    return {  
        x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,  
        y:ev.clientY + document.body.scrollTop  - document.body.clientTop  
    };  
}  

function mouseMove(ev){  
    ev = ev || window.event;  
    var mousePos = mousePosition(ev);  
    //var jiaodian = getElementByClass('ace_text-input');
    document.getElementById('x_origin').value = mousePos.x;  
    document.getElementById('y_origin').value = mousePos.y;  
    //document.getElementById('autoList').style.left = jiaodian.style.left;
    //document.getElementById('autoList').style.top = jiaodian.style.top;
    //获取元素的位置
    //var x = e.offsetLeft;
    //  var y = e.offsetTop;
    //  用jquery获取元素的位置
    //$("#autoList").css({"top":$("#input").offset().top+$(".ace_text-input").offset().top + $(".ace_text-input").height(),position:"absolute"});
    //$("#autoList").css({"left":$("#input").offset().left+$(".ace_text-input").offset().left,position:"absolute"});
}  

function getElementByClass(matchClass) {
    var elems = document.getElementsByTagName('*'), i;
    for (i in elems) {
        if((' ' + elems[i].className + ' ').indexOf(' ' + matchClass + ' ')
                > -1) {
                    //elems[i].innerHTML = content;
                    return elems[i];
                }
    }
}

function keydown(ev) {
    if (_is_selecting)
        return;
    _locate = 0;
    //var jiaodian = getElementByClass('ace_text-input');
    //document.getElementById('autoList').style.left = jiaodian.style.left;
    //document.getElementById('autoList').style.top = jiaodian.style.top;
    $("#autoList").css({"top":$(".ace_text-input").offset().top + $(".ace_text-input").height(),position:"absolute"});
    $("#autoList").css({"left":$(".ace_text-input").offset().left,position:"absolute"});
    var line = editor.getCursorPosition();
    var text = editor.getSelection().doc.$lines[line.row].substring(0,line.column);
    text = text.split(/[\s\(\)\[\]<>{};"',\.:]/);
    text = text[text.length - 1];
    query(text);
}

function query(str) {
    parentNode = document.getElementById('autoList');
    while (parentNode.firstChild) {
        var oldNode = parentNode.removeChild(parentNode.firstChild);
        oldNode = null;
    }
    document.getElementById('autoList').style.height = '0px';
    if (str == "" || str == null)
        return;
    var result = [];
    //doc = editor.getValue();
    //doc = doc.split('');
    doc = [];
    keyword = ['int', 'for', 'while', 'double', 'float', 'short', 'string', 'char', 'return', 'void', 'do', 'if', 'else', 'goto','continue', 'case', 'switch', 'break', 'hehe', 'and', 'or', 'not'];

    for (var i = 0; i < doc.length; ++ i) {
        if (doc[i].indexOf(str) != -1) {
            result.push(doc[i]);
        }
    }

    var flag = 0;
    for (var i = 0; i < keyword.length; ++ i) {
        if (keyword[i].indexOf(str) != -1) {
            ++ flag;
            document.getElementById('autoList').style.height = (flag * 20).toString() + 'px';
            var id = 'auto_word_' + flag.toString();
            var auto_word = document.createElement("span");
            auto_word.setAttribute('id', id);
            auto_word.setAttribute('style', '');
            var auto_word_content = document.createTextNode(keyword[i]);
            var hanghang = document.createElement('br');
            auto_word.appendChild(auto_word_content);
            document.getElementById('autoList').appendChild(auto_word);
            document.getElementById('autoList').appendChild(hanghang);
        }
    }
    _sum = flag;

}

function nextWord(){
    _is_selecting = 1;


    var pre_id = 'auto_word_' + _locate.toString();
    _locate = _locate % _sum + 1;
    var id = 'auto_word_' + _locate.toString();

    //var pre_locate = (_locate - 1 + _sum - 1) % _sum + 1;
    //var pre_id = 'auto_word_' + pre_locate.toString();

    try {
        document.getElementById(id).style.background = 'blue';    
        document.getElementById(pre_id).style.background = '';    
        //editor.insert(document.getElementById(id).innerHTML);
    }
    catch(err){
        //
    }
    _is_selecting = 0;
}

function preWord(){
    _is_selecting = 1;

    var pre_id = 'auto_word_' + _locate.toString();
    _locate = (_locate - 1 + _sum - 1) % _sum + 1;
    var id = 'auto_word_' + _locate.toString();

    //var pre_locate = _locate % _sum + 1;
    //var pre_id = 'auto_word_' + pre_locate.toString();

    try {
        document.getElementById(id).style.background = 'blue';    
        document.getElementById(pre_id).style.background = '';    
        //editor.insert(document.getElementById(id).innerHTML);
    }
    catch(err){
        //
    }
    _is_selecting = 0;
}


document.getElementById('autoList').style.width = '100px';
document.getElementById('autoList').style.height = '0px';
document.getElementById('autoList').style.background = 'red';
document.getElementById('autoList').style.position = 'absolute';
document.getElementById('autoList').style.opacity = '0.6';
document.onmousemove = mouseMove;
//document.body.onkeydown = keydown;
//document.body.onkeypress = keydown;
//document.body.onkeyup = keydown;
var editor = ace.edit('editor');

editor.getSession().selection.on('changeCursor', keydown);

editor.commands.addCommand({
    name: 'myCommand',
    bindKey: {win: 'Ctrl-B',  mac: 'Command-N'},
    exec: nextWord,
    readOnly: true // false if this command should not apply in readOnly mode
});

editor.commands.addCommand({
    name: 'myCommand',
    bindKey: {win: 'Ctrl-P',  mac: 'Command-P'},
    exec: preWord,
    readOnly: true // false if this command should not apply in readOnly mode
});
document.onkeyup = function(e){
    var e = window.event ? window.event : e;
    if(e.ctrlkey && e.which==38 && 1 == 2) {
        preWord();
        return;
    }
    switch(e.keyCode){
        case 38: //up
            preWord();
            break;
        case 40: //down
            nextWord();
            break;
        case 37: //left
            break;
        case 39: //right
            break;}}
