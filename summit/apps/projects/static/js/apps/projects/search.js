
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

// code that does the actual search
var search = function(){
    let FY = document.getElementById('FY').value
    let AwardNumber = document.getElementById('AwardNum').value
    let Partner = document.getElementById('partner').value
    let Place = document.getElementById('location').value
    let Status = document.getElementById('Status').value
    let Agency = document.getElementById('Agency').value
    let Title = document.getElementById('Title').value
    let PI = document.getElementById('pp_i').value
    let PM = document.getElementById('project_manager').value

    const formatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
      })
    
    $(document.getElementById('overlay')).removeClass("invisible")
    /*$.getJSON("/api/contacts/", function(data){    
        $.each( data, function(key, contact){
            if (PM == contact.first_name + " " + contact.last_name){
                console.log(contact.first_name + " " + contact.last_name);
                
                PM = contact.pk;
                console.log(PM);
            }
            
        });
        
    });*/
    
    $.ajax({
        type: "GET",
        url: '/projects/search',
        data: {'FY': FY,
        "AwardNumber": AwardNumber,
        "partner_name": Partner,
        "place": Place,
        "status": Status,
        "agency": Agency,
        "title": Title,
        "pi": PI,
        "pm": PM,
        "cesu": cesuID},
        success: function(resp){
            console.log(resp)
            table = $('#replace').DataTable();
            if($.fn.DataTable.isDataTable('#replace'))
            {
                table.clear()
                console.log("hi")
            }
            $.each(resp['projects'],function(index,project,partners=resp['partners'],agencies=resp['agencies'],managers=resp['managers']){
                //commented this out so we can see all projects regardless of award#
                /**if(project.p_num == "" || project.p_num == null){
                    return;
                }**/
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
                if (project.p_num != null && project.p_num != "" ) {
                    AwardNum = project.p_num.toUpperCase()
                }
                title = '<a href="/projects/detail/'+ project.id + '/">'+ project.project_title + '</a>'
                totalAmount = formatter.format(project.budget)
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
                startDate = start_date
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

                let award_info = "<span style='font-weight: bold;'>Status:</span> " + status 
                    + "</br><span style='font-weight: bold;'>Award Number:</span> " + AwardNum 
                    + "</br><span style='font-weight: bold;'>Award Amount:</span> " +  totalAmount;
                let start_end = "<span style='font-weight: bold;'>FY:</span> " + FY
                    + "</br> <span style='font-weight: bold;'>Start:</span> " + startDate 
                    + "</br> <span style='font-weight: bold;'>End:</span> " + endDate;
                    
                let staff = "<span style='font-weight: bold;'>PM: </span>" + pM
                    + "</br> <span style='font-weight: bold;'>PI: </span>" + pI;

                table.row.add([
                checkBox,
                
                agency_name,
                partner_name,
                award_info,
                title,
                start_end,
                staff,
                //endDate,
                //pM,
                //pI
                ]).draw()
                $(document.getElementById('overlay')).addClass("invisible")
                //$(document.getElementById('overlay')).removeClass("visible");



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
                $(document.getElementById('overlay')).addClass("invisible")
            }


        }
    })
}


$('#searchButton').on('click', search)

var input = document.getElementById("advancedSearch");

input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    document.getElementById("searchButton").click();
  }
}); 