# -*- coding: utf-8 -*-
# Part of YuanCloud. See LICENSE file for full copyright and licensing details.

from yuancloud import tools
from yuancloud.osv import fields, osv

class payslip_report(osv.osv):
    _name = "payslip.report"
    _description = "Payslip Analysis"
    _auto = False
    _columns = {
        'name':fields.char('Name', readonly=True),
        'date_from': fields.date('Date From', readonly=True,),
        'date_to': fields.date('Date To', readonly=True,),
        'year': fields.char('Year', size=4, readonly=True),
        'month': fields.selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'day': fields.char('Day', size=128, readonly=True),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ('cancel', 'Rejected'),
        ], 'Status', readonly=True),
        'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
        'nbr': fields.integer('# Payslip lines', readonly=True),
        'number': fields.char('Number', readonly=True),
        'struct_id': fields.many2one('hr.payroll.structure', 'Structure', readonly=True),
        'company_id':fields.many2one('res.company', 'Company', readonly=True),
        'paid': fields.boolean('Made Payment Order ? ', readonly=True),
        'total': fields.float('Total', readonly=True),
        'category_id':fields.many2one('hr.salary.rule.category', 'Category', readonly=True),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'payslip_report')
        cr.execute("""
            create or replace view payslip_report as (
                select
                    min(l.id) as id,
                    l.name,
                    p.struct_id,
                    p.state,
                    p.date_from,
                    p.date_to,
                    p.number,
                    p.company_id,
                    p.paid,
                    l.category_id,
                    l.employee_id,
                    sum(l.total) as total,
                    to_char(p.date_from, 'YYYY') as year,
                    to_char(p.date_from, 'MM') as month,
                    to_char(p.date_from, 'YYYY-MM-DD') as day,
                    to_char(p.date_to, 'YYYY') as to_year,
                    to_char(p.date_to, 'MM') as to_month,
                    to_char(p.date_to, 'YYYY-MM-DD') as to_day,
                    1 AS nbr
                from
                    hr_payslip as p
                    left join hr_payslip_line as l on (p.id=l.slip_id)
                where 
                    l.employee_id IS NOT NULL
                group by
                    p.number,l.name,p.date_from,p.date_to,p.state,p.company_id,p.paid,
                    l.employee_id,p.struct_id,l.category_id
            )
        """)
