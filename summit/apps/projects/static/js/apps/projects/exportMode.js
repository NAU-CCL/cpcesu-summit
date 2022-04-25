var export_switcher = false;
var table = $('#replace').DataTable({"paging": false});

$(document).ready(function(){
  table.column(0).visible(false);
  export_button = document.getElementById('export-button');
  export_button.style.display = "none";
})

var exportMode = function(){
  export_switcher_button = document.getElementById('export-mode-button');
  if (export_switcher){
    table.column(0).visible(false);
    export_button.style.display = "none"
    export_switcher = false;
    export_switcher_button.innerHTML = "Enable Export Mode"
  }
  else{
    table.column(0).visible(true);
    export_button.style.display = "block"
    export_switcher = true;
    export_switcher_button.innerHTML = "Cancel"
  }
}

$('#export-mode-button').on('click', exportMode)