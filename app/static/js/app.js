
let checkbox = document.getElementById('check');
checkbox.addEventListener('change', function() {
    let passwordField = document.getElementById('id_password');
    if (checkbox.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
});
