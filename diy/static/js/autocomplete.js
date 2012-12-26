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
    $("#autoList").css({"top":$("#input").offset().top+$(".ace_text-input").offset().top + $(".ace_text-input").height(),position:"absolute"});
    $("#autoList").css({"left":$("#input").offset().left+$(".ace_text-input").offset().left,position:"absolute"});
}

document.getElementById('autoList').style.width = '100px';
document.getElementById('autoList').style.height = '300px';
document.getElementById('autoList').style.background = 'red';
document.getElementById('autoList').style.position = 'absolute';
document.getElementById('autoList').style.opacity = '0.6';
document.onmousemove = mouseMove;
document.body.onkeydown = keydown;
document.body.onkeypress = keydown;
document.body.onkeyup = keydown;
