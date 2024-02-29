{
    'name': 'To-Do',
    'version': '3.69',
    'description': 'A to-do module for Odoo',
    'summary': 'The goto to-do module.',
    'author': 'Ishwor',
    'website': 'https://youtube.com/',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/counter_client_action_views.xml'
    ],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend':[
            'todo_list/static/src/**/*.js',
            'todo_list/static/src/**/*.xml'
        ]
    }
}