{
    "name": "HR Salary Input Manager",
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
        "security/hr_salary_input_security.xml",
        "security/ir.model.access.csv",
        "views/salary_input_views.xml",
        "views/salary_input_wizard_views.xml",
    ],
    "installable": True,
    "application": True,
}
