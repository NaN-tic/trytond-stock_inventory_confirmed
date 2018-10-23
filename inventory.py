# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import Workflow, ModelView
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Inventory']


class Inventory(metaclass=PoolMeta):
    __name__ = 'stock.inventory'

    @classmethod
    def __setup__(cls):
        super(Inventory, cls).__setup__()
        confirmed = ('confirmed', 'Confirmed')
        if confirmed not in cls.state.selection:
            cls.state.selection.append(confirmed)
        cls._transitions |= set((
                ('draft', 'confirmed'),
                ('confirmed', 'done'),
                ('confirmed', 'draft'),
                ('confirmed', 'cancel'),
                ))
        cls._buttons.update({
                'draft': {
                    'invisible': Eval('state') != 'confirmed',
                    },
                'confirm': {
                    'invisible': Eval('state') != 'confirmed',
                    },
                'cancel': {
                    'invisible': Eval('state').in_(['cancel', 'done']),
                    },
                'first_confirm': {
                    'invisible': Eval('state') != 'draft',
                    },
                })

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmed')
    def first_confirm(self, inventories):
        pass

    @classmethod
    @ModelView.button
    @Workflow.transition('draft')
    def draft(self, inventories):
        pass
