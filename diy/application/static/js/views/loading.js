
onmessage = function(event) {
    if (event.data == 'loading') {
        loading_dlg();
    }
    else if (event.data == 'end_loading') {
        end_loading_dlg();
    }
}

var loading_dlg = function(){
    self.document.getElementById('loading_dlg').style.display = 'block';
    self.document.getElementById('loading_back').style.display = 'block';
}

var end_loading_dlg = function(){
    self.document.getElementById('loading_dlg').style.display = 'none';
    self.document.getElementById('loading_back').style.display = 'none';
}
