function pageify(){
    $('.dtBasicExample').DataTable({
        retrieve: true,
        'ordering': true,
        "dom": '<"top"f>r<"bottom"litp><"clear">',
    });
    $('.dataTables_filter').addClass('pull-left');
}
$(document).ready(function ()
{

$(document.getElementById("project")).addClass("tab-background")
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