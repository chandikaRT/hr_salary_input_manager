{
    "name": "HR Salary Input Sheet",
    "version": "1.0",
    "category": "Human Resources/Payroll",
    "summary": "Manage additional/deduction salary inputs and upload to payslips",
    "description": """
        Allows HR to manage additions and deductions for employees,
        manually or via Excel, and push them to payslips. Tracks all changes in an audit trail.
    """,
    "author": "Chandika Rathnayake",
    "depends": ["hr", "hr_payroll", "base", "board"],
    "data": [
        'security/ir.model.access.csv',
        'views/payroll_input_sheet_views.xml',
        'views/import_wizard_views.xml',
    ],
    "installable": True,
    "application": True,
}