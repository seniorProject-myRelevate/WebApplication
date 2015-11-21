/* Created by Jeremy on 10/21/2015. */

var contributorsDiv = document.getElementById('profiles');
var requestAccessDiv = document.getElementById('requestAccess');
var registrationBtn = document.getElementById('registration');
var requestBtn = document.getElementById('request');


$(function () {
    var email = document.getElementById('id_subscriptioninput');
    var form = $('#the-form');
    var closeBtn = document.getElementById('close_message');
    email.addEventListener('click', Subscribe, false);

    function Subscribe(event) {
        event.preventDefault();
        CreatPost();
    }

    // AJAX for posting
    function CreatPost() {

        if (validateEmail($('#id_email').val())) {
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

    function validateEmail(checkEmail) {
        var re = /\S+@\S+\.\S+/;
        return re.test(checkEmail);
    }
});




/*

 */
function ContributorAccess() {
    contributorsDiv.style.display = 'none';
    requestAccessDiv.style.display = 'block';
    requestBtn.onclick = function () {

    }
}


/*
 This function gets cookie with a given name
 code came from https://realpython.com/blog/python/django-and-ajax-form-submissions/
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
 The functions below will create a header with csrftoken
 code came from https://realpython.com/blog/python/django-and-ajax-form-submissions/
 */

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});