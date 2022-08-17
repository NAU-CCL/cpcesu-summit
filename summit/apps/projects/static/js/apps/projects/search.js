$('#FY').on('change keyup', function() {
    // Remove invalid characters
    var sanitized = $(this).val().replace(/[^0-9]/g, '');
    // Update value
    $(this).val(sanitized);
});

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
    let techLead = document.getElementById('tech_lead').value

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
        "tech_lead": techLead,
        "cesu": cesuID},
        success: function(resp){
            console.log(resp)
            table = $('#replace').DataTable();
            if($.fn.DataTable.isDataTable('#replace'))
            {
                table.clear()
                console.log("hi")
            }
            $.each(resp['projects'],function(index,project,partners=resp['partners'],agencies=resp['agencies'],managers=resp['managers'],files=resp['files']){
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
                let tech_lead = ""
                table_row = $("<tr></tr");
                checkBox = '<input class="export_list_1" type="checkbox" name="export_list" value="' + project.id + '"/>'
                status = project.status.charAt(0).toUpperCase() + project.status.toLowerCase().slice(1)
                $.each(agencies, function(index,agency){
                    if(agency.id == project_federal_agency_id){
                    agency_name = agency.name + " (" + agency.abbrv + ")" 
                    return false;
                    }
                })
                let p_case = "None"
                $.each(partners, function(index,partner){
                    if(partner.id == project_partner_id){
                    partner_name = partner.name + " (" + partner.abbrv + ")" 
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

                no_man = "None"

                $.each(managers, function(index,manager){
                    if(manager.id == project.tech_rep_id){
                    tech_lead = manager.first_name + " " + manager.last_name
                    no_man = "Exists"
                    return false;
                    }
                })

                if(no_man == "None"){
                    tech_lead = " "
                }

                let award_info = "<span style='font-weight: bold;'>Status:</span> " + status 
                    + "</br><span style='font-weight: bold;'>Award Number:</span> " + AwardNum 
                    + "</br><span style='font-weight: bold;'>Award Amount:</span> " +  totalAmount;
                let start_end = "<span style='font-weight: bold;'>FY:</span> " + FY
                    + "</br> <span style='font-weight: bold;'>Start:</span> " + startDate 
                    + "</br> <span style='font-weight: bold;'>End:</span> " + endDate;
                
                let staff = "";
                if (tech_lead != " "){
                    staff = staff + "<span style='font-weight: bold;'>Tech Rep: </span>" + tech_lead;
                }

                if (pM != " "){
                    staff = staff + "</br> <span style='font-weight: bold;'>PL: </span>" + pM
                }

                if (pI != " "){
                    staff = staff + "</br> <span style='font-weight: bold;'>PI: </span>" + pI;
                }
               
                
                

                table.row.add([
                checkBox,
                
                agency_name,
                partner_name,
                award_info,
                title,
                start_end,
                staff
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

var upload_search = function(){
    let FY = document.getElementById('FY').value
    let AwardNumber = document.getElementById('AwardNum').value
    let Partner = document.getElementById('partner').value
    let Place = document.getElementById('location').value
    let Status = document.getElementById('Status').value
    let Agency = document.getElementById('Agency').value
    let Title = document.getElementById('Title').value
    let PI = document.getElementById('pp_i').value
    let PM = document.getElementById('project_manager').value
    let techLead = document.getElementById('tech_lead').value

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
        "tech_lead": techLead,
        "cesu": cesuID},
        success: function(resp){
            console.log(resp)
            table = $('#replace').DataTable();
            if($.fn.DataTable.isDataTable('#replace'))
            {
                table.clear()
                console.log("hi")
            }
            $.each(resp['projects'],function(index,project,partners=resp['partners'],agencies=resp['agencies'],managers=resp['managers'],files=resp['files']){
                //commented this out so we can see all projects regardless of award#
                /**if(project.p_num == "" || project.p_num == null){
                    return;
                }**/
                project_federal_agency_id = project.federal_agency_id
                project_partner_id = project.partner_id
                project_manager_id = project.project_manager_id
                project_pp_i_id = project.pp_i_id

                let local_num = "N/A"

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
                let tech_lead = ""
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

                no_man = "None"

                $.each(managers, function(index,manager){
                    if(manager.id == project.tech_rep_id){
                    tech_lead = manager.first_name + " " + manager.last_name
                    no_man = "Exists"
                    return false;
                    }
                })

                if(no_man == "None"){
                    tech_lead = " "
                }

                if (project.local_num){
                    local_num = project.local_num
                }
                

                let award_info = "<span style='font-weight: bold;'>Status:</span> " + status 
                    + "</br><span style='font-weight: bold;'>Award Number:</span> " + AwardNum
                    + "</br><span style='font-weight: bold;'>Local Number:</span> " + local_num 
                    + "</br><span style='font-weight: bold;'>Award Amount:</span> " +  totalAmount
                    + "</br><span style='font-weight: bold;'>Partner:</span> " + partner_name 
                    + "</br><span style='font-weight: bold;'>Fed. Agency:</span> " + agency_name;
                let start_end = "<span style='font-weight: bold;'>FY:</span> " + FY
                    + "</br> <span style='font-weight: bold;'>Start:</span> " + startDate 
                    + "</br> <span style='font-weight: bold;'>End:</span> " + endDate;
                
                let staff = "";
                if (tech_lead != " "){
                    "<span style='font-weight: bold;'>Tech Rep: </span>" + tech_lead;
                }

                if (pM != " "){
                    staff = staff + "</br> <span style='font-weight: bold;'>PL: </span>" + pM
                }

                if (pI != " "){
                    staff = staff + "</br> <span style='font-weight: bold;'>PI: </span>" + pI;
                }
                let upload = `<form enctype='multipart/form-data' action='/projects/upload/' method='POST' class='dropzone dz'id='dropzone_`+project.id+`' >
                    <div class='fallback'>
                    <input name='file' type='file' multiple />
                    </div>
                </form>
                `
                upload += '<ul id='+project.id + '-files>'

                $.each(files, function(index,file){
                    if(file.project_id == project.id){
                    upload += '<li> <a href="/data/' + file.file + '">' + file.file + `</a> <a style="cursor:pointer"><ion-icon name="trash-outline" onclick="deleteFile('`+file.id+`', '`+project.id+`')"></ion-icon></a>  </li>`
                    }
                })
                upload += '</ul>'
               
                
                

                table.row.add([
                checkBox,

                award_info,
                title,
                start_end,
                upload
                //endDate,
                //pM,
                //pI
                ]).draw()
                let dropzone_id = '#dropzone_' + project.id;
                const myDropzone= new Dropzone(dropzone_id,{
                    url:'/projects/upload/',
                    init: function() {
                        this.on("sending", function(file, xhr, formData){
                                formData.append("project_id", project.id);
                        });

                        this.on("queuecomplete", function (file) {
                            Dropzone.forElement(dropzone_id).removeAllFiles(true)
                            getFiles(id=project.id)
                       });
                    },
                    headers: {
                        'X-CSRFTOKEN': csrf_token
                    },
                    uploadMultiple: true,
                    parallelUploads: 10,
                    autoProcessQueue: true
                })
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
var getFiles = function(id){
    $.ajax({
        type: "GET",
        url: '/projects/search',
        data: {"id": id},
        
        success: function(resp){
            files=resp['files'];
            new_content = ''
            $.each(files, function(index,file){
                if(file.project_id == id){
                new_content += '<li> <a href="/data/' + file.file + '">' + file.file + `</a> <a style="cursor:pointer"><ion-icon name="trash-outline" onclick="deleteFile('`+file.id+`', '`+file.project_id +`')"></ion-icon></a> </li>`
                }
            })
            replace_id = id+"-files"
            

            document.getElementById(replace_id).innerHTML = new_content


        }
    })
}

var deleteFile = function(file_id, proj_id){
    console.log(file_id);
    console.log(proj_id);
    if (confirm("Do you really want to delete this file?")) {
        $.ajax({
            type: "POST",
            url: '/projects/delete_file/',
            data: {"id": file_id},
            headers: {"X-CSRFToken":csrf_token},
            success: function(resp){
                console.log(resp)
                getFiles(proj_id)
            }
        })
    }
    
}
$('#searchButton').on('click', search)

$('#uploadSearchButton').on('click', upload_search)

var input = document.getElementById("advancedSearch");

input.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    if (document.getElementById("searchButton")){
        document.getElementById("searchButton").click();
    }
    else {
        document.getElementById("uploadSearchButton").click();
    }
  }
}); 