from yuancloud import models, api, _, fields
import json


class ComponentDashboard(models.Model):
    _inherit = "product.product"

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_bom_dashboard_datas())

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')

    @api.multi
    def get_bom_dashboard_datas(self):
        number_documents = 0
        number_boms = 0
        if self.ids:
            plm_documents = self.get_related_docs()
            number_documents = len(plm_documents)
            boms = self.get_related_boms()
            number_boms = len(boms)
        return {
            'number_boms': number_boms,
            'number_documents': number_documents,
        }

    @api.multi
    def get_related_boms(self):
        return self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_tmpl_id.id)])

    @api.multi
    def get_related_docs(self):
        return self.browse(self.ids).linkeddocuments

    @api.multi
    def common_open(self, name, model, view_mode='form', view_type='form', res_id=False, ctx={}, domain=[]):
        # <field name="domain">[('account_id','=', active_id)]</field>
        return {
            'name': _(name),
            'type': 'ir.actions.act_window',
            'view_type': view_type,
            'view_mode': view_mode,
            'res_model': model,
            'res_id': res_id,
            'context': ctx,
            'domain': domain
        }

    @api.multi
    def toggle_favorite(self):
        self.write(
            {'show_on_dashboard': False if self.show_on_dashboard else True})
        return False

    @api.multi
    def open_action(self):
        print 'Pressed open action'
        return self.common_open(_('New Component'), 'product.product', 'form', 'form', self.ids[0], self.env.context)

    @api.multi
    def create_component(self):
        print 'New Component'
        return self.common_open(_('New Component'), 'product.product', 'form', 'form', False, self.env.context)

    @api.multi
    def open_normal_bom(self):
        print 'Open Normal Boms'
        boms = self.get_related_boms()
        domain = [('id', 'in', boms.ids), ('type', '=', 'normal')]
        return self.common_open(_('Related Boms'), 'mrp.bom', 'tree,form', 'form', boms.ids, self.env.context, domain)

    @api.multi
    def open_engin_bom(self):
        print 'Open Engineering Boms'
        boms = self.get_related_boms()
        domain = [('id', 'in', boms.ids), ('type', '=', 'ebom')]
        return self.common_open(_('Related Boms'), 'mrp.bom', 'tree,form', 'form', boms.ids, self.env.context, domain)

    @api.multi
    def open_spare_bom(self):
        print 'Open Spare Boms'
        boms = self.get_related_boms()
        domain = [('id', 'in', boms.ids), ('type', '=', 'spbom')]
        return self.common_open(_('Related Boms'), 'mrp.bom', 'tree,form', 'form', boms.ids, self.env.context, domain)

    @api.multi
    def open_new_component(self):
        print 'Open New Component'
        return self.common_open(_('New Component'), 'product.product', 'form', 'form', False, self.env.context)

    @api.multi
    def open_related_docs_action(self):
        docs = self.get_related_docs()
        domain = [('id', 'in', docs.ids)]
        return self.common_open(_('Related Documents'), 'plm.document', 'tree,form', 'form', docs.ids, self.env.context, domain)

    @api.multi
    def open_related_boms_action(self):
        print 'Open Related Boms'
        boms = self.get_related_boms()
        domain = [('id', 'in', boms.ids)]
        return self.common_open(_('Related Boms'), 'mrp.bom', 'tree,form', 'form', boms.ids, self.env.context, domain)

    @api.multi
    def create_normal_bom(self):
        print 'Open Normal Boms'
        context = self.env.context.copy()
        context.update({'default_type': 'normal'})
        docIds = self.get_related_docs()
        if docIds:
            context.update(
                {'default_product_tmpl_id': self.product_tmpl_id.id})
        return self.common_open(_('Related Boms'), 'mrp.bom', 'form', 'form', False, context)

    @api.multi
    def create_spare_bom(self):
        context = self.env.context.copy()
        context.update({'default_type': 'spbom'})
        docIds = self.get_related_docs()
        if docIds:
            context.update(
                {'default_product_tmpl_id': self.product_tmpl_id.id})
        return self.common_open(_('Related Boms'), 'mrp.bom', 'form', 'form', False, context)

    @api.multi
    def openDocument(self, vals=False):
        print 'Open document'

    @api.multi
    def report_components(self):
        pass

    def computePrevious(self, linkeddocs):
        print 'here'
        print linkeddocs
        pass


ComponentDashboard()
