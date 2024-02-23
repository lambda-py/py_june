function toggleForm(object) {
  if (object.style.display === "block") {
    object.style.display = "none";
  } else {
    object.style.display = "block"
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Toggle post comment form
  let replyPostButton = document.getElementById("reply-post-btn");
  replyPostButton.addEventListener("click", function () {
    let postCommentForm = document.getElementById("post-comment-form");
    toggleForm(postCommentForm);
  });

  // Move reply comment form to comment
  // There's no need to toggle the form, it's at the bottom by default.
  let replyCommentButtons = document.querySelectorAll(".reply-comment-btn");
  let replyCommentForm = document.getElementById("reply-comment-form");

  replyCommentButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      let comment = button.closest(".comment")
      // Move form after comment
      comment.after(replyCommentForm);

      // Add comment text to form input
      // Second instance is the reply comment form
      const editor = CKEDITOR.instances[2];

      // Get comment content from button
      // Perhaps there is better to get content from comment
      const commentContent = this.getAttribute('data-comment-content');

      // Wait for the 'instanceReady' event before setting data
      // It was a nightmare to figure out how to do this!!!
      editor.on('instanceReady', function () {
        this.setData(`<blockquote>${commentContent}</blockquote><br>`);
      });
    });
  });

  let editPostBtn = document.getElementById("editPostBtn");
  let editPostForm = document.getElementById("editPostForm");
  let deletePostForm = document.getElementById("deletePostForm");
  let deletePostBtn = document.getElementById("deletePostBtn");
  let postDetail = document.getElementById("postDetail");
  let editCommentButtons = document.querySelectorAll(".edit-comment-btn");
  let editCommentForm = document.getElementById("edit-comment-form");


  editPostBtn.addEventListener("click", function (){
    if (editPostForm.style.display === "none"){
      editPostForm.style.display = "block";
      postDetail.style.display = "none";
      deletePostForm.style.display = "none";
    } else {
      editPostForm.style.display = "none";
      postDetail.style.display = "block";
      deletePostForm.style.display = "none";
    }
  });

  deletePostBtn.addEventListener("click", function () {
    if (deletePostForm.style.display === "none"){
      deletePostForm.style.display = "block";
      postDetail.style.display = "none";
      editPostForm.style.display = "none";
    } else {
      editPostForm.style.display = "none";
      postDetail.style.display = "block";
      deletePostForm.style.display = "none";
    }
  });

  let commentTextContent = "";

  editCommentButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      if (editCommentForm.style.display === "none") {
        editCommentForm.style.display = "block";
      } else {
        editCommentForm.style.display = "none";
      }

      let hiddenField = editCommentForm.querySelector("input[name='comment-id']");
      let comment = button.closest(".comment");
      let commentText = comment.querySelector(".comment-text");

      if (commentText.querySelector("#edit-comment-form") !== null) {
        commentText.innerHTML = commentTextContent;
        commentTextContent = "";
      } else {
        commentTextContent = commentText.innerHTML;
        commentText.innerHTML = "";
        commentText.appendChild(editCommentForm);

        const editor = CKEDITOR.instances[5];
        const commentEditContent = this.getAttribute("data-comment-edit-content");

        hiddenField.value = this.getAttribute("data-comment-id");

        editor.on('instanceReady', function () {
        this.setData(`${commentEditContent}`);
        });
      }
    });
  });
})
