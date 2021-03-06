# -*- coding: utf-8 -*-
##############################################################################
#
#    yuancloud, Open Source Management Solution
#    Copyright (C) 2014 OmniaSolutions snc (www.omniasolutions.eu).
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
import time
from yuancloud.tools import DEFAULT_SERVER_DATETIME_FORMAT
import yuancloud.tools as tools

import logging
from yuancloud        import models, fields, api, SUPERUSER_ID, _, osv
_logger         =   logging.getLogger(__name__)

class report_plm_component(models.Model):
    _name = "report.plm_component"
    _description = "Report Component"
    _auto = False
    count_component_draft       =   fields.Integer(_('Draft'), readonly=True)
    count_component_confirmed   =   fields.Integer(_('Confirmed'), readonly=True)
    count_component_released    =   fields.Integer(_('Released'), readonly=True)
    count_component_modified    =   fields.Integer(_('Under Modify'), readonly=True)
    count_component_obsoleted   =   fields.Integer(_('Obsoleted'), readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'report_plm_component')
        cr.execute("""
            CREATE OR REPLACE VIEW report_plm_component AS (
                SELECT
                    (SELECT min(id) FROM product_template) as id,
                    (SELECT count(*) FROM product_template WHERE state = 'draft') AS count_component_draft,
                    (SELECT count(*) FROM product_template WHERE state = 'confirmed') AS count_component_confirmed,
                    (SELECT count(*) FROM product_template WHERE state = 'released') AS count_component_released,
                    (SELECT count(*) FROM product_template WHERE state = 'undermodify') AS count_component_modified,
                    (SELECT count(*) FROM product_template WHERE state = 'obsoleted') AS count_component_obsoleted
             )
        """)

report_plm_component()
