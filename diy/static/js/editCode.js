function ts(){
}
function getDocumentString() {
    var codestr = editor.getSession().getValue();
    //var id = Math.random();
    //action = 'action';
    //document.write('<form id="post' + id + '" name="post'+ id +'" action="' + action +  '" target="codestr' + '" method="post">');
    //document.write('<input type="hidden" name="' + "codestr" + '" value="' + codestr + '" />');
    //document.write('</form>'); 
    //document.getElementById('post' + id).submit();
    var input = document.getElementById('inputtext').value;
    /*
       input = input.replace(/\+/g, "%2B");//"+"¿?¿?  
       input = input.replace(/\&/g, "%26");//"&"
       input = input.replace(/\#/g, "%23");//"#"

       codestr = codestr.replace(/\+/g, "%2B");//"+"¿?¿?  
       codestr = codestr.replace(/\&/g, "%26");//"&"
       codestr = codestr.replace(/\#/g, "%23");//"#"
       */
    //alert(codestr);
    //alert(input);

    input = encodeURIComponent(input);
    codestr = encodeURIComponent(codestr);

    var request = new XMLHttpRequest();
    request.open('POST', '/action', false);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send('input=' + input + '&codestr=' + codestr);
    var h = request.responseText;
    if (h.indexOf("atupalykl67") != -1) {
        alert("pleas login first");
        login();
        return;
    }
    alert(h);
    document.getElementById('inputtext').value = h;
    return;

    document.getElementById('input').value = input;
    document.getElementById('codestr').value=codestr;
    document.getElementById('form').submit();
    return;
}

function login()
{
    loginBack.style.display = "inline";
    loginBack.style.width = "100%";
    loginBack.style.height = "100%";
    loginWin.style.display = "inline";
    loginWin.style.left = document.body.clientWidth / 2 - loginWin.clientWidth / 2;
    loginWin.style.top = document.body.clientHeight / 2 - loginWin.clientHeight / 2;
}
function cancel_login() {
    loginBack.style.display = "none";
    loginWin.style.display = "none";
    document.getElementById("login").style.display = "";
}
function register() {
    var iWidth = 500; 
    var iHeight = 300;

    var iTop = (window.screen.availHeight - 30 - iHeight) / 2; 

    var iLeft = (window.screen.availWidth - 10 - iWidth) / 2; 

    window.open('register', 'newwindow', 'height=' + iHeight + ',width=' + iWidth + ',top=' + iTop + ',left=' + iLeft + ',toolbar=no,menubar=no,scrollbars=no, resizable=yes,location=no, status=no');
}
function hidePinel() {
    if (document.getElementById("rightPanel").style.display == "none") {
        document.getElementById("rightPanel").style.display = "inline";
        document.getElementById("editor").style.width = "60%";
        document.getElementById("hideDiv").style.left = "80%";
        return;
    }
    document.getElementById("rightPanel").style.display = "none";
    document.getElementById("editor").style.width = "80%";
    document.getElementById("hideDiv").style.left = document.body.clientWidth - document.getElementById('hideDiv').clientWidth;
}
function saveCode() {
    var codestr = editor.getSession().getValue();
    var filename = prompt("输入一个文件名");
    if (filename == null || filename == '') {
        alert('文件名错误');
        return;
    }
    codestr = encodeURIComponent(codestr);
    filename = encodeURIComponent(filename);

    var request = new XMLHttpRequest();
    request.open('POST', '/saveCode', false);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send('codestr=' + codestr + '&filename=' + filename);
    var h = request.responseText;
    if (h == 'yes') {
        alert('文件保存成功，' + filename);
    }
    else {
        alert(filenem + '保存失败');
    }
    return;
}
function getHideIframe() {
    var h = document.getElementById('bianyi').contentDocument.body.innerHTML.toString();
    alert(h)
        document.getElementById('inputtext').value = h;
}
function getCode() {
    var request = new XMLHttpRequest();
    request.open('GET', '/getCode', false);
    request.send(null);
    if (request.status === 200) {
        files = request.responseText.split(/[\s]/);
        var rightPanel = document.getElementById('codes');
        var childs = rightPanel.childNodes;  
        for(var i = childs.length - 1; i >= 0; i--) {
            rightPanel.removeChild(childs[i]);
        }
        for (var i = 0; i < files.length; ++ i) {
            var file = document.createElement('a');
            var fileName = document.createTextNode(files[i]);
            var hanghang = document.createElement('br');
            file.appendChild(fileName);
            //file.setAttribute('href', 'getFile/' + '?' + 'fileName=' + files[i]);
            file.setAttribute('onclick', 'get_file(' + '"' + files[i] + '"' + ')');
            rightPanel.appendChild(hanghang);
            rightPanel.appendChild(file);
        }
    }
}
function get_file(file_name) {
    var request = new XMLHttpRequest();
    request.open('POST', '/getFile', false);
    file_name = encodeURIComponent(file_name);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send('file_name=' + file_name);
    if (request.status === 200) {
        editor.setValue(request.responseText);
    }
}
function deleteuser() {
    var request = new XMLHttpRequest();
    request.open('GET', '/deleteuser', false);
    request.send(null);
    if (request.status === 200) {
        var h = request.responseText;
        alert(h);
    }
    else {
        alert('get error');
    }
}
function test() {
    var line = editor.getCursorPosition();
    var text = editor.getSelection().doc.$lines[line.row].substring(0,line.column);
    text = text.split(' ');
    text = text[text.length - 1];
    alert(text); 
}

function doc_select(select_value) {
    alert(select_value);
}
function mode_select(select_value) {
    var editor = ace.edit("editor");
    editor.getSession().setMode("ace/mode/" + select_value);
}
function split_select(select_value) {
    alert(select_value);
}
function theme_select(select_value) {
    var editor = ace.edit("editor");
    editor.setTheme(select_value);
}
function fontsize_select(select_value) {
    document.getElementById('editor').style.fontSize=select_value;
}
function keybinding_select(select_value) {
    var editor = ace.edit("editor");
    editor.setKeyboardHandler(select_value);
}

