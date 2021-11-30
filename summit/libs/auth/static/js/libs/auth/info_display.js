$(document).ready(function(){
    $(document.getElementById("contact")).addClass("tab-background")
    $(document.getElementById("contentBody")).addClass("content-background");
    var urlParams = new URLSearchParams(window.location.search);
    var personid = urlParams.get('id');
    if (personid)
    {
      loadDetails(personid);
    }
})

const NOTHING_SELECTED = -1;
var selected = NOTHING_SELECTED;

function loadDetails(id){
    table_2 = $('#table_2').DataTable();
    header = $('#header_top');
    table = $('#info');  
    org_dept = $('#org-dept');
    email = $('#email');
    phone = $('#phone');
    fax = $('#fax');
    pic_container = $('#pic_container');
    user_location = $('#location');
    contact_info = $('#contact-info');
    no_select = $('#nothing-selected');

    if (selected == id)
    {
        contact_info.hide()
        no_select.show()
        $(document.getElementsByClassName("clicked-background")).removeClass("clicked-background");
        selected = NOTHING_SELECTED;
        header.empty()
        pic_container.empty()
        table_2.clear()
        
    }
    else
    {
        no_select.hide()
        contact_info.show()
        $(document.getElementsByClassName("clicked-background")).removeClass("clicked-background");
        $(document.getElementById(id)).addClass("clicked-background");
        $("tr").each(function(index){
            if($(this).hasClass("info-background")){
                $(this).removeClass("info-background");
            }
        })
        selected = id;
        let userID = id;
        
        $(document.getElementById("info")).addClass("info-background");
        $(document.getElementById(id)).addClass("info-background");
        $.ajax({
        type: "GET",
            url: '/accounts/info_display',
            data: {'userID': userID},
            success: function(resp){
                console.log(resp);
                table.empty()
                pic_container.empty()
                org_dept.empty()
                email.empty()
                phone.empty()
                fax.empty()
                user_location.empty()

                header.empty()
                table_2.clear()
                
                
                $.each(resp['user'],function(index,user, orgs=resp['orgs'], projects=resp['projects']){
                let groupID = user.assigned_group_id;
                var groupName = "No Organization"
                if (document.getElementById("a" + groupID))
                {
                    groupName = document.getElementById("a" + groupID).innerText;
                }
                if (user.title)
                {
                    header.append(`
                        <h4 class="center" style="display: block;">
                        ${user.first_name} ${user.last_name}

                        <a href="/accounts/edit_contact/${id}/" title="Edit Contact" 
                            style="float:right; font-size:24px; font-weight: 50%"> <ion-icon name="create-outline"></ion-icon> </a>
                        
                        </h4>
                        
                        
                        
                        <div class="center">${user.title}, ${user.department} </br> <a href="/accounts/all_groups/?id=${user.assigned_group_id}">
                    ${groupName}</a></div>
                    </div>`)
                }
                else
                {
                    header.append(`
                        <h4 class="center" style="display: block;">
                        ${user.first_name} ${user.last_name}

                        <a href="/accounts/edit_contact/${id}/" title="Edit Contact" 
                            style="float:right; font-size:24px; font-weight: 50%"> <ion-icon name="create-outline"></ion-icon> </a>
                        
                        </h4>
                        <div class="center"><a href="/accounts/all_groups/?id=${user.assigned_group_id}">
                    ${groupName}</a></div>
                    </div>`)
                }
                pic_container.append(`
                <img src="/static/imgs/TEST_AVATAR.png" style="float:right; max-width: 80%; margin-top: 5%; margin-bottom: 5%">`)
                
                if (user.email_address)
                {
                    email.append(`
                    ${user.email_address}
                    <br/>
                    `)
                }

                if (user.phone_number)
                {
                    phone.append(`
                    <span class="text-muted">
                        Ph #: 
                    </span>
                    ${user.phone_number}
                    <br/>
                    `)
                }

                if (user.fax_number)
                {
                    fax.append(`
                    <span class="text-muted">
                        Fax #: 
                    </span>
                    ${user.fax_number}
                    `)
                }

                user_location.append(`
                    <span>
                    
                    ${user.location}
                    <br/>
                    ${user.address}
                    </span>
                    
                    
                `)

                
            
            /*<table class="table table-bordered"> 
                    <tr>
                        <td><b>Title:</b><br></td>
                        <td>
                            </div>
            </div>
                        </td>
                    </tr>
                    <tr>
                        <td><b>Email:</b><br></td>
                        <td>
                            ${user.email_address}
                        </td>
                    </tr>
                    <tr>
                        <td><b>Phone Number:</b><br></td>
                        <td>
                            ${user.phone_number}
                        </td>
                    </tr>
                    <tr>
                        <td><b>Fax Number:</b><br></td>
                        <td>
                            ${user.fax_number}
                        </td>
                    </tr>
                    <tr>
                        <td><b>Address:</b><br></td>
                        <td>
                            ${user.address}
                        </td>
                    </tr>
                    
                </table>
                
            `)*/
            $.each(projects, function(index,project){
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
                            start_date,
                            end_date
                    ]).draw()
                }

            })
            if($.fn.DataTable.isDataTable('#table_2')){
                table_2.destroy()
            }
            })


            }

        })
        document.getElementById('contact-info').style.display = "inline-block"
    }
}


