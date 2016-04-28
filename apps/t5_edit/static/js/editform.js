var formOptions = {
    url: ajax_save_url,
    beforeSubmit: function(arr, form, options) {
        window.scrollTo(0, 0);
        $('.alert-success').hide()
        $('.alert.alert-info').show()
        $(form).find('input,textarea').prop('disabled', true);
    },
    success: function(responseText, statusText, xhr, form){
        setTimeout(function(){
            $('.alert.alert-info').hide();
            $(form).find('input,textarea').removeAttr("disabled");  
            if (responseText['success']){
                $('.alert-success').show();
            } else {
                $('#personForm').html(responseText['form_html']);  
            };
        }, 500);                                
    }
};
$('#personForm').ajaxForm(formOptions);
