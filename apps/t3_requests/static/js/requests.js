$(function(){
	var NEW_REQUESTS = 0,
		FOCUSED = true;
	setInterval(function(){
	    $.ajax({
	    	url: "/ajax_requests",
	    	success: function(data){
		        $( data['requests'].reverse() ).each(function(index){
		        	if ( $("input:hidden[value=" + this.id + "]").length > 0){
		        		return true
		        	} else {
		        		NEW_REQUESTS += 1;
		        		$('.requests').prepend(
		        			"<p> 1. " + this.string + "</p>" + 
		        			"<input type='hidden' value='" + this.id + "'/>"
		        		);
		        		$('p', '.requests').last().remove();
		        		$('input', '.requests').last().remove();
		        	};
		        });
		        $('p', '.requests').each(function(index){
		        	var text = $(this).text().replace(/^\d+/, index + 1);
		        	$(this).text(text);
		        });
		        var title = $('title').text();
		        if (NEW_REQUESTS && !FOCUSED) {
		        	if (title[0] != '('){
		        		title = '(' + NEW_REQUESTS + ') ' + title;
		        	} else {
		        		title = title.replace(/\(\d+\)/, '(' + NEW_REQUESTS + ')');
		        	};
		        	$('title').text(title);
		        } else {
		        	NEW_REQUESTS = 0;
		        };
		    },
		    dataType: "json"
		});
	}, 3000);
	$(window).focus(function(){
		$('title').text('Last requests');
		NEW_REQUESTS = 0;
		FOCUSED = true;
	}).blur(function(){
		FOCUSED = false;
	});
})