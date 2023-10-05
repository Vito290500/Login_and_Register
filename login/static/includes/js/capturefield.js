$(document).ready(function() {
  $('#myLink').click(function(e) {
    e.preventDefault();  // Prevent the default link behavior
    
    var fieldValue = $('#myField').val();
    
    // Get the CSRF token from the cookie
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    
    // Make an AJAX request to send the field value to the server
    $.ajax({
      url: '/capture-value/',  // Update with the correct URL
      type: 'POST',
      data: {
        'field_value': fieldValue,
      },
      beforeSend: function(xhr) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      },
      success: function(response) {
        // Handle the success response if needed
        window.location.href = '/check_email/';
      },
      error: function(xhr, status, error) {
        // Handle the error if needed
        console.error('Error capturing value:', error);
      }
    });
  });
});