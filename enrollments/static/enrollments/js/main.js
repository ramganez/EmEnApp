$(document).ready(function(){

    // your javascript here
    $('#id_date_of_birth').datetimepicker({
        format: 'YYYY-MM-DD'
    })

    $('#login-form').validator().on('submit', function (e) {

        if (e.isDefaultPrevented() === false) {
            submitForm($("#login-form").attr('action'), 'login-form');
        }
        return false;
    });

    $('#register-form').validator().on('submit', function (e) {
        if (e.isDefaultPrevented() === false) {
            submitForm($("#register-form").attr('action'), 'register-form');
        }
        return false;
    });

});


$(function() {

    $('#login-form-link').click(function(e) {

        $("#form_errors").hide();
        window.history.pushState("", "", '/signin/');

    	$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$('#register-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$('#register-form-link').click(function(e) {
        $("#form_errors").hide();
	    window.history.pushState("", "", '/register/');

		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$('#login-form-link').removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});

});



// this is the id of the form
function submitForm(ation_url, _id) {
    var url = ation_url;

    $.ajax({
           type: "POST",
           url: url,
           data: $("#"+_id).serialize(), // by default it pass csrf token
           success: function(data)
           {
                window.history.pushState("", "", data.profile_url);

                // replace container with user profile
                $(".container").html($(data.html).find('#first_inner_row').html());
                $("#form_errors").hide();

           },
           error: function(data)
           {
                // form validation error
                if (data.responseJSON.form_errors){
                    $("#form_errors").html(data.responseJSON.form_errors);
                }else{
                    // something went wrong
                    $("#form_errors").html('Something went wrong !');
                }

                $("#form_errors").show();
           }
         });

}

