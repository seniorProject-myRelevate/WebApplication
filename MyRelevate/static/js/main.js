/* Created by Jeremy on 10/21/2015. */

var contributorsDiv = document.getElementById('profiles');
var requestAccessDiv = document.getElementById('requestAccess');
var registrationBtn = document.getElementById('registration');
var requestBtn = document.getElementById('request');

var closeBtn = document.getElementById('close_message');

function validate_email(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function subscribe_validate() {
    var textbox = $('#subscription-inputs');
    var isValid = validate_email($('#id_email').val());

    if (isValid) {
        textbox.removeClass('has-error');
        textbox.addClass('has-success');
        $('#id_email').popover('hide')
    }
    else {
        textbox.removeClass('has-success');
        textbox.addClass('has-error');
        $('#id_email').popover('show')
    }
    return isValid;
}

function post_data() {
    if (subscribe_validate()) {
        $.ajax({
            url: form.attr('action'), // the endpoint
            type: "POST", // http method
            data: {the_post: $('#id_email').val()}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#invalid_email').hide();
                $('#id_email').val(''); // remove the value from the input
                $('#welcomeModal').modal('show'); //shows the modal
            }
        });
    }
    else {
        $('#invalid_email').show();
    }
}

$('#id_email').blur(function () {
    subscribe_validate()
});

$("#form-subscribe").submit(function (event) {
    event.preventDefault();
    subscribe_validate()
});

function ContributorAccess() {
    contributorsDiv.style.display = 'none';
    requestAccessDiv.style.display = 'block';
    requestBtn.onclick = function () {
    }
}