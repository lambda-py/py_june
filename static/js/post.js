function toggleForm(object) {
  if (object.style.display === "block") {
    object.style.display = "none";
  } else {
    object.style.display = "block"
  }
}

function reversToggleForm(object) {
  if (object.style.display === "none") {
    object.style.display = "block";
  } else {
    object.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Toggle post comment form
  let replyPostButton = document.getElementById("reply-post-btn");
  if (replyPostButton) {
    replyPostButton.addEventListener("click", function () {
      let postCommentForm = document.getElementById("post-comment-form");
      toggleForm(postCommentForm);
    });
  }

  // Move reply comment form to comment
  // There's no need to toggle the form, it's at the bottom by default.
  let replyCommentButtons = document.querySelectorAll(".reply-comment-btn");
  let replyCommentForm = document.getElementById("reply-comment-form");


  replyCommentButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      let comment = button.closest(".comment")
      let commentContainer = comment.querySelector(".comment-text")
      let replyForm = comment.querySelector(".reply-form");

      replyForm.appendChild(replyCommentForm);
      hideAllForms();
      reversToggleForm(replyForm);

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
    })
  });


  let editPostBtn = document.getElementById("editPostBtn");
  let editPostForm = document.getElementById("editPostForm");
  let deletePostForm = document.getElementById("deletePostForm");
  let deletePostBtn = document.getElementById("deletePostBtn");
  let postDetail = document.getElementById("postDetail");
  let editCommentButtons = document.querySelectorAll(".edit-comment-btn");
  let editCommentForm = document.getElementById("edit-comment-form");
  let deleteCommentButtons = document.querySelectorAll(".delete-comment-btn");
  let deleteCommentForm = document.querySelectorAll(".delete-comment-form");

// Edit post button form
  if (editPostBtn && deletePostBtn) {
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
// Delete post button form
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
  }
  // Edit comment buttons
  // find all the edit buttons on the page
  editCommentButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      // we find the closest comment block to the button and find the comment text block in it
      let comment = button.closest(".comment");
      let commentText = comment.querySelector(".comment-text");
      let editForm = comment.querySelector(".comment-edit");

      editCommentForm.style.display = "table";
      editForm.appendChild(editCommentForm);
      hideAllForms();
      reversToggleForm(editForm);

      // we find a hidden field in the form for further storage of the comment id in it
      let hiddenField = editCommentForm.querySelector("input[name='comment-id']");

      // We take the instance of the editor, extract the content of the comment from the button
      const editor = CKEDITOR.instances[5];
      const commentEditContent = this.getAttribute("data-comment-edit-content");
      // We take the id of the comment from the button and assign it to the hidden field
      hiddenField.value = this.getAttribute("data-comment-id");
      // We insert the content from the button into the editor
      editor.on('instanceReady', function () {
          this.setData(`${commentEditContent}`);
      });
    });
  });
  // Handler for cancel buttons
  function cancelHandler(cancelButton, form, commentContainer) {
    return function () {
      reversToggleForm(form);
      toggleForm(commentContainer);
    };
  }
  // Delete buttons
  deleteCommentButtons.forEach(function (button, index) {
    button.addEventListener("click", function () {
      let form = deleteCommentForm[index];
      let hiddenField = form.querySelector("input[name='comment-id']");
      let comment = button.closest(".comment");
      let commentContainer = comment.querySelector(".comment-text");
      let cancelButton = form.querySelector(".cancel-btn");
      // Remove the listener for the button so that everything works when it is pressed repeatedly
      cancelButton.removeEventListener("click", cancelButton.clickHandler);

      hiddenField.value = button.getAttribute("data-comment-id");
      hideAllForms();
      reversToggleForm(commentContainer);
      toggleForm(form);

      cancelButton.clickHandler = cancelHandler(cancelButton, form, commentContainer);
      cancelButton.addEventListener("click", cancelButton.clickHandler);
    });
  });

  function hideAllForms() {
    let comments = document.querySelectorAll(".comment");

    comments.forEach(function (comment) {
      let textComment = comment.querySelector(".comment-text");
      let replyComment = comment.querySelector(".reply-form");
      let editComment = comment.querySelector(".comment-edit");
      let deleteComment = comment.querySelector(".delete-comment-form");

      if (deleteComment || replyComment || editComment) {
        deleteComment.style.display = "none";
        replyComment.style.display = "none";
        editComment.style.display = "none";
        textComment.style.display = "block";
      }
    });
  }
})
