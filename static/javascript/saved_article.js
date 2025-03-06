document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.remove-saved-article').forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var parentDiv = this.closest('.headlines--category--titles');
            if (parentDiv) {
                parentDiv.style.opacity = '0';
                parentDiv.style.transition = 'opacity 0.5s, transform 0.5s';
                parentDiv.style.transform = 'translateX(-100%)';
                
                setTimeout(function() {
                    parentDiv.remove();
                }, 500);
            }
        });
    });
});