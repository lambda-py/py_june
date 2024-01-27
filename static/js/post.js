function toggleForm(object) {
  if (object.style.display === "block") {
    object.style.display = "none";
  } else {
    object.style.display = "block"
  }
}

document.addEventListener("DOMContentLoaded", function () {
  let replyButton = document.getElementById("reply-post-btn");
  replyButton.addEventListener("click", function () {
    let postCommentForm = document.getElementById("post-comment-form");
    toggleForm(postCommentForm);
  });
});
