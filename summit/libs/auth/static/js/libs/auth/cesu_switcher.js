var change_cesu = function(cesu_id){
  $.ajax({
      type: "GET",
      url: '/projects/change_cesu',
      data: {'cesu_id': cesu_id},
      success: function(resp){
          window.location.href = "/projects/dashboard/";
          console.log(resp)
      }})
}