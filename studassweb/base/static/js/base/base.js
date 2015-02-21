$("div[data-toggle=hide]").click(function(event) {
    var button = event.target;
    var target_class = button.getAttribute("data-target");
    $(button).toggleClass("active");
    $("." + target_class).toggleClass("hidden");
});