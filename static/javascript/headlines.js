$(document).ready(function() {
  $('.button.save').on('click', function(event) {
    console.log("Save button clicked");
    event.preventDefault();
    const headlineDiv = $(this).closest('.headlines--category--titles');
    const savedArticlesDiv = $('.saved-articles');
    if (headlineDiv.length && savedArticlesDiv.length) {
      headlineDiv.fadeOut(1000, function() {
      event.target.remove();
      savedArticlesDiv.append(headlineDiv);
      headlineDiv.fadeIn(1000);
      });
    }
    
    const articleId = $(this).data('id');
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
    console.log("csrf:", csrfToken);
    const username = $('meta[name="username"]').attr('content');

    console.log("Username:", username);
    $.ajax({
      url: '/save_article',
      type: 'POST',
      data: { id: articleId },
      headers: {
      'X-CSRF-Token': csrfToken
      },
      success: function(response) {
      console.log("Article saved successfully:", response);
      },
      error: function(error) {
      console.error("Error saving article:", error);
      }
    });
  });
});
