odoo.define('stock.scanner.web', function (require) {
'use strict';

var core = require('web.core');
var form_common = require('web.form_common');
var Model = require('web.DataModel');
var data = require('web.data');
var ActionManager = require('web.ActionManager');

var StockScannerWidget = form_common.FormWidget.extend({
    template: "stock_scanner_web.StockScannerWidget",
});
core.form_custom_registry.add('stock_scanner_widget', StockScannerWidget);

return {
    StockScannerWidget: StockScannerWidget,
};

});