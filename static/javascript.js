$(document).ready(function(){
	$('#burger-container').click(function(){
		$(this).toggleClass('open');
		$('#menu').toggle()
		$('.navbar-brand').toggle()

	});
	$('.vert-banner .half-num').each( (i,value) => {
	$(this).hover(  (e) => {
		$(this).toggleClass('slide-right')})
	})

	// $('#text-1').on('mouseover',function () {
	//
	// 	$('#text-12').toggle()
	//
	//
	// })

});

