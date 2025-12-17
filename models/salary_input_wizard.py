import base64
import io
import pandas as pd
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SalaryInputUploadWizard(models.TransientModel):
    _name = "hr.salary.input.upload.wizard"
    _description = "Upload Salary Inputs via Excel"

    file = fields.Binary(string="Excel File", required=True)
    filename = fields.Char(string="File Name")

    def import_file(self):
        if not self.file:
            raise ValidationError("Please upload a file.")

        data = base64.b64decode(self.file)
        df = pd.read_excel(io.BytesIO(data))

        for index, row in df.iterrows():
            employee = self.env['hr.employee'].search([('barcode', '=', str(row['Employee Code']))], limit=1)
            if not employee:
                raise ValidationError(f"Employee with code {row['Employee Code']} not found.")

            salary_rule = self.env['hr.salary.rule'].search([('name', '=', row['Input Type'])], limit=1)
            if not salary_rule:
                raise ValidationError(f"Salary Rule {row['Input Type']} not found.")

            self.env['hr.salary.input'].create({
                'employee_id': employee.id,
                'input_type_id': salary_rule.id,
                'amount': row['Amount'],
            })
        return {'type': 'ir.actions.act_window_close'}
