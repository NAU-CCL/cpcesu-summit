$(document).ready(function ()
    {
        $('.dtBasicExample').DataTable({
            retrieve: true,
            'ordering': true,
            "dom": '<"top"f>r<"bottom"litp><"clear">'
        });
        $('.dataTables_filter').addClass('pull-left');
        $('.dataTables_paginate').addClass('pull-left');
    });

