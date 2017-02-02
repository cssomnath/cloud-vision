$(document).ready(function() {
    $('#labeltable').DataTable( {
        "ajax": {
            "url": labeldata_path, 
            "dataSrc": ""
        },
        
        "order": [[ 0, "desc" ]],

        "columns": [
            { "data" : "score" },
            { "data" : "mid" },
            { "data" : "description" }
        ],

        "searching": false,
        "paging":   false,
        "info":     false
    } );
} );
