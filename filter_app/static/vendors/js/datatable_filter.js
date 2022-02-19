function make_filtered_datatable(selector, ajax_source, columns, process_callback=false, custom_created_row=null) {
    let datatable = selector.DataTable({
        createdRow: function( row, data, dataIndex ) {
            if (custom_created_row !== null){
                console.log('create_row');
                custom_created_row(row, data, dataIndex);
            }
        },
        processing: true,
        serverSide: true,
        ordering: false,
        stateSave: true,
        scrollX: true,
        sDom: "rt<'row'<'col-md-5 col-sm-12'l><'col-md-7 col-sm-12'p>>",
        language: {
            paginate: {
                // remove previous & next text from pagination
                previous: '&nbsp;',
                next: '&nbsp;'
            },
            "lengthMenu": 'Show <select class="form-select">'+
                '<option value="10">10</option>'+
                '<option value="25">25</option>'+
                '<option value="50">50</option>'+
                '<option value="100">100</option>'+
                '</select> entries',
        },
        sAjaxSource: ajax_source,
        fnServerParams: function ( aoData ) {
            $('.filter-input, .filter-select, .filter-range').each(function (){
                let key = $(this).attr('id').replace("id_", "filter_");
                let value = $(this).val();
                aoData.push( { "name": key, "value": value } );
            });
        },
        columns: columns,
    }).on('page.dt', function () {
        $('html, body').animate({
            scrollTop: 0
        }, 300);
    });

    return datatable
}
