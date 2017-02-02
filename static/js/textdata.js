$(document).ready(function() {
    $('#texttable').DataTable( {
        "ajax": {
            "url": textdata_path,
            "dataSrc": ""
        },
        
        "order": [[ 0, "desc" ]],

        "columns": [
            { "data" : "locale" },
            { "data" : "description" },

        ],

        "searching": false,
        "paging":   false,
        "info":     false
    } );
} );
