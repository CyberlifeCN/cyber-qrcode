$(function(){

	// 手机版导航点击效果
	$('.ph_nav h1').click(function() {
		$(this).hide();
		$(this).parent().find('h2').show();
		$(this).parent().find('ul').show();
	});
	$('.ph_nav h2').click(function() {
		$(this).hide();
		$(this).parent().find('h1').show();
		$(this).parent().find('ul').hide();
	});


	$('.in_two_hot_right ul li:nth-child(2n)').css({'float':'right'});
	$('.in_active ul li:nth-child(2n)').css({'float':'right'});
	$('.in_news ul li:nth-child(2n)').css({'float':'right'});
	







});