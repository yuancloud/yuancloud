# -*- coding: utf-8 -*-
# Part of YuanCloud. See LICENSE file for full copyright and licensing details.

from yuancloud import api
from yuancloud.osv import osv, fields
from itertools import groupby


def grouplines(self, ordered_lines, sortkey):
    """Return lines from a specified invoice or sale order grouped by category"""
    grouped_lines = []
    for key, valuesiter in groupby(ordered_lines, sortkey):
        group = {}
        group['category'] = key
        group['lines'] = list(v for v in valuesiter)

        if 'subtotal' in key and key.subtotal is True:
            group['subtotal'] = sum(line.price_subtotal for line in group['lines'])
        grouped_lines.append(group)

    return grouped_lines


class SaleLayoutCategory(osv.Model):
    _name = 'sale_layout.category'
    _order = 'sequence, id'
    _columns = {
        'name': fields.char('Name', required=True, translate=True),
        'sequence': fields.integer('Sequence', required=True),
        'subtotal': fields.boolean('Add subtotal'),
        'separator': fields.boolean('Add separator'),
        'pagebreak': fields.boolean('Add pagebreak')
    }

    _defaults = {
        'subtotal': True,
        'separator': True,
        'pagebreak': False,
        'sequence': 10
    }


class AccountInvoice(osv.Model):
    _inherit = 'account.invoice'

    def sale_layout_lines(self, cr, uid, ids, invoice_id=None, context=None):
        """
        Returns invoice lines from a specified invoice ordered by
        sale_layout_category sequence. Used in sale_layout module.

        :Parameters:
            -'invoice_id' (int): specify the concerned invoice.
        """
        ordered_lines = self.browse(cr, uid, invoice_id, context=context).invoice_line_ids
        # We chose to group first by category model and, if not present, by invoice name
        sortkey = lambda x: x.sale_layout_cat_id if x.sale_layout_cat_id else ''

        return grouplines(self, ordered_lines, sortkey)


import yuancloud

class AccountInvoiceLine(osv.Model):
    _inherit = 'account.invoice.line'
    _order = 'invoice_id, categ_sequence, sequence, id'

    sale_layout_cat_id = yuancloud.fields.Many2one('sale_layout.category', string='Section')
    categ_sequence = yuancloud.fields.Integer(related='sale_layout_cat_id.sequence',
                                            string='Layout Sequence', store=True)

class SaleOrder(osv.Model):
    _inherit = 'sale.order'

    def sale_layout_lines(self, cr, uid, ids, order_id=None, context=None):
        """
        Returns order lines from a specified sale ordered by
        sale_layout_category sequence. Used in sale_layout module.

        :Parameters:
            -'order_id' (int): specify the concerned sale order.
        """
        ordered_lines = self.browse(cr, uid, order_id, context=context).order_line
        sortkey = lambda x: x.sale_layout_cat_id if x.sale_layout_cat_id else ''

        return grouplines(self, ordered_lines, sortkey)


class SaleOrderLine(osv.Model):
    _inherit = 'sale.order.line'
    _columns = {
        'sale_layout_cat_id': fields.many2one('sale_layout.category',
                                              string='Section'),
        'categ_sequence': fields.related('sale_layout_cat_id',
                                         'sequence', type='integer',
                                         string='Layout Sequence', store=True)
        #  Store is intentionally set in order to keep the "historic" order.
    }

    _order = 'order_id, categ_sequence, sale_layout_cat_id, sequence, id'

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Save the layout when converting to an invoice line."""
        invoice_vals = super(SaleOrderLine, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
        if line.sale_layout_cat_id:
            invoice_vals['sale_layout_cat_id'] = line.sale_layout_cat_id.id
        if line.categ_sequence:
            invoice_vals['categ_sequence'] = line.categ_sequence
        return invoice_vals

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.sale_layout_cat_id:
            res['sale_layout_cat_id'] = self.sale_layout_cat_id.id
        return res
