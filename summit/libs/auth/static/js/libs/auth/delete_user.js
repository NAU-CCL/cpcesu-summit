var delete_user = function(userID){
  console.log(userID);
  if (confirm('Are you sure you want to delete this user? This action cannot be undone!')) {
      $.ajax({
          type: "POST",
          url: '/accounts/delete_user/',
          data: {"userID": userID},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}