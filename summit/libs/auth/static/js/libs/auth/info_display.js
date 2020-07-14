$(document).ready(function(){
$(document.getElementById("contact")).addClass("tab-background")
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
            table = $('#info')
            table.empty()
            $.each(resp['user'],function(index,user, orgs=resp['orgs']){
            table.append(`<div style="background-color: gray;">
            <div style="width: 89%; display: inline-block">
            <h3 class="center" style="display: block">${user.first_name} ${user.last_name}</h3>
            <h4 class="center"><a href="/accounts/manage_organization/${user.assigned_group_id}/"
        >${groupName}</a></h4>
        </div>
        <div style="width: 10%; display: inline-block">
            <img src="http://s3.amazonaws.com/37assets/svn/765-default-avatar.png" style="max-height: 100%; max-width: 100px">
        </div>
        </div>

            <table style="display: block"><tbody>

        <tr>
            <td><b>Email Address:</b></td>
            <td>${user.email_address}</td>
        </tr>
        <tr>
            <td><b>Phone Number:</b> </td>
            <td>${user.phone_number}</td>
            <td><b>Fax Number:</b> </td>
            <td>${user.fax_number}</td>
        </tr>
        <tr>
            <td><b>Title and Department:</b></td>
            <td>${user.title} | ${user.department}</td>
        </tr>
        <tr>
            <td><b>Location and Address:<b></b></b></td>
            <td>${user.location} <br>${user.address} </td>
        </tr>
        </tbody></table>`)
        }

        )}
     })
}


