$("div[data-toggle=hide]").click(function(event) {
    var button = event.target;
    var target_class = button.getAttribute("data-target");
    $(button).toggleClass("active");
    $("." + target_class).toggleClass("hidden");
});

// This supposedly makes submenus clickable on touch devices
$(function(){
	$(".dropdown-menu > li > a.trigger").on("click",function(e){
		var current=$(this).next();
		var grandparent=$(this).parent().parent();
		if($(this).hasClass('left-caret')||$(this).hasClass('right-caret'))
			$(this).toggleClass('right-caret left-caret');
		grandparent.find('.left-caret').not(this).toggleClass('right-caret left-caret');
		grandparent.find(".sub-menu:visible").not(current).hide();
		current.toggle();
		e.stopPropagation();
	});
	$(".dropdown-menu > li > a:not(.trigger)").on("click",function(){
		var root=$(this).closest('.dropdown');
		root.find('.left-caret').toggleClass('right-caret left-caret');
		root.find('.sub-menu:visible').hide();
	});
});

// remove empty breadcrumbs
$(function() {
    var breadcrumbs = document.getElementsByClassName("breadcrumb");
    for (var i = 0; i < breadcrumbs.length; i++) {
        var text = breadcrumbs[i].innerHTML;
        if (text.trim() == "") {
            breadcrumbs[i].parentNode.removeChild(breadcrumbs[i]);
        }
    }
});