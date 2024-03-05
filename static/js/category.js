document.addEventListener("DOMContentLoaded", function () {

    let messageBlock = document.getElementById("notification-messages");
    console.log(messageBlock)
    messageBlock.style.display = "block";
    setTimeout(function () {
        messageBlock.style.display = "none";
    }, 10000);

})