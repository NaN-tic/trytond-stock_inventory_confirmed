# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .inventory import *


def register():
    Pool.register(
        Inventory,
        module='stock_inventory_confirmed', type_='model')
