from odoo import models, fields

class PayrollInputSheet(models.Model):
    _name = 'hr.payroll.input.sheet'
    _description = 'Payroll Input Sheet'

    name = fields.Char(string='Reference', default='New')
    month = fields.Selection([(str(i), str(i)) for i in range(1,13)], string='Month', required=True)
    year = fields.Integer(string='Year', required=True)
    line_ids = fields.One2many('hr.payroll.input.sheet.line','sheet_id', string='Input Lines')
    state = fields.Selection([('draft','Draft'),('done','Done')], default='draft')

class PayrollInputSheetLine(models.Model):
    _name = 'hr.payroll.input.sheet.line'
    _description = 'Payroll Input Sheet Line'

    sheet_id = fields.Many2one('hr.payroll.input.sheet', ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    input_name = fields.Char(string='Input Name', required=True)
    amount = fields.Monetary(string='Amount', currency_field='company_currency')
    company_currency = fields.Many2one('res.currency', related='employee_id.company_id.currency_id', readonly=True)
    applied = fields.Boolean(default=False)
