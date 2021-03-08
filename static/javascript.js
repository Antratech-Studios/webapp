$(document).ready(function () {
    $('#fullpage').fullpage()
    $('#burger-container').click(function () {
        $(this).toggleClass('open');
        $('#menu').toggle()
        $('.navbar-brand').toggle()

    });

    // Transitions  elements with the same class on hover
    $('.vert-banner').each(function (i, value) {
        $(this).hover(function (e) {
            $(this).children('.half-num').toggleClass('slide-right')
            e.preventDefault()
        })
    })

    // $('#text-1').on('mouseover',function () {
    //
    // 	$('#text-12').toggle()
    //
    //
    // })


    var scrollLink = $('.scroll');

  // Smooth scrolling
  scrollLink.click(function(e) {
    e.preventDefault();
    $('body,html').animate({
      scrollTop: $(this.hash).offset().top
    }, 250 );
  });

  // Active link switching
  $(window).scroll(function() {
    var scrollbarLocation = $(this).scrollTop();

    scrollLink.each(function() {

      var sectionOffset = $(this.hash).offset().top - 20;

      if ( sectionOffset <= scrollbarLocation ) {
        $(this).parent().addClass('active');
        $(this).parent().siblings().removeClass('active');
      }
    })

  })

});

