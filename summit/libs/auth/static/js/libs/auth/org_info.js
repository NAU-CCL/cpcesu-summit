$(document).ready(function(){
$(document.getElementById("organization")).addClass("tab-background")
$(document.getElementById("contentBody")).addClass("content-background");
$('td:nth-child(3),th:nth-child(3)').hide();
  var urlParams = new URLSearchParams(window.location.search);
  var orgid = urlParams.get('id');
  var table = $('#main_table').DataTable();
  if (orgid)
  {
    var test_var = document.getElementById("a"+orgid).innerText;
    console.log(test_var);
    table.row('#' + orgid).scrollTo(false);
    //table.search(test_var).draw();
    loadDetails(orgid);
  }
  
})
var people_table = $('#people_table').DataTable({
  "scrollY": "400px",
  "scrollCollapse": true
})

$(document).on('click', '#people_table tr', function(){
    loadProjectDetails($(this).attr('class'));
});

const NOTHING_SELECTED = -1;
var org_selected = NOTHING_SELECTED;
var person_selected = NOTHING_SELECTED;
var current_org_id = NOTHING_SELECTED;

function loadProjectDetails(id){
    $(document.getElementsByClassName(person_selected)).removeClass("clicked-background");
    id = id.split(" ")[0];
    console.log(id)
    $(document.getElementsByClassName(id)).addClass("clicked-background");
    
    
    let projects_name = document.getElementById("projects_header");
    if (person_selected == id)
    {
      
      current_org_id = org_selected;
      org_selected = NOTHING_SELECTED;

      console.log(current_org_id)
      console.log(org_selected)
      $(document.getElementsByClassName("clicked-background")).removeClass("clicked-background");
      loadDetails(current_org_id);

    }
    else
    {
      let userID = id;
      person_selected = id;
      $.ajax({
      type: "GET",
          url: '/accounts/info_display',
          data: {'userID': userID, 'cesuID': cesuID},
          success: function(resp){
              console.log(resp);
              table_2 = $('#table_2').DataTable({
                "scrollY": "400px",
                "scrollCollapse": true
              })
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
    
    

    let info = $('#info')


    no_select = $('#nothing-selected');

    document.getElementById("projects_header").innerHTML = "Projects";

    person_selected = NOTHING_SELECTED;
    

    if(org_selected == id)
    {
      no_select.show()
      org_selected = NOTHING_SELECTED;
      info.hide()
    }
    else
    {
      no_select.hide()
      info.show()
      org_selected = id;
    

    let table = $('#org_info');
    let pic_container = $('#pic_container');
    let city = $('#city');
    let state = $('#state');
    let description = $('#description');

    
    
    let groupID = id;
    //let groupName = document.getElementById("a" + groupID).innerText;
    $.ajax({
    type: "GET",
    url: '/accounts/org_info',
    data: {'groupID': groupID, 'cesuID': cesuID},
    success: function(resp){
        console.log(resp);
        people_table = $('#people_table').DataTable()
        table_2 = $('#table_2').DataTable()
        people_table.clear();
        table_2.clear();

        table.empty();
        let group = resp['org'][0].name;
        if (user_role != 'VIEWER'){
          table.append(`<a href="/accounts/edit_organization/${id}/" style="float:right; 
            font-size:24px"> <ion-icon name="create-outline"></ion-icon></a>`)
        }
        
        if (resp['org'][0].logo)
        {
          pic_container.append(`
                    <img src="/data/${resp['org'][0].logo}" style="float:right; max-width: 80%; margin-top: 5%; margin-bottom: 5%">`)
        }
        
        table.append(`<h4 class="center" style="display: block;">${resp['org'][0].name}</a></h4>`)
        table.append(`<h4 class="center"></h4>`)
        if (resp['org'][0].description)
        {
          description.append(`<div><span class="text-muted">
          Description:
            </span> ${resp['org'][0].description}</div>`)
        }
        if (resp['org'][0].contact)
        {
          description.append(`<div><span class="text-muted">
          Contact Information:
            </span> ${resp['org'][0].contact}</div>`)
        }
        if (resp['org'][0].city)
        {
          description.append(`<div><span class="text-muted">
          City:
            </span> ${resp['org'][0].city}</div>`)
        }
        if (resp['org'][0].state)
        {
          description.append(`<div><span class="text-muted">
          State:
            </span> ${resp['org'][0].state}</div>`)
        }
        

        $.each(resp['people'], function(index,person){
            var new_row = people_table.row.add([
                    '<a href="/accounts/all_contacts/?id='+ person.id + '"/>' + person.first_name + '</a>',
                    '<a href="/accounts/all_contacts/?id='+ person.id + '"/>' + person.last_name + '</a>'
            ]).node();
            var person_id = person.id.toString();
            $(new_row).addClass(person_id);
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

}