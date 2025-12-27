{
    'name': 'API',
    'version': '19.0.1.0.0',
    'summary': 'A module to provide a CRUD API',
    'description': 'This module provides a basic CRUD API for a simple model.',
    'author': 'Gemini',
    'website': 'https://www.google.com',
    'category': 'Uncategorized',
    'depends': ['base', 'website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/item_views.xml',
        'report/cli_report.xml',
        'report/cli_report_template.xml',
        'wizard/cli_wizard_views.xml',
        'views/cli_record_views.xml',
        'views/templates.xml',
        'views/dashboard.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_web': [
            'cli/static/src/dashboard.js',
            'cli/static/src/dashboard.xml',
            'cli/static/src/dashboard_action.js',
        ],
    },
    'installable': True,
    'application': True,
}
