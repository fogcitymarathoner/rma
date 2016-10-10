
$(function() {


    $('#id_customer').change(function(e) {
            customer_id = $("select#id_customer").val();
            url = '/'+services_customers_rmas_url+customer_id
            $.get( url, function( data ) {
                $('div#customer-rma-results').html(data);
            });
            e.preventDefault();
    });
});