var unarchive = function(proj_id){
  console.log(proj_id);
  if (confirm("Do you really want to unarchive this project?")) {
      $.ajax({
          type: "POST",
          url: '/projects/unarchive_project/',
          data: {"id": proj_id},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}