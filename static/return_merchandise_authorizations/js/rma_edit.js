$(function() {
    // setup date picker
    $("#id_date" ).datepicker({ dateFormat: "yy-mm-dd" });
    // set company drop down to correct company
    $('#id_company_name').val(customer_id);  // To select via value;
    // select site
    url = customers_sites_dropdown_url+customer_id;
    $.get( url,function( data ) {
        $('select#id_name').html(data);
        $('select#id_name').val(site_id);
    });

    $('#id_company_name').change(function() {
        url = customers_sites_dropdown_url+$(this).val();
        $.get( url,function( data ) {
            $('select#id_name').html(data);
            $('select#id_name').val('');
        });
    });
    function validateRmaForm(e){
        site = $('#id_name');
        selected_site_number = site.val();
        if (selected_site_number == "") {
            alert('You must select a site');
            e.preventDefault();
        }
        part0 = $('#id_part_0').find("option:selected").text();
        part1 = $('#id_part_1').find("option:selected").text();
        part2 = $('#id_part_2').find("option:selected").text();
        part0_quant = $('#id_quantity_0').val();
        part1_quant = $('#id_quantity_1').val();
        part2_quant = $('#id_quantity_2').val();
        if(part0 != '---------' && (part0_quant == 'null' || part0_quant == 0))
        {
            alert('Please Select a Quantity for your first part selected part '+part0);
            e.preventDefault();
        }
        if(part1 != '---------' && (part1_quant == 'null' || part1_quant == 0))
        {
            alert('Please Select a Quantity for your second part selected part'+part1);
            e.preventDefault();
        }
        if(part2 != '---------' && (part2_quant == 'null' || part2_quant == 0))
        {
            alert('Please Select a Quantity for your third part selected part'+part2);
            e.preventDefault();
        }
    }
    $('#submit-create-rma-selected-site').click(
        /*
        do some light form validation here, making sure select parts have quantities
         */
        function(e) {
            validateRmaForm(e);
        }
    );
    $('#submit-edit-rma-selected-site').click(
        /*
        do some light form validation here, making sure select parts have quantities
         */
        function(e) {
            validateRmaForm(e);
        }
    );

    $('#add-return-item').click(
        function(e)
        {
            rowCount = $('#return-items tr').length;
            url = '/'+returned_item_form_url+(rowCount/3+1);
            $.get( url, function( data ) {
                $('#return-items tr:last').after( data );
                // alternate row backgrounds
                $("table#return-items tr:even").css("background-color", "#F4F4F8");
                $("table#return-items tr:odd").css("background-color", "#EFF1F1");
            });
            e.preventDefault()
        }
    );
    // stop enter in inputs from submitting form
    $('form input:not([type="submit"])').keydown(function(e) {
        var keyCode = e.keyCode || e.which;

        if (keyCode == 13) {
            return false;
        }
    });
    // alternate row backgrounds
    $("table#return-items tr:even").css("background-color", "#F4F4F8");
    $("table#return-items tr:odd").css("background-color", "#EFF1F1");
    $( "#id_approved_on" ).datepicker({ dateFormat: "yy-mm-dd" });
    $('#id_date').change(function () {
        $('#id_reference_number').val($('#id_date').val()+$('#id_case_number').val());
    });
    $('#id_case_number').change(function () {
            $('#id_reference_number').val($('#id_date').val() + $('#id_case_number').val());
     }
    );
    $(function() {
        $("#id_part option").each(function(i){
            if ($(this).text() != '---------') {
                desA1 = $(this).text().split(',');
                desA2 = desA1[0].split(',');
                desA22 = desA1[1].split(',');
                desA3 = desA2[0].split(':');
                desA32 = desA22[0].split(':');
                $(this).text(desA3[1] + '-' + desA32[1]);
            }
        });
    });
});