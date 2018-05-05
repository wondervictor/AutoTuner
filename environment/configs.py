# -*- coding: utf-8 -*-

"""
description: MySQL Database Configurations
"""

docker_config = {
    'mysql1': {
        'host': '192.168.0.11',
        'user': 'root',
        'passwd': '12345678',
        'port': 3306,
        'database': 'data'
    },
    'mysql2': {
        'host': '192.168.0.15',
        'user': 'root',
        'passwd': '12345678',
        'port': 3306,
        'database': 'data'
    },
}


server_config = {
    'mysql1': {
        'instance_id': 'e1ecd360-3d3f-11e8-b828-70e2840ca2fd',
        'host': '100.119.17.24',
        'port': 20149,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang'
    }
}
