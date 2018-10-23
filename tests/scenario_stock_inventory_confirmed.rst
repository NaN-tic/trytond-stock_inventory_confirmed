==================================
Stock Inventory Confirmed Scenario
==================================

=============
General Setup
=============

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts, create_tax
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> today = datetime.date.today()

Activate stock_inventory_confirmed::

    >>> config = activate_modules('stock_inventory_confirmed')

Create company::

    >>> _ = create_company()
    >>> company = get_company()
    >>> party = company.party

Get stock locations::

    >>> Location = Model.get('stock.location')
    >>> supplier_loc, = Location.find([('code', '=', 'SUP')])
    >>> storage_loc, = Location.find([('code', '=', 'STO')])
    >>> customer_loc, = Location.find([('code', '=', 'CUS')])

Create products::

    >>> ProductUom = Model.get('product.uom')
    >>> ProductTemplate = Model.get('product.template')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> template = ProductTemplate()
    >>> template.name = 'Product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.list_price = Decimal('300')
    >>> template.cost_price = Decimal('80')
    >>> template.cost_price_method = 'average'
    >>> template.save()
    >>> product, = template.products

Create an inventory::

    >>> Inventory = Model.get('stock.inventory')
    >>> inventory = Inventory()
    >>> inventory.location = storage_loc
    >>> line = inventory.lines.new()
    >>> line.product = product
    >>> line.quantity = 3.0
    >>> inventory.click('first_confirm')
    >>> inventory.state
    u'confirmed'

Moves are not created until the inventory is done::

    >>> StockMove = Model.get('stock.move')
    >>> moves = StockMove.find([('product', '=', product.id)])
    >>> len(moves)
    0
    >>> inventory.click('confirm')
    >>> inventory.state
    u'done'
    >>> move, = StockMove.find([('product', '=', product.id)])
    >>> move.quantity
    3.0

A confirmed inventory can be reset to draft::

    >>> inventory = Inventory()
    >>> inventory.location = storage_loc
    >>> line = inventory.lines.new()
    >>> line.product = product
    >>> line.quantity = 3.0
    >>> inventory.click('first_confirm')
    >>> inventory.state
    u'confirmed'
    >>> inventory.click('draft')
    >>> inventory.state
    u'draft'
