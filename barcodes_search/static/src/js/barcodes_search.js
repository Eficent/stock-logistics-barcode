odoo.define('barcodes_search.systray', function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');
    var Widget = require('web.Widget');

    ///**
    // * Menu item appended in the systray part of the navbar
    // On click : Display a barcode search form view
    // */
    var BarcodeSearchItem = Widget.extend({
        template:'barcodes_search.BarcodeSearchItem',
        events: {
            "click": "on_click",
        },

        on_click: function (event) {
            event.preventDefault();
            return this.do_action('barcodes_search.action_barcode_search_form');
        },

    });

    SystrayMenu.Items.push(BarcodeSearchItem);

});
