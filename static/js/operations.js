/**
 * Created by marc on 12/5/2014.
 */

$(function() {
    $( "#nav-bar-rma-list-link" ).removeClass('active');
    $( "#nav-bar-commissioned-sites-link" ).removeClass('active');
    $( "#nav-bar-list-parts-link" ).removeClass('active');
    $( "#nav-bar-list-return-items-link" ).removeClass('active');
    $( "#nav-bar-admin-panel-link" ).removeClass('active');
    $( "#nav-bar-reports-dropdown" ).removeClass('active');
    $( "#nav-bar-operations-dropdown" ).addClass('active');
});
$('#redirect-to-assign-customer-to-site-new-customer').click(
    function(e)
    {
        window.location.replace('/'+assign_customer_to_site_new_customer+'/'+site_id);
        e.preventDefault()
    }
);

$('#redirect-to-assign-customer-select-customer').click(
    function(e)
    {
        window.location.replace('/'+assign_customer_select_customer+'/'+site_id);
        e.preventDefault()
    }
);

$('#run-selected-role-change').change(function() {
    role = $('select[name="role"]').val();
    if (role != 'NON-OP') {

        url = '/' + assign_role_url + id + '/' + role;
        $.get(url, function (data) {
            $('div#results').html(data);
        });
    }
    e.preventDefault();
});