# Copyright (C) 2017-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Search By Barcode',
    'summary': 'Search any item by it barcode',
    'version': '11.0.1.0.1',
    'category': 'Tools',
    'author':
        'GRAP, '
        'LasLabs, '
        'Odoo Community Association (OCA)',
    'website': 'https://www.odoo-community.org',
    'license': 'AGPL-3',
    'depends': [
        'barcodes',
        'product',
    ],
    'data': [
        'views/templates.xml',
        'wizards/barcode_search_view.xml',
    ],
    'qweb': [
        'static/src/xml/barcodes_search.xml',
    ],
    'demo': [
        'demo/res_partner.xml',
        'demo/product_product.xml',
    ],
    'images': [
        'static/description/barcode_button_menu.png',
        'static/description/partner_search.png',
        'static/description/partner_user_search.png',
        'static/description/price_product_search.png',
    ],
}
