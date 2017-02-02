$(document).ready(function() {
    $('#logotable').DataTable( {
        "ajax": {
            "url": logodata_path,
            "dataSrc": ""
        },
        
        "order": [[ 0, "desc" ]],

        "columns": [
            { "data" : "score" },
            { "data" : "description" }
        ],

        "searching": false,
        "paging":   false,
        "info":     false
    } );
} );
