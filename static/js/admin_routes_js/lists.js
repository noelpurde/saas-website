document.addEventListener("DOMContentLoaded", function() {
    // Handle modal opening
    var editButtons = document.querySelectorAll('.edit-btn');
    editButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var modalId = this.getAttribute('data-target');
            var modal = document.querySelector(modalId);
            var nameInput = modal.querySelector('#name');
            var alertsInput = modal.querySelector('#alerts');
            var listId = this.getAttribute('data-list-id');
            var name = this.getAttribute('data-name');
            var alerts = this.getAttribute('data-alerts');

            nameInput.value = name;
            alertsInput.value = alerts;

            $(modal).modal('show');
        });
    });

    // Handle form submission
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            fetch('/lists_update', {
                method: 'POST',
                body: formData
            })
            .then(function(response) {
                if (response.ok) {
                    return response.text();
                }
                throw new Error('Network response was not ok.');
            })
            .then(function(data) {
                alert(data); // You can replace this with any UI feedback
                window.location.reload(); // Reload the page after successful update
            })
            .catch(function(error) {
                console.error('There was a problem with the fetch operation:', error);
                alert('Error while updating list');
            });
        });
    });
});