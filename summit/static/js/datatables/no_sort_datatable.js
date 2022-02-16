$(document).ready(function ()
    {
        $('.dtBasicExample').DataTable({
            retrieve: true,
            "paging":   false,
            'ordering': true,
            'info': false,
            "dom": '<"top"f>r<"bottom"litp><"clear">',
            "scrollY": "400px",
            "scrollCollapse": true,
            "scroller": true,
            "deferRender": true,
        });
        $('.dataTables_filter').addClass('pull-left');
    });

