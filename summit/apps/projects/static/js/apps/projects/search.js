$('#advancedSearchButton').on('click', function(){
$(document.getElementById('advancedSearch')).removeClass("invisible");
 $(document.getElementById('advancedSearch')).addClass("visible");
 $(document.getElementById('search')).removeClass("visible");
   $(document.getElementById('search')).addClass("invisible");


})

$('#basicSearchButton').on('click', function(){
$(document.getElementById('search')).addClass("visible");
$(document.getElementById('search')).removeClass("invisible");
   $(document.getElementById('advancedSearch')).addClass("invisible")
   $(document.getElementById('advancedSearch')).removeClass("visible")


})

$('#searchButton').on('click', function(){
    let FY = document.getElementById('FY').value
    let AwardNumber = document.getElementById('AwardNum').value
    let Partner = document.getElementById('Partner').value
    console.log(FY);
    console.log(AwardNumber)
    console.log(Partner)

    $.ajax({
        type: "GET",
        url: '/projects/search',
        data: {'FY': FY,
        "AwardNumber": AwardNumber,
        "partner_name": Partner},
        success: function(resp){
            console.log(resp)
            table = $('#replace').DataTable();
            if($.fn.DataTable.isDataTable('#replace'))
            {
                table.clear()
                console.log("hi")
            }
            $.each(resp['projects'],function(index,project,partners=resp['partners'],agencies=resp['agencies'],managers=resp['managers']){
                project_federal_agency_id = project.federal_agency_id
                project_partner_id = project.partner_id
                project_manager_id = project.project_manager_id
                project_pp_i_id = project.pp_i_id
                let checkBox = ""
                let status = ""
                let agency_name = ""
                let partner_name = ""
                let FY = ""
                let AwardNum = ""
                let title = ""
                let totalAmount = ""
                let startDate = ""
                let endDate = ""
                let pM = ""
                let pI = ""
                table_row = $("<tr></tr");
                checkBox = '<input class="export_list_1" type="checkbox" name="export_list" value="' + project.id + '"/>'
                status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
                $.each(agencies, function(index,agency){
                    if(agency.id == project_federal_agency_id){
                    agency_name = agency.name
                    return false;
                    }
                })
                let p_case = "None"
                $.each(partners, function(index,partner){
                    if(partner.id == project_partner_id){
                    partner_name = partner.name
                    p_case = "Exists"
                    return false;
                    }
                })
                if(p_case == "None"){
                partner_name = " "
                }
                FY = project.fiscal_year
                AwardNum = project.p_num.toUpperCase()
                title = '<a href="/projects/detail/'+ project.id + '/">'+ project.project_title + '</a>'
                totalAmount = project.award_amt
                let start = new Date(project.tent_start_date)
                let start_date = start.toDateString()
                startDate = start_date
                let end = new Date(project.tent_end_date)
                let end_date = end.toDateString()
                endDate = end_date
                let no_man = "None"
                $.each(managers, function(index,manager){
                    if(manager.id == project_manager_id){
                    pM = manager.first_name + " " + manager.last_name
                    no_man = "Exists"
                    return false;
                    }
                })
                if(no_man == "None"){
                    pM = " "
                }

                no_man = "None"

                $.each(managers, function(index,manager){
                    if(manager.id == project_pp_i_id){
                    pI = manager.first_name + " " + manager.last_name
                    no_man = "Exists"
                    return false;
                    }
                })
                if(no_man == "None"){
                    pI = " "
                }

                table.row.add([
                checkBox,
                status,
                agency_name,
                partner_name,
                FY,
                AwardNum,
                title,
                totalAmount,
                startDate,
                endDate,
                pM,
                pI
                ]).draw()



                /*table_row.append(`<td>
                                <a class="btn btn-outline-primary btn-sm m-0 waves-effect"
                                   href="/projects/detail/${project.id}/">
                                    Details
                                </a>
                            </td>`)*/
            })
            if(resp['projects'].length == 0)
            {
                alert("No projects match given search")
            }


        }
    })
})