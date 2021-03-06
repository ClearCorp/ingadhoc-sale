# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, models
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('sale_type_id')
    def onchange_sale_type_set_pay_now(self):
        if (
                self.sale_type_id.payment_atomation != 'none' and
                self.sale_type_id.payment_journal_id):
            self.pay_now_journal_id = self.sale_type_id.payment_journal_id.id
        else:
            self.pay_now_journal_id = False
