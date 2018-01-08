.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================
Search by Barcode
=================

This module expends Odoo functionality, allowing user to search any item by
it barcode.

Usage
=====

* In the main menu click on the barcode new button

.. image:: /barcodes_search/static/description/barcode_button_menu.png

* In the pop up form, enter the barcode and click on the search button

.. image:: /barcodes_search/static/description/partner_search.png
   :width: 800 px


1. If an item is found, the pop up is closed, and the form view of the item is
displayed.


2. In some specifics cases when the barcode contains extra data (like price
or weight), the barcode will be different than the product barcode.
In that case, the item is displayed, and the data is analysed.

Exemple : Barcode 2391000005002 when:

* 23 is a prefix
* 91000 is a base code of the product
* 00500 is the price
* 2 is a control digit

If this barcode is entered, the product with the barcode 2391000000007 will
be returned.

.. image:: /barcodes_search/static/description/price_product_search.png
   :width: 800 px


3. If many items are found, the list of the items are displayed and the user
   can go on the according form view by clicking on the button on the end of
   the line. This case can occur:

* in a normal case, if a barcode is associated to many models. Two typical
  cases are : product.product / product.template and res.users / res.partner.
* if the database is corrupted, and a barcode is set to many differents
  items.

.. image:: /barcodes_search/static/description/partner_user_search.png
   :width: 800 px

Technical Note
--------------

The search will be done on all the fields named ``barcode`` in any models.

For developers, there are one handy method in ``barcode.search`` as well:

.. code-block:: python

    result = self.env['barcode.search'].search_by_barcode('12345567890123')

.. code-block:: python

    @api.model
    def search_by_barcode(self, barcode):
        """Return the record associated with the barcode.

        Args:
            barcode (str): Barcode string to search for.

        Returns: a tuple (Field, BaseModel, ExtraData)
            Field: a record of the field that matched the search
            BaseModel: A record matching the barcode, if existing
            ExtraData: An optional dictionnary that provides extra informations
        """

Try On Runbot
-------------

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/150/11.0

Inheritance
===========

* If you want to make a search on a field that is not named 'barcode', you
  should overload the function ``get_barcode_fields`` of the model
  ``barcode.search``.

* If you want to implement another integration of extra data in a barcode
  via a rule, you should overload the function
  ``get_model_by_rule_type`` of the model ``barcode.search``.

For the time being, three rule types are handled:

- ``weight``, defined in Odoo ``stock`` module
- ``price``, defined in Odoo ``point_of_sale`` module
- ``price_to_weight``, defined in OCA ``pos_price_to weight`` module

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/stock-logistics-barcode/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted it
first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)
* Dave Lasley <dave@laslabs.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.

