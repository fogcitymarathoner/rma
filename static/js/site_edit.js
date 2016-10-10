$(function() {

    function validateSiteRmaMoveForm(e){
        site = $('#autocomplete');
        count = 0;
        for (x in sites){
            matching_candidate = sites[x]['value'];
            selected = site.val();
            sarray = selected.split(':');
            if(matching_candidate == selected){
                count = 1;
                $('#id_customer').val(sarray[0]);
                break;
            }
        }
        if (count == 0) {
            alert('You must select a site');
            e.preventDefault();
        }
    }

    $('#submit-new-site-selected-for-rma-moving').click(
        /*
        do some light form validation here, making sure select parts have quantities
         */
        function(e) {
            validateSiteRmaMoveForm(e);
        }
    );
});/**
 * Created by marc on 12/17/2014.
 */
