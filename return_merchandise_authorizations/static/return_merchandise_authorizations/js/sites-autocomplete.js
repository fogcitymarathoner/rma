
/*
 * jQuery UI Autocomplete: Highlight Matched Text
 * http://salman-w.blogspot.com/2013/12/jquery-ui-autocomplete-examples.html
 */

$(function() {

    $("#autocomplete").autocomplete({
        source: sites
    }).data("ui-autocomplete")._renderItem = function(ul, item) {
        var $a = $("<a></a>").text(item.label);
        highlightText(this.term, $a);
        return $('<li class="ui-menu-item" ></li>').append($a).appendTo(ul);
    };
});