
$(document).ready(function(){
    $('a.back').click(function(){
        parent.history.back();
        return false;
    });
    // clean up drop down that's messed up using __unicode__ function of the model
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
