function ajax_all(url,form_id,data_id) {
	$("#"+form_id).submit(function(event){event.preventDefault();
	var  form = $('form#'+form_id);
	$.ajax({
                type:"GET",
                url:"/"+url+"/",
		data:form.serialize(),
		success:function(data){
			$('#'+data_id).html(data);}});});}

function ajax_film(url,pk){
     $.get(("/"+url+"/"+pk+"/"),
	function(data){
	$("#ajax").html(data);}); 
}

function ajax_film1(url){
     $.get(("/"+url+"/"),
	function(data){
	$("#ajax").html(data);}); 
}

function ajax_film_all(){
     $.get(("/"),
	function(data){
	$("#ajax").html(data);}); 
}
