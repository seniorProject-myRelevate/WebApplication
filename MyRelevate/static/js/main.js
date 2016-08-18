var emailInput = $('#id_email');

function validateEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

function subscribeValidate() {
    var textbox = $('#subscription-inputs');
    var isValid = validateEmail(emailInput.val());

    if (isValid) {
        emailInput.removeClass('uk-form-danger');
        emailInput.addClass('uk-form-success');
    }
    else {
        emailInput.removeClass('uk-form-success');
        emailInput.addClass('uk-form-danger');
    }
    return isValid;
}

function postData() {
    if (validateEmail(emailInput.val())) {
        var textbox = $('#subscription-inputs');
        $.ajax({
            url: $("#form-subscribe").attr('action'),
            type: "POST", // http method
            dataType: "json",
            data: {email: emailInput.val()}, // data sent with the post request

            // handle a successful response
            success: function (data) {
                console.log(data);
                emailInput.removeClass('uk-form-danger');
                emailInput.addClass('uk-form-success');
                addMessage('success', data['message']);
            },
            error: function (data) {
                emailInput.removeClass('uk-form-success');
                emailInput.addClass('uk-form-danger');
                addMessage('danger', data.responseJSON.message);
            }
        });
    }
}

emailInput.blur(function () {
    subscribeValidate()
});

emailInput.focus(function () {
    emailInput.popover('destroy');
});

$("#form-subscribe").submit(function (event) {
    event.preventDefault();
    subscribeValidate();
    postData();
});


function ContributorSearch() {
    $('#allContributors').hide();
    $('#searchedContributors').show();
}

$(document).ready(function () {
    $('.dropdown').hover(
        function () {
            $(this).children('.sub-menu').slideDown(200);
        },
        function () {
            $(this).children('.sub-menu').slideUp(200);
        }
    );
}); // end ready

$('#editExpertise').click(function(){
    $('#topic_list').hide();
    $('#expertise_topic_form').show();
});

$('a').parent().hover(
  function () {
      if ($(this).children("ul") )
        $(this).children("ul").show();
  },
  function () {
    $(this).children("ul").hide();
  }
);

function addMessage(tag, message) {
    var str = "<div class=\"uk-alert uk-alert-" + tag + "\" data-uk-alert><a href=\"\" class=\"uk-alert-close uk-close\"></a> "
        + message + " </div>";

    $('#messages').append(str);
}

$('#myLink').click(function(){ addMessage('info', 'test'); return false; });

UIkit.offcanvas.show('#submenu');
UIkit.offcanvas.hide([force = false]);