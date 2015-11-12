/* Created by Jeremy on 10/21/2015. */

var contributorsDiv = document.getElementById('profiles');
var requestAccessDiv = document.getElementById('requestAccess');
var registrationBtn = document.getElementById('registration');
var requestBtn = document.getElementById('request');
var subscribeDiv = document.getElementById('subscribe');
var welcomeDiv = document.getElementById('welcome');
var emailDiv = document.getElementById('id_email');
var email = document.getElementById('id_subscriptioninput');

email.addEventListener('click', Subscribe, true);

/*

 */
function ContributorAccess() {
    contributorsDiv.style.display = 'none';
    requestAccessDiv.style.display = 'block';
    requestBtn.onclick = function () {

    }
}

/*
 $("id_subscriptioninput").click(function(){
 window.location = "https://www.google.com";
 return false;
 });
 */

/*

 */
function Subscribe(event) {

    event.preventDefault();

    if (email.form.valueOf("")) {
        subscribeDiv.style.display = 'none';
        welcomeDiv.style.display = 'block';
    }
    else {

    }

    //window.location.replace("https://www.google.com");
    if (emailDiv.value === "") {
        //subscribeDiv.style.display = 'none';
        //welcomeDiv.style.display = 'block';
    }
    else {
        //window.location = "https://www.google.com"
        //subscribeDiv.style.display = 'none';
        //welcomeDiv.style.display = 'block';
    }


    //window.location.replace("https://www.google.com");
    //window.location = "https://www.google.com";
    //console.log('here');
    /*
     if ($("input").val()!= ""){
     subscribeDiv.style.display = 'none';
     welcomeDiv.style.display = 'block';
     window.location = "/subscribe"
     }
     else{

     }
     */
}