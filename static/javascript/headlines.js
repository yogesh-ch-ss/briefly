$(document).ready(function() {
  $('.button.save').on('click', function(event) {
      event.preventDefault();   
      const savedArticlesDiv = $('.saved-articles');
      var parentDiv = $(this).closest('.headlines--category--titles');
      var articleId = $(this).attr('id');
      var userId = $(this).attr('data-user-id');
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

      if (parentDiv.length) {
          parentDiv.fadeOut(1000, function() {
              parentDiv.remove();
              parentDiv.find('.button.save').remove();
              savedArticlesDiv.append(parentDiv);
              parentDiv.fadeIn(1000);
          });
      }

      $.ajax({
          url: '/save_article',
          type: 'POST',
          data: {
              article_id: articleId,
              user_id: userId
          },
          headers: {
              "X-CSRFToken": csrfToken
          },
          success: function(response) {
              console.log('Article saved successfully:', response);
          },
          error: function(xhr, status, error) {
              console.error('Error saving article:', error);
          }
      });

  });
});