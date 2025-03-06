$(document).ready(function() {
    $('.remove-saved-article').on('click', function(event) {
        event.preventDefault();
        var parentDiv = $(this).closest('.headlines--category--titles');
        if (parentDiv.length) {
            parentDiv.css({
                'opacity': '0',
                'transition': 'opacity 0.5s, transform 0.5s',
                'transform': 'translateX(-100%)'
            });
            setTimeout(function() {
                parentDiv.remove();
            }, 500);
        }
    });
});