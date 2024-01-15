$(document).ready(function () {
    $('.answer').click(function () {
      const comment = $(this).data('comment-text');
      const iframe = $('#answer-comment-form').contents().find('textarea')
      iframe.text(comment);

      // scroll to #answer-comment-form
      $('html, body').animate({
        scrollTop: $("#answer-comment-form").offset().top
      }, 500);
    });
  }
);
