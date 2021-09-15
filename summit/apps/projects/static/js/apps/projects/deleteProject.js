var deleteProject = function(){
  var confirmation = confirm('Are you sure you want to archive this project? You will not be able to find it in search results!');
  if (confirmation) {
    console.log("deleteProject")
    console.log(document.getElementById("id_status").value)
    document.getElementById("id_status").value = "ARCHIVED"
    document.getElementById("projectForm").submit()
  }
  
}

$('#deleteButton').on('click', deleteProject)