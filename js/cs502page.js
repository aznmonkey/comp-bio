$(document).ready(function(){
    $(".nav-pills a").click(function(){
        $(this).tab('show');
    });
});

var url = document.location.toString(); // select current url shown in browser.
if (url.match('#')) {
    $('.nav-pills a[href=#' + url.split('#')[1] + ']').tab('show'); // activate current tab after reload page.
    }
    // Change hash for page-reload
    $('.nav-pills a').on('shown', function (e) { // this function call when we change tab.
        window.location.hash = e.target.hash; // to change hash location in url.
});