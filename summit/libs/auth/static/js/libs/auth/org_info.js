$(document).ready(function(){
$(document.getElementById("organization")).addClass("tab-background")
$(document.getElementById("contentBody")).addClass("content-background");
$('td:nth-child(3),th:nth-child(3)').hide();
})

var people_table = $('#people_table').DataTable()

$(document).on('click', '#people_table tr', function(){
    loadProjectDetails($(this).attr('id'));
});

function loadProjectDetails(id){
    $(document.getElementsByClassName("people_table")).removeClass("clicked-background");
    $(document.getElementById(id)).addClass("clicked-background");
    
    let projects_name = document.getElementById("projects_header");
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
                  let status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
                  
                  table_2.row.add([
                    status,
                    '<a href="/projects/detail/' + project.id + '"/>' + project.project_title + '</a>', 
                    userRole
                  ]).draw()
                  $('td:nth-child(3),th:nth-child(3)').show();
                }
                  
              })
        if($.fn.DataTable.isDataTable('#table_2')){
            table_2.destroy()
        }
        })
  
  
        }
  
     })
  }

function loadDetails(id){
    $(document.getElementsByClassName("clicked-background")).removeClass("clicked-background");
    $(document.getElementById(id)).addClass("clicked-background");
$("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById("info")).addClass("info-background");
    $(document.getElementById(id)).addClass("info-background");

    document.getElementById("projects_header").innerHTML = "Projects";

    let table = $('#org_info')
    table.empty();
    let group = document.getElementById("a" + id).innerText
    table.append(`<a href="/accounts/edit_organization/${id}/" style="float:right; 
        font-size:24px"> <i class="fas fa-edit"></i></a>`)
    table.append(`<h5 class="center" style="align: block;"><a href="/accounts/manage_organization/${id}/">${group}</a></h5>`)
    table.append(`<h5 class="center"></h4>`)
    
    let groupID = id;
    //let groupName = document.getElementById("a" + groupID).innerText;
    $.ajax({
    type: "GET",
    url: '/accounts/org_info',
    data: {'groupID': groupID},
    success: function(resp){
        console.log(resp);
        people_table = $('#people_table').DataTable()
        table_2 = $('#table_2').DataTable()
        people_table.clear();
        table_2.clear();

        $.each(resp['people'], function(index,person){
            people_table.row.add([
                    person.first_name,
                    person.last_name
            ]).node().id = person.id;
            people_table.draw(false);
        })

        $.each(resp['projects'], function(index,project){
            if (project.status != 'ARCHIVED'){
                let start = new Date(project.tent_start_date)
                let start_date_day = start.getDate();
                let start_date_month = start.getMonth() + 1;
                let start_date_year = start.getFullYear();
                let start_date = start_date_month + "/" + start_date_day + "/" + start_date_year;

                let end = new Date(project.tent_end_date)
                let end_date_day = end.getDate();
                let end_date_month = end.getMonth() + 1;
                let end_date_year = end.getFullYear();
                let end_date = end_date_month + "/" + end_date_day + "/" + end_date_year;
                let status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
                table_2.row.add([
                        status,
                        '<a href="/projects/detail/' + project.id + '"/>' + project.project_title + '</a>',
                        null
                ]).draw()
            }

        })
        if($.fn.DataTable.isDataTable('#people_table'))
        {
            people_table.destroy()
        }
        /*else{
        $('#table_1').DataTable({
            retrieve: true,
            'ordering': true,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        })
        }*/
        if($.fn.DataTable.isDataTable('#table_2')){
        table_2.destroy()
        }
        /*else{
        $('#table_2').DataTable({
            retrieve: true,
            'ordering': true,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        });
        }*/
    }
    })
    //$('#table_1').DataTable().ajax.reload();
    document.getElementById('info').style.display = "inline-block";
    $('td:nth-child(3),th:nth-child(3)').hide();
}