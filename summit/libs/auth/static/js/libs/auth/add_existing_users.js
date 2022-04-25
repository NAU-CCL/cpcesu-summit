var add_users = function(){
  var checkedBoxes = document.querySelectorAll('input[name=user_checkbox]:checked');
  var userIDs = [];
  for (let i = 0; i < checkedBoxes.length; i++){
    userIDs.push(checkedBoxes[i].value)
  }
  console.log(userIDs)

  $.ajax({
      type: "POST",
      url: '/accounts/add_users/',
      data: {'userIDs[]': userIDs},
      headers: {"X-CSRFToken":csrf_token},
      success: function(resp){
          window.location.href = "/accounts/all_users/";
          console.log(resp)
      }})
}