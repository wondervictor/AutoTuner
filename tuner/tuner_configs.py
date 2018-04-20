# -*- coding: utf-8 -*-
"""
description: Tuner's configurations
"""

config = {
    'num_actions': 16,
    'num_states': 63,
    'use_gpu': False,
    'epsilon': 0.2,
    'gamma': 0.85,
    'update_target': 20,
    'epoches': 100,
    'v': 16,
    'learning_rate': 0.001,
    'memory_size': 10000,
}

TENCENT_URL = "http://10.252.218.130:8080/cdb2/fun_logic/cgi-bin/public_api"
