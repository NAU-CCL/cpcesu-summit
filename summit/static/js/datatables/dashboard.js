$(document).ready(function ()
{
    $('.dtBasicExample').DataTable({
        'pageLength': 100,
        'lengthMenu': [[10, 25, 50, 100, 500, 1000, -1], [10, 25, 50, 100, 500, 1000, "All"]]
    });
    $('.dataTables_length').addClass('bs-select');


    $('#select_all').click(function () {
        // if (isChecked){
        $('.export_list').prop("checked", !$('.export_list').prop("checked"));
        // }
    });
});