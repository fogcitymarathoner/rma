
/*
 * jQuery UI Autocomplete: Highlight Matched Text
 * http://salman-w.blogspot.com/2013/12/jquery-ui-autocomplete-examples.html
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
            // prevent autocomplete from updating the textbox
            //event.preventDefault();
            // navigate to the selected item's url
            //window.open(ui.item.url);
        }
    }).data("ui-autocomplete")._renderItem = function(ul, item) {
        var $a = $('<a></a>').text(item.label);
        highlightText(this.term, $a);
        return $('<li class="ui-menu-item" ></li>').append($a).appendTo(ul);
    };
});