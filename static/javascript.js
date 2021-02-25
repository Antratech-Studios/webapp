$(document).ready(function(){
	$('#burger-container').click(function(){
		$(this).toggleClass('open');
		$('#menu').toggle()
		$('.navbar-brand').toggle()
	});

});

