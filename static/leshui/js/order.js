$(function(){

$('.order_left ul li').eq(0).addClass('order_li_hover');
$('#order_right > div').eq(0).show();
$('.order_left').find('li').each(function(){
	$(this).click(function(){
		$(this).addClass('order_li_hover').siblings().removeClass('order_li_hover');
		$(this).addClass('order_li_hover').parent().siblings().find('li').removeClass('order_li_hover');	
	});
});


$('#cent_dd li').click(function(){
	var Oindex=$(this).index();
	$('.center_dd').show();
	$('.zc_main').hide();
	$('.adrees_main').hide();
	
	$('#order_right > div').eq(Oindex).show().siblings().hide();
});
$('#cent_pep li').click(function(){
	var Pindex=$(this).index();
	$('.center_dd').hide();
	$('.center_peple > div').eq(Pindex).show().siblings().hide();
});




// 预定后下一步
$('.next_day > div').each(function(){
	$(this).click(function(){
		$(this).addClass('next_true_yes').siblings().removeClass('next_true_yes');

		if( $(this).hasClass('next_true2') ){
			$('.next_em').show();
		}else{
			$('.next_em').hide();
		}
	});
});

	




});