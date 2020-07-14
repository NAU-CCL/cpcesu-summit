$(document).ready(function(){
    $(document.getElementById("project")).addClass("tab-background")
    $('#filter').on('click', function() {
    let start_date = document.getElementById('start_date').value;
    //console.log(start_date)
    let end_date = document.getElementById('end_date').value;
    //console.log(end_date)
    let ddl = document.getElementById('status');
    let status = ddl.options[ddl.selectedIndex].text;
    status.toUpperCase()
    //console.log(status)
    $.ajax({
        type: "GET",
        url: '/projects/filter',
        data: {'start_date': start_date,
        "end_date": end_date,
        "status": status},
        success: function(resp){
            console.log(resp)
            table = $('#filterable')
            table.empty()
            $.each(resp['projects'],function(index,project,partners=resp['partners'],agencies=resp['agencies'],managers=resp['managers']){
                project_federal_agency_id = project.federal_agency_id
                project_partner_id = project.partner_id
                project_manager_id = project.project_manager_id
                project_pp_i_id = project.pp_i_id
                table_row = $("<tr></tr");
                table_row.append(`<th scope="row">
                                <input class="export_list_1" type="checkbox" name="export_list" value="${ project.id }"/>
                            </th>`)
                table_row.append(`<td>${project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)}</td>`)
                $.each(agencies, function(index,agency){
                    if(agency.id == project_federal_agency_id){
                    table_row.append(`<td>${agency.name}</td>`)
                    }
                })
                let p_case = "None"
                $.each(partners, function(index,partner){
                    if(partner.id == project_partner_id){
                    table_row.append(`<td>${partner.name}</td>`)
                    p_case = "Exists"
                    }
                })
                if(p_case == "None"){
                table_row.append(`<td></td>`)
                }
                table_row.append(`<td>${project.fiscal_year}</td>`)
                table_row.append(`<td>${project.p_num.toUpperCase()}</td>`)
                table_row.append(`<td><a href="/projects/detail/${project.id}/">${project.project_title}</a></td>`)
                table_row.append(`<td>${project.award_amt}</td>`)
                let start = new Date(project.tent_start_date)
                let start_date = start.toDateString()
                table_row.append(`<td>${start_date}</td>`)
                let end = new Date(project.tent_end_date)
                let end_date = end.toDateString()
                table_row.append(`<td>${end_date}</td>`)
                table.append(table_row)
                let no_man = "None"
                $.each(managers, function(index,manager){
                    if(manager.id == project_manager_id){
                    table_row.append(`<td>${manager.first_name} ${manager.last_name}</td>`)
                    no_man = "Exists"
                    }
                })
                if(no_man == "None"){
                    table_row.append(`<td>${no_man}</td>`)
                }

                no_man = "None"

                $.each(managers, function(index,manager){
                    if(manager.id == project_pp_i_id){
                    table_row.append(`<td>${manager.first_name} ${manager.last_name}</td>`)
                    no_man = "Exists"
                    }
                })
                if(no_man == "None"){
                    table_row.append(`<td>${no_man}</td>`)
                }

                /*table_row.append(`<td>
                                <a class="btn btn-outline-primary btn-sm m-0 waves-effect"
                                   href="/projects/detail/${project.id}/">
                                    Details
                                </a>
                            </td>`)*/
            })


        }
    })
    });

});
