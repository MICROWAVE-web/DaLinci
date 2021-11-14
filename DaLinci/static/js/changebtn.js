$(document).ready(function() {
    const searchString = new URLSearchParams(window.location.search);
    const index = searchString.get('index');
    document.getElementById("buttons_list").children[0].children[index].classList.add("bg-gray-300");
});