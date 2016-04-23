var formOptions = {
	url: '/ajax_save/',
	beforeSubmit: function(arr, form, options) {
        $('.alert-success').hide()
        $('.alert.alert-info').show()
        $(form).find('input,textarea').prop('disabled', true);
	},
	success: function(responseText, statusText, xhr, form){
		$('.alert.alert-info').hide();
        $(form).find('input,textarea').removeAttr("disabled");  
    	if (responseText['success']){
    		$('.alert-success').show();
    	} else {
            $('#personForm').html(responseText['form_html']);  
        };          		    	
	}
};
$('#personForm').ajaxForm(formOptions);
