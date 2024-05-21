(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space

// Button scroll to top
let button = document.getElementById("scrollToTopBtn");

window.onscroll = function (){
    showHideScrollTopBtn();
};
function showHideScrollTopBtn() {

    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        button.style.display = "block";
    } else {
        button.style.display = "none";
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

// Header search line processing
let searchResultsHeader = document.getElementById("search-results-header");
let searchResults = document.getElementById("search-results");
let searchInput = document.getElementById("search-input");
document.addEventListener("click", function (event) {

    if (event.target !== searchInput && !searchResultsHeader.contains(event.target)) {
        searchResults.style.display = "none";
    }
});

searchInput.addEventListener("click", function (event) {
    if (searchResults.style.display === "none") {
        searchResults.style.display = "";
    }
});

// Notification about actions was completed successfully
let messageBlock = document.getElementById("notification-messages");
if (messageBlock) {
    messageBlock.style.display = "block";
    setTimeout(function () {
        messageBlock.classList.add("notification-hidden");
        setTimeout(function () {
            messageBlock.style.display = "none";
            messageBlock.classList.remove("notification-hidden");
        }, 2000);
    }, 2000);
}