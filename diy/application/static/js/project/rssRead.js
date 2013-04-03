var getrss_feed = function(){
    jQuery.getFeed({
        url: 'http://tech.163.com/special/000944OI/hulianwang.xml',
    success: function(feed) {
        alert(feed.title);
    }
    });
}

var getrss = function() {
    $.ajax({
            datatype: "xml",
            url: 'http://tech.163.com/special/000944OI/hulianwang.xml',
            Access-Control-Allow-Origin: *,
            success: function(data, status, xhr) {
                alert(data);
            }
    });
}
