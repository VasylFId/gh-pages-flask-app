document.addEventListener('DOMContentLoaded', function() {
    var password = document.getElementById("password");
    var confirm_password = document.getElementById("confirm_password");

    function validatePassword(){
        if(password.value !== confirm_password.value) {
            confirm_password.setCustomValidity("Passwords do not match.");
        } else {
            confirm_password.setCustomValidity('');
        }
    }

    password.addEventListener('change', validatePassword);
    confirm_password.addEventListener('keyup', validatePassword);
});
