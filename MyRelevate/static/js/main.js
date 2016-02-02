var requestBtn = document.getElementById('request');
var emailInput = $('#id_email');

function validate_email(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function subscribe_validate() {
    var textbox = $('#subscription-inputs');
    var isValid = validate_email(emailInput.val());

    if (isValid) {
        textbox.removeClass('has-error');
        textbox.addClass('has-success');
        emailInput.popover('destroy');
    }
    else {
        textbox.removeClass('has-success');
        textbox.addClass('has-error');
        emailInput.popover('show');
    }
    return isValid;
}

function post_data() {
    if (validate_email(emailInput.val())) {
        $.ajax({
            url: $("#form-subscribe").attr('action'),
            type: "POST", // http method
            data: {the_post: emailInput.val()}, // data sent with the post request

            // handle a successful response
            success: function (json) {
                $('#form-subscribe').hide();
                $('#subscribe-success').removeClass('hidden').fadeIn();
                //$('#welcomeModal').modal('show');
            },
            error: function () {
            }
        });
    }
}

emailInput.blur(function () {
    subscribe_validate()
});

emailInput.focus(function () {
    emailInput.popover('destroy');
});

$("#form-subscribe").submit(function (event) {
    event.preventDefault();
    subscribe_validate();
    post_data();
});


function ContributorAccess() {
    $('#profiles').hide();
    $('#requestAccess').show();
    requestBtn.onclick = function () {
    }
}
