var delete_contact = function(contactID){
  console.log(contactID);
  if (confirm('Are you sure you want to delete this user? This action cannot be undone!')) {
      $.ajax({
          type: "POST",
          url: '/auth/delete_contact/',
          data: {"contactID": contactID},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}