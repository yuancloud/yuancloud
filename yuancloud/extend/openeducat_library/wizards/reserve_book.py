# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from yuancloud import models, fields, api


class ReserveBook(models.TransientModel):

    """ Reserve Book """
    _name = 'reserve.book'

    partner_id = fields.Many2one('res.partner', required=True)

    @api.one
    def set_partner(self):
        self.env['op.book.movement'].browse(
            self.env.context.get('active_ids', False)).write(
            {'partner_id': self.partner_id.id,
             'reserver_name': self.partner_id.name, 'state': 'reserve'})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
