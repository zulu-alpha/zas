/*
* Open the drawer when the menu icon is clicked.
* This is borrowed from the Udacity UD893 Course
*/
var menu = document.querySelector('#menu');
var header = document.querySelector('header');
var main = document.querySelector('main');
var footer = document.querySelector('footer');
var drawer = document.querySelector('#drawer');

menu.addEventListener('click', function(e) {
    drawer.classList.toggle('open');
    e.stopPropagation();
});

header.addEventListener('click', function() {
    drawer.classList.remove('open');
});

main.addEventListener('click', function() {
    drawer.classList.remove('open');
});

footer.addEventListener('click', function() {
    drawer.classList.remove('open');
});