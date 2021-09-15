$(document).ready(function(){
$(document.getElementById("organization")).addClass("tab-background")
$(document.getElementById("contentBody")).addClass("content-background");
})

function loadDetails(id){
$("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById("info")).addClass("info-background");
    $(document.getElementById(id)).addClass("info-background");
    let table = $('#org_info')
    table.empty();
    let group = document.getElementById("a" + id).innerText
    table.append(`<h5 class="center" style="align: block; font-weight:bold;">${group}</h5>`)
    table.append(`<h5 class="center"></h4>`)
    table.append(`<a href="/accounts/edit_organization/${id}/" style="float:right" class="btn btn-light">Edit Organization</a>`)
    let groupID = id;
    //let groupName = document.getElementById("a" + groupID).innerText;
    $.ajax({
    type: "GET",
    url: '/accounts/org_info',
    data: {'groupID': groupID},
    success: function(resp){
        console.log(resp);
        table_1 = $('#table_1').DataTable()
        table_2 = $('#table_2').DataTable()
        table1 = $('#table1')
        table2 = $('#table2')
        table_1.clear();
        table_2.clear();
        $.each(resp['projects'], function(index,project){
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
        if($.fn.DataTable.isDataTable('#table_1'))
        {
        table_1.destroy()
        console.log("hi")
        $('#table_1').DataTable({
            retrieve: true,
            'ordering': true,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        });
        $('.dataTables_filter').addClass('pull-left');
        $('.dataTables_paginate').addClass('pull-left');
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
        $('#table_2').DataTable({
            retrieve: true,
            'ordering': true,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        });
        $('.dataTables_filter').addClass('pull-left');
        $('.dataTables_paginate').addClass('pull-left');
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
}