$(document).ready(function ()
{
  console.log("hey")

      $('.dataTables_filter').addClass('pull-left');


$(document.getElementById("upload")).addClass("tab-background")
$(document.getElementById("project")).removeClass("tab-background")
$(document.getElementById("contentBody")).addClass("content-background");

  $('#select_all_1').click(function () {
      $('.export_list_1').prop("checked", !$('.export_list_1').prop("checked"));
      $('#select_all_1').prop("checked", $('.export_list_1').prop("checked"));
  });

  $('#select_all_2').click(function () {
      $('.export_list_2').prop("checked", !$('.export_list_2').prop("checked"));
      $('#select_all_1').prop("checked", $('.export_list_1').prop("checked"));
  });
});