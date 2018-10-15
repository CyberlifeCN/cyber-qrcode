$(function(){

$('.ht_hot_left_sc').click(function(){
	$('#sc1').hide();
	$('#sc2').show();
});

$('.ht_hot_left_say em').click(function(){
	$('.ht_hot_left_dl').css({'height':'auto'});
});


// 右侧tab效果
$('.ht_two_title ul li').eq(0).addClass('ht_title_hover');
$('.ht_two_bot_main').eq(0).show();
$('.ht_two_title ul li').each(function(){
	$(this).click(function(){
		var Hindex=$(this).index();
		$(this).addClass('ht_title_hover').siblings().removeClass('ht_title_hover');
		$('.ht_two_bot > div').eq(Hindex).show().siblings().hide();
	});

});

	
});