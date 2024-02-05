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
})


document.addEventListener("DOMContentLoaded", function() {
    let editPost = document.getElementById("editPost");
    let editPostBtn = document.getElementById("editPostBtn");
    let postContent = document.getElementById("postContent");
    let postDetailCon = document.getElementById("post-details");
    let postSlug = postDetailCon.getAttribute("data-post-slug");
    let deletePost = document.getElementById("deletePost");
    let deletePostBtn = document.getElementById("deletePostBtn");


    editPostBtn.addEventListener("click", function () {
        if (editPost.style.display === "none") {
            editPost.style.display = "block";
            postContent.style.display = "none";
            deletePost.style.display = "none";
            fetchEditForm();
        } else {
            editPost.style.display = "none";
            postContent.style.display = "block";
            deletePost.style.display = "none";
        }
    });

    deletePostBtn.addEventListener("click", function () {
        if (deletePost.style.display === "none") {
            deletePost.style.display = "block";
            editPost.style.display = "none";
            postContent.style.display = "none";
            fetchDeleteForm();
        } else {
            editPost.style.display = "none";
            postContent.style.display = "block";
            deletePost.style.display = "none";
        }
    });

    function fetchEditForm() {
        let url = "/posts/update/" + postSlug + "/";
        fetch(url, {
            method: "GET",
            headers: {
                "Content-type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            let formHtml = data.form_html;
            editPost.innerHTML = formHtml;

            document.getElementById("saveFormBtn").addEventListener("click", function (event) {
                event.preventDefault();
                let editData = new FormData(document.getElementById("editPostForm"));

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: editData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload()
                    }
                })
                .catch(error => {
                    console.error("Error sending form:", error);
                });
            });
        })
        .catch(error => {
            console.error("Error fetching form:", error);
        });
    }

    function fetchDeleteForm(){
        let url = "/posts/delete/" + postSlug + "/";
        fetch(url, {
            method: "GET",
            headers: {
                "Content-type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            let deleteformHtml = data.delete_html;
            deletePost.innerHTML = deleteformHtml;

            document.getElementById("saveDeleteFormBtn").addEventListener("click", function (event) {
                event.preventDefault();
                let deleteData = new FormData(document.getElementById("deletePostForm"));

                fetch(url, {
                    method: "POST",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    body: deleteData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = "/forum/"
                    }
                })
                .catch(error => {
                    console.error("Error fetching form:", error);
                });
            });

        })
        .catch(error => {
            console.error("Error fetching form:", error);
        });

    }


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
