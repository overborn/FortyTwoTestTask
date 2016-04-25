$(function(){
	var NEW_REQUESTS = 0,
		FOCUSED = true;
	setInterval(function(){
	    $.ajax({
	    	url: "/ajax_requests",
	    	data: {'order': $('[name="order"]:checked').val()},
	    	success: function(data){
		        $( data['requests'].reverse() ).each(function(index){
		        	if ( $("input:hidden[value=" + this.id + "]").length > 0){
		        		return true
		        	} else {
		        		NEW_REQUESTS += 1;
		        	};
		        });
		        $('.requests').empty();
				$( data['requests'].reverse() ).each(function(index){
					$('.requests').append(
		        			"<p> " + (index + 1) + ". " + this.string + "</p>" + 
		        			"<input type='hidden' value='" + this.id + "'/>"
		        		);
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
		        	$('title').text('Last requests');
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
	$('[name="order"]').on('change', function(){
		$.ajax({
			url: "/ajax_requests",
	    	data: {'order': $('[name="order"]:checked').val()},
	    	success: function(data){
				NEW_REQUESTS = 0;
				FOCUSED = true;
				$('.requests').empty();
				$( data['requests'] ).each(function(index){
					$('.requests').append(
		        			"<p> " + (index + 1) + ". " + this.string + "</p>" + 
		        			"<input type='hidden' value='" + this.id + "'/>"
		        		);
				});
	    	},
	    	dataType: "json"
	    });
	});
})