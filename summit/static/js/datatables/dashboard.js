$(document).ready(function ()
{
    $('.dtBasicExample').DataTable({
        'pageLength': 100,
        'lengthMenu': [[10, 25, 50, 100, 500, 1000, -1], [10, 25, 50, 100, 500, 1000, "All"]]
    });
    $('.dataTables_length').addClass('bs-select');


    $('#select_all_1').click(function () {
        $('.export_list_1').prop("checked", !$('.export_list_1').prop("checked"));
        $('#select_all_1').prop("checked", $('.export_list_1').prop("checked"));
    });

    $('#select_all_2').click(function () {
        $('.export_list_2').prop("checked", !$('.export_list_2').prop("checked"));
        $('#select_all_1').prop("checked", $('.export_list_1').prop("checked"));
    });
});