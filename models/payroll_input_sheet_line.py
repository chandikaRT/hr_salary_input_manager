from odoo import models, fields

class PayrollInputSheetLine(models.Model):
    _name = 'hr.payroll.input.sheet.line'
    _description = 'Payroll Input Sheet Line'

    sheet_id = fields.Many2one('hr.payroll.input.sheet', string='Sheet', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    input_name = fields.Char('Input Name', required=True)
    amount = fields.Float('Amount', required=True)
    applied = fields.Boolean('Applied', default=False)