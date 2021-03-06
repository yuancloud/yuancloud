# -*- coding: utf-8 -*-
# Part of YuanCloud. See LICENSE file for full copyright and licensing details.


{
    'name': 'Portal Gamification',
    'version': '1',
    'category' : 'Tools',
    'complexity': 'easy',
    'description': """
This module adds security rules for gamification to allow portal users to participate to challenges
===================================================================================================
    """,
    'depends': ['gamification','portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/portal_security.xml',
    ],
    'installable': True,
    'auto_install': True,
    'category' : 'Hidden',
}
