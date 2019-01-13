function modifyShowAll() {
    var confirm = true;
    if (document.getElementById("filter-field").value === "")
        confirm = window.confirm("Show all restaurants? (slow query)");
    return confirm;
}

/*  START Mode nocturne/day */
'use strict';
$(document).ready(function () {
    var switchStatus = false;
    $("#switch-mode-light").on('change', function () {
        if ($(this).is(':checked')) {
            $("body").removeClass("day");
            $("body").addClass("night");
            $("#flip").css({
                'background-color': '#d6d8db',
                'color': '#212529'
            })
        }
        else {
            $("body").removeClass("night");
            $("body").addClass("day");
            $("#flip").css({
                'background-color': '#e5eecc'
            })
        }
    });
});

/*  END Mode nocturne/day */

// Cambiamos tamaño de letra
$(document).ready(function () {
    $("#button-font-size").click(function () {
        if ($("body").css("font-size") <= '20') {
            //console.log($("body").css("font-size"));
            $("body").css("font-size", "1.5rem");
        }
        else if ($("body").css("font-size") >= '14') {
            //console.log($("body").css("font-size"));
            $("body").css("font-size", "1rem");
        }
    });
});

// Cambiamos tipo de letra
$(document).ready(function () {
    $("#button-font-type").click(function () {
        console.log($("body").css("font-family"));
        var fontType = $("body").css("font-family");

        if (fontType.includes('-apple-system')) {
            $("body").css("font-family", "Verdana");
        } else {
            $("body").css("font-family", '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"');
        }
    });
});

// Changues list toggle
$(document).ready(function () {
    $("#flip").click(function () {
        $("#changes-panel").slideToggle("slow");
        var textFLip = $("#flip").text();
        if (textFLip.includes('Hide')) {
            $("#flip").text('Show changes\'s practice');
        } else
            $("#flip").text('Hide changes\'s practice');
    });
});

