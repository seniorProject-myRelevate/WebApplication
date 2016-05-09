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

$('#contributorPage').click(function () {
    ContributorAccess();
    return false;
});

$("form select[name='credential']").change(function(){
        var credentialVal = $("form select[name='credential']").val();
        var email = $('#id_adviser_email');
        var firstName = $('#id_adviser_first_name');
        var lastName = $('#id_adviser_last_name');
        if(credentialVal == "SU" || credentialVal == "SM"){
            $('#studentAccess').show();
        }
        else {
            email.val('');
            firstName.val('');
            lastName.val('');
            $('#studentAccess').hide();
        }
    });

/*
 Remove selected topic from option list and add it to selected list
*/
//$('#add_right_arrow').click(function(){

//    $("form select[name='expertise_topics']").selected().each(function(){
//        $('#id_my_topics').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
//        $(this).remove();
//    });

    /*
   $('#id_expertise_topics option:selected').each(function(){
       $('#id_my_topics').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
       $(this).remove();
       */
       /*
       $('#id_selected_topics').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
       $(this).remove();
       */
   //});
//});

/*
 Remove selected topic from select list and add it back to the options list
*/
//$('#remove_left_arrow').click(function(){
//    $('#id_my_topics option:selected').each(function(){
//        $('#id_expertise_topics').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
//        $(this).remove();
//   });
    /*
    $('#id_selected_topics option:selected').each(function(){
        $('#id_expertise_topics').append("<option value='"+$(this).val()+"'>"+$(this).text()+"</option>");
        $(this).remove();
   });
   */
//});


function ContributorAccess() {
    //$('#profiles').hide();
    //$('#contributorApplication').show();

    $("form select[name='credential']").change(function(){
        var credentialVal = $("form select[name='credential']").val();
        var email = $('#id_adviser_email');
        var firstName = $('#id_adviser_first_name');
        var lastName = $('#id_adviser_last_name');
        if(credentialVal == "SU" || credentialVal == "SM"){
            $('#studentAccess').show();
        }
        else {
            email.val('');
            firstName.val('');
            lastName.val('');
            $('#studentAccess').hide();
        }
    });
}

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
function ViewProfile() {
    $('#viewContent').hide();
    $('#createPost').hide();
    $('#contributorProfile').show();

    if($('#id_interests').val() == ""){
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

$('#editExpertise').click(function(){
    $('#topic_list').hide();
    $('#expertise_topic_form').show();
});

function EditBiography() {
    $('#biography-paragraph').hide();
    $('#biographyForm').show();
}

function EditInterests() {
    $('#interests-paragraph').hide();
    $('#interestsForm').show();
}

function EditContactInformation() {
    $('#contact_list').hide();
    $('#contactInfoForm').show();
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

function addMessage(tag, message) {
    var str = "<div class=\"uk-alert uk-alert-" + tag + "\" data-uk-alert><a href=\"\" class=\"uk-alert-close uk-close\"></a> "
        + message + " </div>";

    $('#messages').append(str);
}

$('#myLink').click(function(){ addMessage('info', 'test'); return false; });

UIkit.offcanvas.show('#submenu');
UIkit.offcanvas.hide([force = false]);
