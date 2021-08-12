$(document).ready(function(){
$(document.getElementById("contact")).addClass("tab-background");
$(document.getElementById("contentBody")).addClass("content-background");
})

function loadDetails(id, group){
    $("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    let userID = id;
    let groupID= group;
    let groupName = document.getElementById("a" + groupID).innerText;
    console.log(groupName)
    $(document.getElementById("info")).addClass("info-background");
    $(document.getElementById(id)).addClass("info-background");
    console.log(userID);
    $.ajax({
    type: "GET",
        url: '/accounts/info_display',
        data: {'userID': userID},
        success: function(resp){
            console.log(resp);
            table_2 = $('#table_2').DataTable()
            table = $('#info')
            header = $('#header')
            header.empty()
            table_2.clear()
            $.each(resp['user'],function(index,user, orgs=resp['orgs'], projects=resp['projects']){
            header.append(`<div style="background-color: #bab4b5">
            <div style="width: 100%; display: inline-block">
            <h5 class="center" style="display: block; font-weight:bold">${user.first_name} ${user.last_name}</h5>
            <h5 class="center"><a href="/accounts/manage_organization/${user.assigned_group_id}/"
        >${groupName}</a></h5>
        </div>
        </div>`)
        $.each(projects, function(index,project){
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
                    start_date,
                    end_date
            ]).draw()

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
     document.getElementById('contact-info').style.display = "inline-block"
}


