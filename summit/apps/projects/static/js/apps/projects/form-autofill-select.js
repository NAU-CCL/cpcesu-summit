let curr_name = "";
let type = "";
let park = ""
let agency=""
let partner=""
function selectPerson(id, letter){
    let first = document.getElementById(id + "first").innerText
    let last = document.getElementById(id + "last").innerText;
    $("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById(id)).addClass("info-background");
    curr_name = first + " " + last;
}
function selectPark(id){
    let park_name = document.getElementById(id + "park").innerText
    console.log(park_name)
    $("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById(id)).addClass("info-background");
    park = park_name;
}
function selectPartner(id){
    let partner_name = document.getElementById(id + "partner").innerText
    console.log(partner_name)
    $("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById(id)).addClass("info-background");
    partner= partner_name;
}
function selectAgency(id){
    let agency_name = document.getElementById(id + "agency").innerText
    console.log(agency_name)
    $("tr").each(function(index){
        if($(this).hasClass("info-background")){
            $(this).removeClass("info-background");
        }
    })
    $(document.getElementById(id)).addClass("info-background");
    agency = agency_name
}

$("#project_manager").on('click', function(){
    type = "m";
})

$("#pp_i").on('click', function(){
    type = "i";
})

$("#tech_rep").on('click', function(){
    type = "r";
})

$("#submit-person").on('click', function(){
    console.log(curr_name);
    if(type == "m"){
    document.getElementById("project_manager").value = curr_name;
    }
    if(type == "i"){
    document.getElementById("pp_i").value = curr_name;
    }
    if(type == "r"){
    document.getElementById("tech_rep").value = curr_name;
    }
    $("#myModal").close
})
$("#submit-park").on('click', function(){
    document.getElementById("location").value = park;

    $("#locationModal").close
})
$("#submit-partner").on('click', function(){
    document.getElementById("partner").value = partner;
    $("#partnerModal").close
})
$("#submit-agency").on('click', function(){
    document.getElementById("federal_agency").value = agency;
    $("#agencyModal").close
})
