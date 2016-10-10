/**
 * Created by marc on 11/17/2014.
 */

$(document).ready(function() {

    // alternate row backgrounds
    $("table#keyword-table tr:even").css("background-color", "#F4F4F8");
    $("table#keyword-table tr:odd").css("background-color", "#EFF1F1");
    $("#add-extra-field").click( function(e)
    {
            $('input#new_field').val('yes');
    });
});