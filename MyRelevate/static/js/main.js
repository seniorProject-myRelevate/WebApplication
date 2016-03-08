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
                $('#welcomeModal').modal('show');
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
    //event.preventDefault();
    //subscribe_validate();
    //post_data();
});

function ContributorAccess() {
    $('#profiles').hide();
    $('#requestAccess').show();

    $("form select[name='credential']").change(function(){
        var credentialVal = $("form select[name='credential']").val();
        if(credentialVal == "SU" || credentialVal == "SM"){
            $('#studentAccess').show();
        }
        else {
            $('#id_email').val('');
            $('#id_first_name').val('');
            $('#id_last_name').val('');
            $('#studentAccess').hide();
        }
    });

    requestBtn.onclick = function () {
    }
}

function ViewProfile() {
    $('#viewContent').hide();
    $('#createPost').hide();
    $('#contributorProfile').show();

    if($('#interests-paragraph').val() == ""){
        $('#interests-paragraph').hide();
        $('#interestsForm').show();
    }

    /*
    $('#editInterests').onclick = function() {
        //$('#interests-paragraph').hide();
        //$('#interestsForm').show();
    }
    */
}

function ViewContent() {
    $('#contributorProfile').hide();
    $('#viewResources').hide();
    $('#createPost').hide();
    $('#viewContent').show();
}

function ViewResources() {
    $('#contributorProfile').hide();
    $('#viewContent').hide();
    $('#createPost').hide();
    $('#viewResources').show();
}

function CreatePost() {
    $('#contributorProfile').hide();
    $('#viewContent').hide();
    $('#viewResources').hide();
    $('#createPost').show();
}

function EditInterests() {
    $('#interests-paragraph').hide();
    $('#interestsForm').show();
}

function EditBiography() {
    $('#biography-paragraph').hide();
    $('#biographyForm').show();
}

$('a').parent().hover(
  function () {
      if ($(this).children("ul") )
        $(this).children("ul").show();
  },
  function () {
    $(this).children("ul").hide();
  }
);