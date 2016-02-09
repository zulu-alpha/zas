/*
* Open the drawer when the menu icon is clicked.
* This is borrowed from the Udacity UD893 Course
*/
var menu = document.querySelector('#ham-menu');
var content = document.querySelector('#content');
var drawer = document.querySelector('#drawer');

menu.addEventListener('click', function(e) {
    drawer.classList.toggle('open');
    e.stopPropagation();
});

content.addEventListener('click', function() {
    drawer.classList.remove('open');
});
