$(document).ready(function(){
  $(document.getElementById("contact")).addClass("tab-background")
  $(document.getElementById("contentBody")).addClass("content-background");
  var urlParams = new URLSearchParams(window.location.search);
  console.log(cesuID);
  var personid = urlParams.get('id');

  var table = $('#main_table').DataTable();
  if (personid)
  {
      console.log(table.row(personid))
      table.row('#' + personid).scrollTo(false);
      loadDetails(personid);
  }
})

const NOTHING_SELECTED = -1;
var selected = NOTHING_SELECTED;

function loadDetails(id){
  table_2 = $('#table_2').DataTable();
  header = $('#header_top');
  admin_buttons = $('#admin-buttons');
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
          url: '/accounts/user_info_display',
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
              admin_buttons.empty()

              header.empty()
              table_2.clear()
              
              
              $.each(resp['user'],function(index,user, orgs=resp['orgs'], projects=resp['projects']){
              let groupID = user.assigned_group_id;
              var groupName = ""
              if (document.getElementById("a" + groupID))
              {
                  groupName = document.getElementById("a" + groupID).innerText;
              }
              if (user.title)
              {
                  header.append(`
                      <h4 class="center" style="display: block;">
                      ${user.first_name} ${user.last_name}

                      <a href="/accounts/edit_user/${id}/" title="Edit User" 
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

                      <a href="/accounts/edit_user/${id}/" title="Edit Contact" 
                          style="float:right; font-size:24px; font-weight: 50%"> <ion-icon name="create-outline"></ion-icon> </a>
                      
                      </h4>
                      <div class="center"><a href="/accounts/all_groups/?id=${user.assigned_group_id}">
                  ${groupName}</a></div>
                  </div>`)
              }
              pic_container.append(`
              <img src="/static/imgs/TEST_AVATAR.png" style="float:right; max-width: 80%; margin-top: 5%; margin-bottom: 5%">`)
              
              if (user.email)
              {
                  email.append(`
                  ${user.email}
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

              admin_buttons.append(`

              <button class="btn btn-sm btn-outline-primary" style="float:left">
                Change Password
              </button>
              <button class="btn btn-sm btn-outline-danger" onclick=delete_user(${userID}) style="float:right">
                Delete Account
              </button>
              
            `)
            if (user.is_active)
            {
              admin_buttons.append(`
              <button id="suspend-button" onclick=suspend_account(${user.id}) class="btn btn-sm btn-outline-primary" style="float:right">
                Suspend Account
              </button>`)
            }
            else
            {
                admin_buttons.append(`
              <button id="activate-button" onclick=activate(${user.id}) class="btn btn-sm btn-outline-primary" style="float:right">
                Reactivate Account
              </button>`)
            }

          })
          

          }

      })
      document.getElementById('contact-info').style.display = "inline-block"
  }
}

var suspend_account = function(userID){
    console.log('hi')
    admin_buttons = $('#admin-buttons');
    $.ajax({
        type: "POST",
        url: '/accounts/deactivate_user/',
        data: {'userID': userID, 'reactivate': "false"},
        headers: {"X-CSRFToken":csrf_token},
        success: function(resp){
            console.log(resp)
        }})
        admin_buttons.empty()
        admin_buttons.append(`

        <button class="btn btn-sm btn-outline-primary" style="float:left">
          Change Password
        </button>
        <button class="btn btn-sm btn-outline-danger" onclick=delete_user(${userID}) style="float:right">
          Delete Account
        </button>
        <button id="activate-button" onclick=activate(${userID}) class="btn btn-sm btn-outline-primary" style="float:right">
          Reactivate Account
        </button>
        
      `)
  }

  var activate = function(userID){
    console.log('hi')
    admin_buttons = $('#admin-buttons');
    $.ajax({
        type: "POST",
        url: '/accounts/deactivate_user/',
        data: {'userID': userID, 'reactivate': "true"},
        headers: {"X-CSRFToken":csrf_token},
        success: function(resp){
            console.log(resp)
        }})
        admin_buttons.empty()
        admin_buttons.append(`

        <button class="btn btn-sm btn-outline-primary" style="float:left">
          Change Password
        </button>
        <button class="btn btn-sm btn-outline-danger" onclick=delete_user(${userID}) style="float:right">
          Delete Account
        </button>
        <button id="suspend-button" onclick=suspend_account(${userID}) class="btn btn-sm btn-outline-primary" style="float:right">
          Suspend Account
        </button>
        
      `)
  }

  var delete_user = function(userID){
    console.log(userID);
    if (confirm('Are you sure you want to delete this user? This action cannot be undone!')) {
        $.ajax({
            type: "POST",
            url: '/accounts/delete_user/',
            data: {"userID": userID},
            headers: {"X-CSRFToken":csrf_token},
            success: function(resp){
                console.log(resp)
                window.location.reload(true)
            }
        })
    }
    
  }


