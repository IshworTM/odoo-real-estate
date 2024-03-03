{
    'name': 'Student Management',
    'version': '3.02',
    'description': 'A system that manages student information.',
    'summary': 'Student management system for a school.',
    'author': 'Rowshi',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/student_management_views.xml',
        'views/student_optional_subjects.xml'
    ],
    'application': True,
    'installable' : True,
}