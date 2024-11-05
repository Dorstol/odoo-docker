{
    'name': 'IRRIGATOR Export Survey Attachments',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Export survey attachments grouped by respondent nickname for IRRIGATOR',
    'author': 'IRRIGATOR',
    'website': 'https://irrigator.ua/',
    'license': 'AGPL-3',
    'depends': ['survey'],
    'data': [
        'security/ir.model.access.csv',
        'views/export_survey_attachment_wizard_view.xml',
        'views/survey_user_input_views.xml',
    ],
    'iamges': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
}
