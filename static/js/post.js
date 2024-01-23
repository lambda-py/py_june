document.addEventListener("DOMContentLoaded", function (){
    let replyButton = document.getElementById("replyBtn");
    replyButton.addEventListener("click", function (){
        let commentForm = document.getElementById("commentForm");
        if (commentForm.style.display === "block") {
            commentForm.style.display = "none";
        } else {
            commentForm.style.display = "block";
        }
    });
});


document.addEventListener("DOMContentLoaded", function (){
    let answerButton = document.querySelectorAll(".answerBtn");

    answerButton.forEach(function (button){
        button.addEventListener("click", function (){
        let comment = button.closest(".comment")
        let answerForm = comment.querySelector(".answerForm");

        if (answerForm.style.display === "block") {
            answerForm.style.display = "none";
        } else {
            answerForm.style.display = "block";
        }
        });
    });
});