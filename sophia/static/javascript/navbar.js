// document.addEventListener('DOMContentLoaded', function() {
//     var backButton = document.getElementById('backButton');
  
//     if (backButton) {
//       backButton.addEventListener('click', function() {
//         window.history.back();
//       });
//     }
//   });
  
document.addEventListener('DOMContentLoaded', function() {
  var backButton = document.getElementById('backButton');

  if (backButton) {
      backButton.addEventListener('click', function() {
          window.history.back();
          location.reload(); // Reload the page
      });
  }
});
