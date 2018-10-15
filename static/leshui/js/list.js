$(function(){

	$('.er_choose_all > i').eq(0).addClass('er_hover');
	$('.er_choose_all > i').click(function(){
		$(this).addClass('er_hover').siblings().removeClass('er_hover');

	});

	
	$('.er_choose_all > p > i').click(function(){
		$(this).toggleClass('er_hover2').siblings().removeClass('er_hover2');
	});


	// 景点主题点击更多效果
	$('#zhuti_more').click(function(){
		$(this).find('span').css({'color':'#ff9913'});
		$('.zhuti_more').show();
	});
	$('.zhuti_more>i').click(function(){
		$(this).parent().hide();
		$('#zhuti_more').find('span').css({'color':'#666'});
	});

	$(document).bind('click',function(e){ 
	var e = e || window.event; //浏览器兼容性 
	var elem = e.target || e.srcElement; 
	while (elem) { //循环判断至跟节点，防止点击的是div子元素 
	if (elem.id && elem.id=='zhuti_more') { 
	return; 
	} 
	elem = elem.parentNode; 
	} 

	$('.zhuti_more').css('display','none'); //点击的不是div或其子元素 
	$('#zhuti_more').find('span').css({'color':'#666'});
	}); 


	$('.in_left_two a').click(function(){
		$(this).toggleClass('er_hover2').siblings().removeClass('er_hover2');
	});	

	$('.in_left_three a').click(function(){
		$(this).toggleClass('er_hover2').siblings().removeClass('er_hover2');
	});	


});