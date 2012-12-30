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
    $("#autoList").css({"top":$("#input").offset().top+$(".ace_text-input").offset().top + $(".ace_text-input").height(),position:"absolute"});
    $("#autoList").css({"left":$("#input").offset().left+$(".ace_text-input").offset().left,position:"absolute"});
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
    //var jiaodian = getElementByClass('ace_text-input');
    //document.getElementById('autoList').style.left = jiaodian.style.left;
    //document.getElementById('autoList').style.top = jiaodian.style.top;
    $("#autoList").css({"top":$(".ace_text-input").offset().top + $(".ace_text-input").height(),position:"absolute"});
    $("#autoList").css({"left":$(".ace_text-input").offset().left,position:"absolute"});
    var line = editor.getCursorPosition();
    var text = editor.getSelection().doc.$lines[line.row].substring(0,line.column);
    text = text.split(' ');
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
    keyword = ['int', 'for', 'while', 'double', 'float', 'short', 'string', 'char', 'return', 'void', 'do', 'if', 'else', 'goto','continue', 'case', 'switch', 'break', 'hehe'];

    for (var i = 0; i < doc.length; ++ i) {
        if (doc[i].indexOf(str) != -1) {
            result.push(doc[i]);
        }
    }

    var flag = 0;
    for (var i = 0; i < keyword.length; ++ i) {
        if (keyword[i].indexOf(str) != -1) {
            ++ flag;
            document.getElementById('autoList').style.height = (flag * 4).toString() + '0px';
            var pelement = document.createElement("p");
            var messagenode = document.createTextNode(keyword[i]);
            pelement.appendChild(messagenode);
            document.getElementById('autoList').appendChild(pelement);
        }
    }

}

document.getElementById('autoList').style.width = '100px';
document.getElementById('autoList').style.height = '0px';
document.getElementById('autoList').style.background = 'red';
document.getElementById('autoList').style.position = 'absolute';
document.getElementById('autoList').style.opacity = '0.6';
document.onmousemove = mouseMove;
document.body.onkeydown = keydown;
document.body.onkeypress = keydown;
document.body.onkeyup = keydown;
