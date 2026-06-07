{
    'name': "Employee Equpiment Request",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base','hr_contract','mail'],
    'author': "Ahmed",
    'category': 'Category',
    'description': """
    Description text
    """,
# data files always loaded at installation
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/equipment_excel_wizard_view.xml',
        'data/sequence.xml',
        'data/cron_data.xml',
        'views/hr_employee.xml',
        'views/base_menu.xml',
        'views/employee_equipment_request.xml',
        'wizard/reject_request_view.xml',
        'reports/equipment_report.xml',
        ],
    # data files containing optionally loaded demonstration data
    'application': True,
}