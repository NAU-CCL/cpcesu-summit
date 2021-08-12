// TODO: Make it so that the default funcitonality, if no specific field is given,
// is to have the search bar just search the whole row's HTML
function filterQueryModalList( test, filterBy="" ) {
  console.log("filterQueryModalList RAN");
    let listObj = $(".query-modal-list");
    console.log( listObj );
    console.log( test.parents('div[class^="query-modal-list"]') );
    if(filterBy == ""){
      console.log("Filter is empty");
        listObj.children(".query-entry").removeClass("hidden");
    }
    else {
      console.log("Filter is not empty");
        listObj.children(".query-entry").each(function(i, e){
            console.log($(e).children(".search_field"));
            console.log($(e).children(".search_field").html());
            if($(e).children(".search_field").html().includes(filterBy)){
                $(e).removeClass("hidden");
            }
            else {
                $(e).addClass("hidden");
            }
        })
    }
}