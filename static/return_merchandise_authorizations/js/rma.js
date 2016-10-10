/**
 * Created by marc on 10/29/2014.
 */
function newPopup(url) {
    popupWindow = window.open(
        url,'popUpWindow','height=700,width=800,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}


$(function() {
    $('#select-all-return-items').click(function () {
        if ($('#select-all-return-items').prop('checked')) {

            $('#returned-items-list').find(':checkbox').each(function(){
                jQuery(this).prop('checked', true);
            });
        } else {

            $('#returned-items-list').find(':checkbox').each(function(){
                jQuery(this).prop('checked', false);
            });
        }
    });
});
/*
START - Confirm parts move
 */

$(function() {
    $('#select-all-return-items-confirm').click(function () {
        if ($('#select-all-return-items-confirm').prop('checked')) {

            $('#returned-items-list-confirm').find(':checkbox').each(function(){
                jQuery(this).prop('checked', true);
            });
        } else {

            $('#returned-items-list-confirm').find(':checkbox').each(function(){
                jQuery(this).prop('checked', false);
            });
        }
    });
});
    /*
    END - Confirm parts move
     */

