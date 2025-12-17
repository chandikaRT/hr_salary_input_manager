from odoo import models, fields, api
import base64
import xlrd

class ImportPayrollInputWizard(models.TransientModel):
    _name = 'hr.payroll.input.import.wizard'
    _description = 'Import Payroll Inputs from Excel'

    file = fields.Binary('Excel File', required=True)
    filename = fields.Char('File Name')
    month = fields.Selection([(str(i), str(i)) for i in range(1, 13)], string="Month", required=True)
    year = fields.Integer('Year', required=True)
    sheet_ref = fields.Many2one('hr.payroll.input.sheet', string='Payroll Input Sheet')

    def action_import(self):
        self.ensure_one()
        if not self.file:
            return
        data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)

        lines = []
        for row in range(1, sheet.nrows):
            employee_code = sheet.cell(row, 0).value
            input_name = sheet.cell(row, 1).value
            amount = sheet.cell(row, 2).value

            employee = self.env['hr.employee'].search([('barcode', '=', employee_code)], limit=1)
            if employee:
                lines.append((0, 0, {
                    'employee_id': employee.id,
                    'input_name': input_name,
                    'amount': amount,
                }))

        payroll_sheet = self.env['hr.payroll.input.sheet'].create({
            'month': self.month,
            'year': self.year,
            'line_ids': lines,
        })
        self.sheet_ref = payroll_sheet
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payroll Input Sheet',
            'res_model': 'hr.payroll.input.sheet',
            'view_mode': 'form',
            'res_id': payroll_sheet.id,
            'target': 'current',
        }

    def action_create_inputs(self):
        self.ensure_one()
        if not self.sheet_ref:
            return
        for line in self.sheet_ref.line_ids:
            input_type = self.env['hr.salary.input'].search([('name', '=', line.input_name)], limit=1)
            if not input_type:
                input_type = self.env['hr.salary.input'].create({'name': line.input_name})
            payslips = self.env['hr.payslip'].search([
                ('employee_id', '=', line.employee_id.id),
                ('date_from', '>=', f'{self.year}-{self.month}-01'),
                ('date_to', '<=', f'{self.year}-{self.month}-31'),
            ])
            for slip in payslips:
                self.env['hr.payslip.input'].create({
                    'name': input_type.name,
                    'amount': line.amount,
                    'slip_id': slip.id,
                    'code': input_type.code,
                })
