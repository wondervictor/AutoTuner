# -*- coding: utf-8 -*-

"""
description: MySQL Database Configurations
"""

instance_config = {
    'mysql1': {
        'host': '192.168.0.11',
        'user': 'root',
        'passwd': '12345678',
        'port': 3306,
        'database': 'data',
        'memory': 34359738368
    },
    'mysql2': {
        'host': '192.168.0.15',
        'user': 'root',
        'passwd': '12345678',
        'port': 3306,
        'database': 'data',
        'memory': 34359738368
    },

    'tencent1': {
        'server_url': 'http://10.249.84.215:8080/cdb2/fun_logic/cgi-bin/public_api',
        'instance_id': 'f9e4ebdd-6d4e-11e8-8728-283152b07750',
        'host': '100.121.150.87',
        'port': 20122,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang',
        'memory': 12884901888
    }

}



