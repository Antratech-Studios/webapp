$(document).ready(function(){
	$('#burger-container').click(function(){
		$(this).toggleClass('open');
		$('#menu').toggle()
		$('.navbar-brand').toggle()

	});

	// Transitions  elements with the same class on hover
	$('.vert-banner').each(function (i,value) {
	$(this).hover( function (e) {
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

});

