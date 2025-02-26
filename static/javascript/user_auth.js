document.addEventListener('DOMContentLoaded', function() {
    const logoutForm = document.getElementById('user-logout');
    const deleteAccountForm = document.getElementById('user-account-delete');

    if (logoutForm) {
        logoutForm.onsubmit = function() {
            return confirm('Are you sure you want to logout?');
        };
    }

    if (deleteAccountForm) {
        deleteAccountForm.onsubmit = function() {
            return confirm('Are you sure you want to delete your account?');
        };
    }
});