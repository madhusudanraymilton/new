{
    'name': 'Two-Layer Time Off Approval System',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Time Off',
    'summary': 'Two-layer approval workflow for time off requests (Team Leader → HR Manager)',
    'description': """
        Two-Layer Time Off Approval System
        ===================================
        * Team Leader approval as first layer
        * HR Manager/Admin approval as second layer
        * State-based workflow: confirm → validate1 → validate
        * Role-based access control
        * Record rules for team visibility
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['hr_holidays'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hr_leave_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}