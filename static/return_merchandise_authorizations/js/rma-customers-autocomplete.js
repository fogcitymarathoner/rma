
/*
 * jQuery UI Autocomplete: Highlight Matched Text
 * http://salman-w.blogspot.com/2013/12/jquery-ui-autocomplete-examples.html
 */
/*
select customer from service and fill sites dropdown
 */
$(function() {

    $("#autocomplete").autocomplete({
        source: function(request, response) {
            //+'customers'
            //
                    url = customers_service_url+'rma_customer_dropdown_service/';
					$.getJSON(url, {
						// do not copy the api key; get your own at developer.rottentomatoes.com
						term: request.term
					}, function(data) {
						// data is an array of objects and must be transformed for autocomplete to use
						var array = data.error ? [] : $.map(data.customers, function(m) {
							return {
								label: m.id + ": " + m.name
							};
						});
                        //
						response(array);
					});
				},
        focus: function(event, ui) {
            // prevent autocomplete from updating the textbox
            event.preventDefault();
        },
        select: function(event, ui) {
            // customer selected, fill in site drop down
            selectedObj = ui.item;
            customer_name_raw = selectedObj.value;
            custSA = customer_name_raw.split(':');
            url = customers_sites_dropdown_url+custSA[0];
            $.get( url,function( data ) {
                $('select#id_name').html(data);
                $('select#id_name').show();
                $('label[for=id_name]').show();
                $('#id_customer').val(custSA[0]);
            });
            //event.preventDefault();
        }
    }).data("ui-autocomplete")._renderItem = function(ul, item) {
        var $a = $('<a></a>').text(item.label);
        highlightText(this.term, $a);
        return $('<li class="ui-menu-item" ></li>').append($a).appendTo(ul);
    };
});