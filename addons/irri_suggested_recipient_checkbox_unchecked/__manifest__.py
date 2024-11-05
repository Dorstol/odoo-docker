{
    'name': 'IRRI Suggested Recipient Checkbox Unchecked',
    'version': '17.0.1.0.0',
    'category': 'Discuss',
    'summary': 'Unchecks suggested recipients by default in Odoo chatter.',
    'description': """
This module prevents the 'Suggested Recipients' checkboxes from being selected by default in the Odoo chatter, helping to avoid accidental notifications.
""",
    'author': 'IRRIGATOR',
    'website': 'https://irrigator.ua',
    'license': 'LGPL-3',
    'depends': ['mail'],
    'assets': {
        'web.assets_backend': [
            'irri_suggested_recipient_checkbox_unchecked/static/src/js/uncheck_suggested_recipients.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
