$(document).ready(function ()
{
    $('.dtBasicExample').DataTable({
        'pageLength': 100,
        'lengthMenu': [[10, 25, 50, 100, 500, 1000, -1], [10, 25, 50, 100, 500, 1000, "All"]]
    });
    $('.dataTables_length').addClass('bs-select');
});