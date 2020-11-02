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
            header.append(`<div style="background-color: gray;">
            <div style="width: 89%; display: inline-block">
            <h3 class="center" style="display: block">${user.first_name} ${user.last_name}</h3>
            <h4 class="center"><a href="/accounts/manage_organization/${user.assigned_group_id}/"
        >${groupName}</a></h4>
        </div>
        <div style="width: 10%; display: inline-block">
            <img src="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png" style="max-height: 100%; max-width: 100px">
        </div>
        </div>`)
        $.each(projects, function(index,project){
            let start = new Date(project.tent_start_date)
            let start_date = start.toDateString()
            let end = new Date(project.tent_end_date)
            let end_date = end.toDateString()
            let status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
            table_2.row.add([
                    status,
                    '<a href="/projects/detail/' + project.id + '"/>' + project.project_title + '</a>',
                    start_date,
                    end_date
            ]).draw()

        })
        })


        }

     })
     document.getElementById('info').style.display = "inline-block"
}


