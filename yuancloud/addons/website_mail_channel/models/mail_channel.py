# -*- coding: utf-8 -*-

from yuancloud.osv import osv
from yuancloud.tools.safe_eval import safe_eval as eval
from yuancloud.addons.website.models.website import slug


class MailGroup(osv.Model):
    _inherit = 'mail.channel'

    def message_get_email_values(self, cr, uid, id, notif_mail=None, context=None):
        res = super(MailGroup, self).message_get_email_values(cr, uid, id, notif_mail=notif_mail, context=context)
        group = self.browse(cr, uid, id, context=context)
        base_url = self.pool['ir.config_parameter'].get_param(cr, uid, 'web.base.url')
        headers = {}
        if res.get('headers'):
            try:
                headers = eval(res['headers'])
            except Exception:
                pass
        headers.update({
            'List-Archive': '<%s/groups/%s>' % (base_url, slug(group)),
            'List-Subscribe': '<%s/groups>' % (base_url),
            'List-Unsubscribe': '<%s/groups?unsubscribe>' % (base_url,),
        })
        res['headers'] = repr(headers)
        return res
