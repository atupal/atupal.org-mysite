window.onload=display;
var sum = 42;
sum = -1;

for (var i = 0; i < sum; ++ i) {
    var div = document.createElement('div');
    div.setAttribute("id", "div_" + i.toString());
    div.setAttribute("style", "position:absolute");
    document.body.appendChild(div);
}

for (var i = 0; i < sum; ++ i) {
    var img = document.createElement('img');
    img.setAttribute('src', '/images/' + 'psb_' + (i + 1).toString() + '.jpg');
    document.getElementById("div_" + i.toString()).appendChild(img);
}

function setCookie(name, value, expiredays){
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + exdate.toGMTString());

    return true;
}

function getCookie(name) {
    if(document.cookie.length > 0) {
        var start = document.cookie.indexOf("name" + "=");
        var end;
        if (start != -1) {
            start = start + name.length + 1;
            end = document.cookie.indexOf(";", start);
            if(end == -1) {
                end = document.cookie.length;
            }

        }
        return unescape(document.cookie.substring(start, end));
    }
}
function display() {
    alert(getPic(0, 5));
    return;
    var col = 0;
    var row = document.body.clientWidth - 50;
    var H = 250;
    var h = 0;
    var w = 300;
    var jiange = 20;
    var imgs = document.getElementsByTagName("img");
    for (var i = 0; i < imgs.length; ++ i) {
        var flag = i;
        h = row / imgs[i].width * imgs[i].height;
        while (h > H && i < imgs.length - 1) {
            ++ i;
            h = row / (row / h + (imgs[i].width + jiange) / imgs[i].height);
        }
        w = 0;
        for (var j = flag; j <= i; ++ j) {
            imgs[j].parentNode.style.top = (col + jiange).toString() + "px";
            imgs[j].parentNode.style.left = (w + jiange).toString() + "px";
            imgs[j].style.height = h.toString() + "px";
            w = w + h / imgs[j].height * imgs[j].width + jiange;
        }
        col += h + jiange;
    }
}

function getPic(startIndex, count) {
    var req = new XMLHttpRequest();
    var requrl = 'getPic';
    requrl = 'getPic' + "?startIndex=" + startIndex.toString() + "&count=" + count.toString(); 
    alert(requrl)
    req.open('GET', requrl, false);
    req.send(null);
    return req.responseText;
}

window.onresize=display;
//$(window).resize(display);

