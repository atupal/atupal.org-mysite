
function display_rss(data) {
    //alert(JSON.stringify(data));
    //console.log(JSON.stringify(data));
    rss_container = $("#rss_container")[0];
    rss_container.remove();
    rss_container = document.createElement("div");
    rss_container.id = "rss_container";
    for (var i = 0; i < data.entries.length; ++ i) {
        div = document.createElement("div");
        div.class = "rss_container_div";
        div.id = "container_" + i.toString();

        h3 = document.createElement("h3");
        h3.innerHTML = data.entries[i].title;
        div.appendChild(h3);

        hr = document.createElement("hr");
        div.appendChild(hr);

        a = document.createElement("a");
        a.href = data.entries[i].link;
        a.innerHTML = "from:" + a.href
        div.appendChild(a);

        content = document.createElement("p");
        content.innerHTML = data.entries[i].content;
        div.appendChild(content);

        rss_container.appendChild(div);
    }
    $("#rss")[0].appendChild(rss_container);
}

function parserss(rssname, url, callback) {
    $("#rssname")[0].innerHTML = rssname;
    if (callback == undefined) {
        callback = display_rss;
    }
    $.ajax({
        //url: document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&callback=?&q=' + encodeURIComponent(url),
        url: 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&callback=?&q=' + encodeURIComponent(url),
        dataType: 'json',
        success: function(data) {
            callback(data.responseData.feed);
        },
    });
}

url = 'http://feed.feedsky.com/matrix67';
url = 'https://news.ycombinator.com/rss'
parserss("Hacker News", url, display_rss);
