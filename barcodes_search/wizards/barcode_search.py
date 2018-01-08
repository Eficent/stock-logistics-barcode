# Copyright (C) 2017-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BarcodeSearch(models.TransientModel):
    _name = 'barcode.search'

    barcode = fields.Char(
        string='Barcode', required=True, help='Barcode to search for.')

    state = fields.Selection(
        selection=[('new', 'New'), ('done', 'Done')], default='new')

    line_ids = fields.One2many(
        comodel_name='barcode.search.line', inverse_name='barcode_search_id',
        readonly=True)

    @api.multi
    def button_search(self):
        self.ensure_one()
        res = self.search_by_barcode(self.barcode)
        if len(res) == 1 and not res[0][2]:
            # Display the result in the according form view
            record = res[0][1]
            return record.get_formview_action()
        else:
            # Update Wizard Values
            line_vals = []
            self.line_ids.unlink()
            for item in res:
                line_vals.append((0, 0, {
                    'field_id': item[0].id,
                    'item_id': item[1].id,
                    'item_name': item[1].name,
                    'extra_data': item[2],
                }))
            self.state = 'done'
            self.line_ids = line_vals

            # Return Action
            action = self.get_formview_action()
            action['target'] = 'new'
            return action

    @api.model
    def search_by_barcode(self, barcode):
        """Return a list of tuple (field, record, {extra_data})
        that matches with the given barcode
        """
        barcode_fields = self.get_barcode_fields()
        res = self._search_by_barcode_barcode_fields(
            barcode, barcode_fields)

        # Extra search for objects that have a barcode with encoded data
        # Typical exemple, product with a pattern 20{barcode_base}{NNDDD}
        # where {NNDDD} is the weight of the product
        nomenclature_obj = self.env['barcode.nomenclature']
        nomenclatures = nomenclature_obj.search([])
        rule_types = self.get_model_by_rule_type()
        for nomenclature in nomenclatures:
            parsed_result = nomenclature.parse_barcode(barcode)
            rule_type = parsed_result['type']
            if rule_type in rule_types:
                barcode_fields = self.get_barcode_fields(rule_types[rule_type])
                base_code = parsed_result['base_code']
                extra_results = self._search_by_barcode_barcode_fields(
                    base_code, barcode_fields)
                for extra_result in extra_results:
                    extra_result[2]['type'] = rule_type
                    extra_result[2]['value'] = parsed_result['value']
                res += extra_results
        return res

    @api.model
    def get_barcode_fields(self, model_name=False):
        """Return a recordset of fields that represent a barcode, in any model.
        By default, it will return all fields named 'barcode'.
        Note : Overload that function in a custom module, if you define
        a barcode field with a name different than 'barcode'"""
        field_obj = self.env['ir.model.fields']
        if model_name:
            domain = [
                ('name', '=', 'barcode'), ('model', '=', model_name)]
        else:
            domain = [
                ('name', '=', 'barcode'), ('model', '!=', 'barcode.search')]
        return field_obj.search(domain)

    @api.model
    def get_model_by_rule_type(self):
        """Return a dictionary of rule type: model
        for each special barcode nomenclature rule types, with  a pattern
        that belong a fixed part like '.....' and a variable part like {NNDDD}.
        Note : Overload that function in a custom module, if you define
        such new rule type.

        'weight' is define in Odoo / 'stock' module.
        'price' is define in Odoo / 'point_of_sale' module.
        'price_to_weight' is defined in OCA / 'pos_price_to weight' module
        """
        return {
            'weight': 'product.product',
            'price': 'product.product',
            'price_to_weight': 'product.product',
        }

    # Private Section
    @api.model
    def _search_by_barcode_barcode_fields(self, barcode, barcode_fields):
        res = []
        for barcode_field in barcode_fields:
            model_obj = self.env.get(barcode_field.model, False)
            if not type(model_obj) is bool:
                items = model_obj.search([(barcode_field.name, '=', barcode)])
                for item in items:
                    res.append((barcode_field, item, {}))
        return res
