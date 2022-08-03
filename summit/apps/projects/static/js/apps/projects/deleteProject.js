var archive = function(proj_id){
  console.log(proj_id);
  if (confirm('Are you sure you want to archive this project? You will not be able to find it in search results!')) {
      $.ajax({
          type: "POST",
          url: '/projects/archive_project/',
          data: {"id": proj_id},
          headers: {"X-CSRFToken":csrf_token},
          success: function(resp){
              console.log(resp)
              window.location.reload(true)
          }
      })
  }
  
}
