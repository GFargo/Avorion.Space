/*
 * Main Javascript Ready Function
 */

(function($){
	$(function(){

    // custom parallax
    $(window).scroll(function() {
      var top = $(window).scrollTop();
      var width = $(window).width();
      var bottom = top + $(window).height();
      if (width > 768) {
        $("img.background").css({top: -1 * Math.abs(top / 2)});
      }
      else {
        if (top > $(".section.welcome").height()) { $(".section.welcome").css("visibility", "hidden"); }
        else { $(".section.welcome").css("visibility", "visible"); }
      }

      $(".parallax").each(function() {
        if ((bottom > $(this).offset().top) && (width > 768)) {
          if ($(this).offset().top > top ) {
            var parallax = (Math.abs(top - $(this).offset().top) / 2);
          }
          else {
            var parallax = ($(this).offset().top - top) / 2;
          }
          $(this).css("backgroundPosition", ("0px " + (parseInt(parallax)).toString() + "px"));
        }
        else {
          $(this).css("backgroundPosition", "0px 0px");
        }
      });
    });

    // Smooth Scrolling
    $("a.navbar-brand[href^='#'], ul.nav li a[href^='#'], a.scroll-down").click(function(e) {
       e.preventDefault();
       $('html, body').animate({ scrollTop: $(this.hash).offset().top }, 400);
    });

    // Small Navbar closes Open toggle menus
    $("ul.nav li a[href^='#']").click(function () {
      $(".navbar-collapse.in").collapse('hide');
    });

	}); // end of document ready
})(jQuery); // end of jQuery name space