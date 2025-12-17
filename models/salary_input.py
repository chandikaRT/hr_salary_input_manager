from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SalaryInput(models.Model):
    _name = "hr.salary.input"
    _description = "Employee Salary Inputs"

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    input_type_id = fields.Many2one('hr.salary.rule', string='Input Type', required=True)
    amount = fields.Float(string='Amount', required=True)
    payslip_id = fields.Many2one('hr.payslip', string='Payslip')
    date = fields.Date(string='Date', default=fields.Date.context_today)
    uploaded_by = fields.Many2one('res.users', string='Uploaded By', default=lambda self: self.env.user)
    state = fields.Selection([('draft', 'Draft'), ('uploaded', 'Uploaded')], default='draft')
    audit_log = fields.One2many('hr.salary.input.audit', 'salary_input_id', string='Audit Trail')

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Amount cannot be negative.")

    def upload_to_payslip(self, payslip):
        for record in self:
            if record.state != 'draft':
                continue
            line_vals = {
                'name': record.input_type_id.name,
                'code': record.input_type_id.code,
                'category_id': record.input_type_id.category_id.id,
                'salary_rule_id': record.input_type_id.id,
                'amount': record.amount,
                'contract_id': record.employee_id.contract_id.id,
                'employee_id': record.employee_id.id,
                'slip_id': payslip.id,
            }
            self.env['hr.payslip.line'].create(line_vals)
            record.state = 'uploaded'
            record.payslip_id = payslip.id
            self.env['hr.salary.input.audit'].create({
                'salary_input_id': record.id,
                'changed_by': self.env.user.id,
                'old_value': 0,
                'new_value': record.amount,
            })
