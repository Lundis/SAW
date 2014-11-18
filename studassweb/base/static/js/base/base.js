//Pushes content below navbar
$(document).ready(function(){
    $(document.body).css('padding-top', $('#topnavbar').height() + 10);
    $(window).resize(function(){
        $(document.body).css('padding-top', $('#topnavbar').height() + 10);
    });
});
