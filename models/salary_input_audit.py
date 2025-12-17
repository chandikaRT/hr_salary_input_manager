from odoo import models, fields

class SalaryInputAudit(models.Model):
    _name = "hr.salary.input.audit"
    _description = "Salary Input Audit Trail"

    salary_input_id = fields.Many2one('hr.salary.input', string='Salary Input', required=True)
    changed_by = fields.Many2one('res.users', string='Changed By')
    old_value = fields.Float(string='Old Value')
    new_value = fields.Float(string='New Value')
    timestamp = fields.Datetime(string='Timestamp', default=lambda self: fields.Datetime.now())
