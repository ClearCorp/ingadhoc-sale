# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import api, models, fields, _
from openerp.tools import float_compare
from openerp.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    type_invoice_policy = fields.Selection(
        related='type_id.invoice_policy',
        readonly=True,
    )

    @api.multi
    def action_invoice_create_force(self):
        self.ensure_one()
        for line in self.order_line:
            line.qty_to_invoice = line.product_uom_qty - line.qty_invoiced
        self.action_invoice_create()

    @api.multi
    def action_confirm(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for rec in self:
            if rec.type_invoice_policy == 'prepaid':
                invoice_status = rec.mapped(
                    'order_line.invoice_lines.invoice_id.state')
                if (set(invoice_status) - set(['paid'])) or any(
                        (float_compare(
                        line.product_uom_qty, line.qty_invoiced,
                        precision_digits=precision) > 0)
                        for line in rec.order_line):
                    raise UserError(_(
                        'If you use a sale type with invoice policy "Before '
                        'Delivery", then every sale line must be invoiced and '
                        'paid before you can confirm the sale order'))
        return super(SaleOrder, self).action_confirm()
