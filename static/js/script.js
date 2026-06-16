// static/js/script.js

// Example JavaScript for ML Projects Website

// Run this function when the document is ready
$(document).ready(function() {
  // Example: Add active class to nav item based on current URL
  var currentLocation = window.location.href;
  $('.navbar-nav .nav-item .nav-link').each(function() {
      if ($(this).attr('href') === currentLocation) {
          $(this).addClass('active');
      }
  });

  // Example: Show an alert when clicking a button
  $('.btn').click(function() {
      alert('Button clicked!');
  });

  // You can add more JavaScript/jQuery functionality here
});








// static/js/script.js

// Example: Toggle navbar menu on mobile
const navbarMenu = document.querySelector('.navbar-menu');
const navbarToggle = document.querySelector('.navbar-toggle');

navbarToggle.addEventListener('click', () => {
    navbarMenu.classList.toggle('open');
});

