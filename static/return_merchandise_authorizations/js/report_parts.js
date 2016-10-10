/**
 * Created by marc on 11/10/2014.
 */
function pad(number, length) {

    var str = '' + number;
    while (str.length < length) {
        str = '0' + str;
    }

    return str;

}
$(function() {
    $( "#id_start_date" ).datepicker({ dateFormat: "mm/dd/yy" });
    $( "#id_end_date" ).datepicker({ dateFormat: "mm/dd/yy" });

    $('#search-for-returned-items-in-period').click(function (e) {
        part_id = $("select#id_part").val();
        start_date = $("input#id_start_date").val();
        ds = new Date(start_date);
        if (ds.getMonth() == 0) {
            start_month = 'jan';
        }
        if (ds.getMonth() == 1) {
            start_month = 'feb';
        }
        if (ds.getMonth() == 2) {
            start_month = 'mar';
        }
        if (ds.getMonth() == 3) {
            start_month = 'apr';
        }
        if (ds.getMonth() == 4) {
            start_month = 'may';
        }
        if (ds.getMonth() == 5) {
            start_month = 'jun';
        }
        if (ds.getMonth() == 6) {
            start_month = 'jul';
        }
        if (ds.getMonth() == 7) {
            start_month = 'aug';
        }
        if (ds.getMonth() == 8) {
            start_month = 'sep';
        }
        if (ds.getMonth() == 9) {
            start_month = 'oct';
        }
        if (ds.getMonth() == 10) {
            start_month = 'nov';
        }
        if (ds.getMonth() == 11) {
            start_month = 'dec';
        }

        end_date = $("input#id_end_date").val();
        de = new Date(end_date);
        if (de.getMonth() == 0) {
            end_month = 'jan';
        }
        if (de.getMonth() == 1) {
            end_month = 'feb';
        }
        if (de.getMonth() == 2) {
            end_month = 'mar';
        }
        if (de.getMonth() == 3) {
            end_month = 'apr';
        }
        if (de.getMonth() == 4) {
            end_month = 'may';
        }
        if (de.getMonth() == 5) {
            end_month = 'jun';
        }
        if (de.getMonth() == 6) {
            end_month = 'jul';
        }
        if (de.getMonth() == 7) {
            end_month = 'aug';
        }
        if (de.getMonth() == 8) {
            end_month = 'sep';
        }
        if (de.getMonth() == 9) {
            end_month = 'oct';
        }
        if (de.getMonth() == 10) {
            end_month = 'nov';
        }
        if (de.getMonth() == 11) {
            end_month = 'dec';
        }
        url = '/'+services_parts_in_period_url+part_id+'/'+ds.getFullYear()+'/'+start_month+'/'+pad(ds.getDate(),2)+'/'+de.getFullYear()+'/'+end_month+'/'+pad(de.getDate(),2)+'/';

        // start spinner
        $('#wait-area').addClass( 'waiting div400x100' );
        $.get( url, function( data ) {
            $('div#parts-results').html(data);
        });
        // stop spinner
        $('#wait-area').removeClass( 'waiting div400x100' );
        e.preventDefault();
    });

    $('#id_part').change(function (e) {
        part_id = $("select#id_part").val();

        url = '/'+services_parts_all_time_url+part_id+'/';
        // start spinner
        $('#wait-area').addClass( 'waiting div400x100' );
        $.get( url, function( data ) {
            $('div#parts-results').html(data);
        });
        // stop spinner
        $('#wait-area').removeClass( 'waiting div400x100' );
        e.preventDefault();
    });

    $('#search-for-returned-items-by-quarter-by-site').click(function (e) {
        year = $("select#id_year").val();
        quarter = $("select#id_quarter").val();

        url = '/'+returned_parts_by_quarter_by_site+year+'/'+quarter+'/';
        // start spinner
        $('#wait-area').addClass( 'waiting div400x100' );
        $.get( url, function( data ) {
            $('div#parts-results').html(data);
        });
        // stop spinner
        $('#wait-area').removeClass( 'waiting div400x100' );
        e.preventDefault();
    });
});