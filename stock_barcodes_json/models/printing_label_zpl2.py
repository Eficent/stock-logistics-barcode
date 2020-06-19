# Copyright (C) 2016 SYLEAM (<http://www.syleam.fr>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class PrintingLabelZpl2(models.Model):
    _inherit = "printing.label.zpl2"

    data_type = fields.Selection(selection_add=[("json", "JSON")])

    @api.model
    def _get_component_data(self, component, eval_args):
        data = super()._get_component_data(component, eval_args)
        # TODO implement all types in zpl module
        if not self.env.context.get("ld", False):
            return data
        if component.component_type == "text" and not component.only_product_barcode:
            data = ""
            for _, val in self.env.context.get("ld", False).items():
                if isinstance(val, (str)):
                    data += str(val) + " | "
        elif component.component_type == "code_128" or component.only_product_barcode:
            data_copy = data.copy()
            for key, val in data_copy.items():
                if key == "product_barcode":
                    data = val
        else:
            data = self.env.context.get("ld", False)
        return data

    def custom_fill_component(self, line):
        for component in self.component_ids.sorted("sequence"):
            if component.name == "Product Name":
                component.data = "str('%s')" % line.product_id.display_name
            elif component.name == "QRCode":
                component.data = {"product_id": line.product_id.id, "product_qty": line.product_qty,
                                  "uom_id": line.product_id.uom_id.id}
            elif component.name == "Qty + UoM":
                component.data = "str('%s')" % (str(line.product_qty) + " " + line.product_id.uom_id.name,)
            else:
                json = {
                    "product_barcode": line.product_barcode,
                    "lot_barcode": line.lot_barcode,
                    "uom": str(line.product_qty) + " " + line.product_id.uom_id.name,
                    "package_barcode": line.package_barcode,
                    "product_qty": line.product_qty,
                }
                component.data = json

    def print_label(self, printer, record, page_count=1, **extra):
        res = super().print_label(printer, record, page_count=1, **extra)
        for label in self:
            if label.data_type == "json":
                self.custom_fill_component(self.env.context.get("mapping"))
                # Send the label to printer
                label_contents = label._generate_zpl2_data(
                    label, page_count=page_count, **extra
                )
                printer.print_document(
                    report=None, content=label_contents, doc_format="raw"
                )
        return res
