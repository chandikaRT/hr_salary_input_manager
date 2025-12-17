from odoo import models, fields

class PayrollInputSheet(models.Model):
    _name = 'hr.payroll.input.sheet'
    _description = 'Payroll Input Sheet'

    name = fields.Char('Description', compute='_compute_name')
    month = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string='Month', required=True)
    year = fields.Integer('Year', required=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    line_ids = fields.One2many('hr.payroll.input.sheet.line', 'sheet_id', string='Lines')

    def _compute_name(self):
        for rec in self:
            rec.name = f"Payroll Inputs {rec.month}/{rec.year}"

class PayrollInputSheetLine(models.Model):
    _name = 'hr.payroll.input.sheet.line'
    _description = 'Payroll Input Sheet Line'

    sheet_id = fields.Many2one('hr.payroll.input.sheet', string='Sheet')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    input_name = fields.Char('Input Name', required=True)
    amount = fields.Float('Amount', required=True)
    applied = fields.Boolean('Applied', default=False)
