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
  let deleteCommentButtons = document.querySelectorAll(".delete-comment-btn");
  let deleteCommentForm = document.querySelectorAll(".delete-comment-form");

// Edit post button form
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
//Edit comment buttons
  let commentTextContent = "";
  let currentEditButton = null;

  editCommentButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      if (editCommentForm.style.display === "none") {
        editCommentForm.style.display = "block";
      }
      let comment = button.closest(".comment");
      let commentText = comment.querySelector(".comment-text");

      if (currentEditButton !== button) {
        if (currentEditButton) {
          let previousComment = currerntEditButton.closest(".comment");
          let previousCommentText = previousComment.querySelector(".comment-text");
          let editForm = previousCommentText.querySelector("#edit-comment-form");

          if (editForm) {
            previousCommentText.innerHTML = commentTextContent;
          }
        }

        currentEditButton = button;

        let hiddenField = editCommentForm.querySelector("input[name='comment-id']");


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
      } else {
        let editForm = commentText.querySelector("#edit-comment-form");
        if (editForm) {
          commentText.innerHTML = commentTextContent;
          currentEditButton = null;
        }
      }
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

      reversToggleForm(commentContainer);
      toggleForm(form);

      cancelButton.clickHandler = cancelHandler(cancelButton, form, commentContainer);
      cancelButton.addEventListener("click", cancelButton.clickHandler);
    });
  });
  // Notification about actions was completed successfully
  let messageBlock = document.getElementById("notification-messages");
  messageBlock.style.display = "block";
  setTimeout(function () {
    messageBlock.style.display = "none";
  }, 10000);
})
