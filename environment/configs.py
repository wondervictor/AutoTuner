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
    'tencent0': {
        'server_url': 'http://10.249.84.215:8080/cdb2/fun_logic/cgi-bin/public_api',
        'instance_id': 'e9d1725f-6d4e-11e8-8728-283152b07750',
        'host': '100.121.152.99',
        'port': 20120,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang',
        'memory': 8589934592
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
    },
    'tencent2': {
        'server_url': 'http://10.249.84.215:8080/cdb2/fun_logic/cgi-bin/public_api',
        'instance_id': '5130c91f-75f0-11e8-8728-283152b07750',
        'host': '100.121.150.87',
        'port': 20132,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang',
        'memory': 12884901888
    },
    'tencentNVME-SH': {
        'server_url': 'http://10.249.84.215:8080/cdb2/fun_logic/cgi-bin/public_api',
        'instance_id': 'cc6b7527-8574-11e8-8728-283152b07750',
        'host': '9.28.173.157',
        'port': 20120,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang',
        'memory': 751619276800
    },
    'tencentNVME-TJ': {
        'server_url': 'http://10.249.84.215:8080/cdb2/fun_logic/cgi-bin/public_api',
        'instance_id': '2018f2a7-959d-11e8-8728-283152b07750',
        'host': '9.20.42.29',
        'port': 20120,
        'passwd': '123456',
        'user': 'root',
        'operator': 'zakijzhang',
        'memory': 751619276800
    },
}



