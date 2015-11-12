/* Created by Jeremy on 10/21/2015. */

var contributorsDiv = document.getElementById('profiles');
var requestAccessDiv = document.getElementById('requestAccess');
var registrationBtn = document.getElementById('registration');
var requestBtn = document.getElementById('request');
var subscribeDiv = document.getElementById('subscribe');
var welcomeDiv = document.getElementById('welcome');
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

 */
function Subscribe(event) {

    event.preventDefault();

    if (email.form.valueOf("")) {
        subscribeDiv.style.display = 'none';
        welcomeDiv.style.display = 'block';
    }
    else {

    }
}