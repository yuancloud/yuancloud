# -*- coding: utf-8 -*-
##############################################################################
#
#    YuanCloud, Run your business
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from yuancloud import models, fields, _
from yuancloud import exceptions


class DocumentPageShowDiff(models.TransientModel):
    """Display Difference for History."""

    _name = 'wizard.document.page.history.show_diff'

    def get_diff(self):
        """Return the Difference between two document."""
        history = self.env["document.page.history"]
        ids = self.env.context.get('active_ids', [])

        diff = ""
        if len(ids) == 2:
            if ids[0] > ids[1]:
                diff = history.getDiff(ids[1], ids[0])
            else:
                diff = history.getDiff(ids[0], ids[1])
        elif len(ids) == 1:
            old = history.browse(ids[0])
            nids = history.search(
                [('page_id', '=', old.page_id.id)],
                order='id DESC',
                limit=1
            )
            diff = history.getDiff(ids[0], nids.id)
        else:
            raise exceptions.Warning(
                _("Select one or maximum two history revisions!")
            )
        return diff

    diff = fields.Text(
        'Diff',
        readonly=True,
        default=get_diff
    )
