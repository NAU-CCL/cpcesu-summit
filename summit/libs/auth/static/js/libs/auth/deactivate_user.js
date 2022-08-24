var deactivate = function(userID){
  console.log(userID);
  if (confirm('Are you sure you want to deactivate this user?')) {
      $.ajax({
          type: "POST",
          url: '/accounts/deactivate_user/',
          data: {"userID": userID, "reactivate": false},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}

var reactivate = function(userID){
  console.log(userID);
  if (confirm('Are you sure you want to reactivate this user?')) {
      $.ajax({
          type: "POST",
          url: '/accounts/deactivate_user/',
          data: {"userID": userID, "reactivate": true},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}