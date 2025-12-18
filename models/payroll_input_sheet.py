from odoo import models, fields, api
import base64
import xlrd

class PayrollInputSheet(models.Model):
    _name = 'hr.payroll.input.sheet'
    _description = 'Payroll Input Sheet'

    name = fields.Char(string='Reference', required=True, default='New')
    month = fields.Selection(
        [(str(i), str(i)) for i in range(1, 13)],
        required=True
    )
    year = fields.Integer(required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done')],
        default='draft'
    )

    line_ids = fields.One2many(
        'hr.payroll.input.sheet.line',
        'sheet_id',
        string='Lines'
    )

    # ------------------------------------------------------
    # Excel Import
    # ------------------------------------------------------
    def action_import_excel(self):
        self.ensure_one()

        if not self.import_file:
            return

        data = base64.b64decode(self.import_file)
        workbook = xlrd.open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)

        # Expected headers:
        # Employee Code | Input Name | Amount
        for row in range(1, sheet.nrows):
            emp_code = str(sheet.cell(row, 0).value).strip()
            input_name = str(sheet.cell(row, 1).value).strip()
            amount = float(sheet.cell(row, 2).value or 0.0)

            employee = self.env['hr.employee'].search(
                [('barcode', '=', emp_code)],
                limit=1
            )
            if not employee:
                continue

            self.env['hr.payroll.input.sheet.line'].create({
                'sheet_id': self.id,
                'employee_id': employee.id,
                'input_name': input_name,
                'amount': amount,
            })

        self.import_file = False
        self.import_filename = False

    # ------------------------------------------------------
    # Apply to Payslips
    # ------------------------------------------------------
    def action_apply_to_payslips(self):
        for sheet in self:
            for line in sheet.line_ids.filtered(lambda l: not l.applied):

                input_type = self.env['hr.salary.input'].search(
                    [('name', '=', line.input_name)],
                    limit=1
                )
                if not input_type:
                    input_type = self.env['hr.salary.input'].create({
                        'name': line.input_name,
                        'code': line.input_name.replace(' ', '_').upper(),
                    })

                payslips = self.env['hr.payslip'].search([
                    ('employee_id', '=', line.employee_id.id),
                    ('state', '=', 'draft'),
                ])

                for slip in payslips:
                    self.env['hr.payslip.input'].create({
                        'slip_id': slip.id,
                        'input_type_id': input_type.id,
                        'amount': line.amount,
                        'name': input_type.name,
                        'code': input_type.code,
                    })

                line.applied = True

            sheet.state = 'done'
