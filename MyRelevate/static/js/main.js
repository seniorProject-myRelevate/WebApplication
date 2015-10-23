/* Created by Jeremy on 10/21/2015. */

function loadReq() {
    console.log('Javascript is working!!')
}

loadReq();

var loginDiv = document.getElementById('login');
var requestAccessDiv = document.getElementById('requestAccess');

var registrationBtn = document.getElementById('registration');
var requestBtn = document.getElementById('request');

registrationBtn.onclick = function () {
    loginDiv.style.display = 'none';
    requestAccessDiv.style.display = 'block';
}