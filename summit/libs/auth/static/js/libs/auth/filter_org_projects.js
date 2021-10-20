function loadDetails(id){
  $(document.getElementsByClassName("clicked-background")).removeClass("clicked-background");
  $(document.getElementById(id)).addClass("clicked-background");

  let projects_name = document.getElementById("projects_name");
  
  let userID = id;
  $.ajax({
  type: "GET",
      url: '/accounts/info_display',
      data: {'userID': userID},
      success: function(resp){
          console.log(resp);
          table_2 = $('#table_2').DataTable()
          table_2.clear()
          
          $.each(user=resp['user'],function(index,user, orgs=resp['orgs'], projects=resp['projects']){
            projects_name.innerHTML = "Projects involving " + user.first_name + " " + user.last_name;
            console.log(projects);
            $.each(projects, function(index,project){
              if (project.status != 'ARCHIVED'){
                var userRole = "";
                if (project.pp_i_id == id) {
                  userRole = "PPI";
                }
                if (project.project_manager_id == id) {
                  userRole = "APM";
                }
                if (project.tech_rep_id == id) {
                  userRole = "AATR";
                }
                if (project.staff_member_id == id) {
                  userRole = "SM";
                }
                //let status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
                
                table_2.row.add([
                        '<a href="/projects/detail/' + project.id + '"/>' + project.project_title + '</a>', 
                        project.status,
                        userRole
                ]).draw()
              }
                
            })
      if($.fn.DataTable.isDataTable('#table_2')){
          table_2.destroy()
          $('#table_2').DataTable({
              retrieve: true,
              'ordering': true,
              "dom": '<"top"f>r<"bottom"litp><"clear">'
          });
          $('.dataTables_filter').addClass('pull-left');
          $('.dataTables_paginate').addClass('pull-left');
      }
      })


      }

   })
}