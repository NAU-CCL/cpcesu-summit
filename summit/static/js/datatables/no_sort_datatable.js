$(document).ready(function ()
    {
        $('.dtBasicExample').DataTable({
            retrieve: true,
            "paging":   false,
            'ordering': true,
            'info': false,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        });
        $('.dataTables_filter').addClass('pull-left');
    });

