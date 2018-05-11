# -*- coding: utf-8 -*-
"""
desciption: Knob information

"""

import utils
import configs


memory_size = 32*1024*1024*1024
instance_name = ''

KNOBS = ['skip_name_resolve',               # OFF
         'table_open_cache',                # 2000
         'max_connections',                 # 151
         'innodb_buffer_pool_size',         # 134217728
         'innodb_buffer_pool_instances',    # 8
         'innodb_log_files_in_group',       # 2
         'innodb_log_file_size',            # 50331648
         'innodb_purge_threads',            # 1
         'innodb_read_io_threads',          # 4
         'innodb_write_io_threads',         # 4
         'innodb_file_per_table',           # ON
         'binlog_checksum',                 # CRC32
         'binlog_cache_size',               # 32768
         'max_binlog_cache_size',           # 18446744073709547520
         'max_binlog_size',                 # 1073741824
         'binlog_format'                    # STATEMENT
         ]

KNOB_DETAILS = None
num_knobs = len(KNOBS)


def init_knobs(instance):
    global instance_name
    global memory_size
    global KNOB_DETAILS
    instance_name = instance
    memory_size = configs.instance_config[instance]['memory']

    KNOB_DETAILS = {
        'skip_name_resolve': ['enum', ['ON', 'OFF']],
        'table_open_cache': ['integer', [1, 524288, 2000]],
        'max_connections': ['integer', [1100, 100000, 1100]],
        'innodb_buffer_pool_size': ['integer', [1048576, memory_size, 134217728]],
        'innodb_buffer_pool_instances': ['integer', [1, 64, 8]],
        'innodb_log_files_in_group': ['integer', [2, 100, 2]],
        'innodb_log_file_size': ['integer', [1048576, 5497558138, 50331648]],
        'innodb_purge_threads': ['integer', [1, 32, 1]],
        'innodb_read_io_threads': ['integer', [1, 64, 4]],
        'innodb_write_io_threads': ['integer', [1, 64, 4]],
        'innodb_file_per_table': ['enum', ['OFF', 'ON']],
        'binlog_checksum': ['enum', ['NONE', 'CRC32']],
        'binlog_cache_size': ['integer', [1048, 34359738368, 32768]],
        'max_binlog_cache_size': ['integer', [4096, 4294967296, 4294967296]],
        'max_binlog_size': ['integer', [4096, 1073741824, 1073741824]],
        'binlog_format': ['enum', ['ROW', 'MIXED']],
    }

    print("Instance: %s Memory: %s" % (instance_name, memory_size))


def get_init_knobs():

    knobs = {}

    for name, value in KNOB_DETAILS.items():
        knob_value = value[1]
        knobs[name] = knob_value[-1]

    return knobs


def gen_continuous(action):
    knobs = {}

    for idx in xrange(num_knobs):
        name = KNOBS[idx]
        value = KNOB_DETAILS[name]
        knob_type = value[0]
        knob_value = value[1]
        min_value = knob_value[0]
        if knob_type == 'integer':
            max_val = knob_value[1]
            eval_value = int(max_val * action[idx])
            eval_value = max(eval_value, min_value)
        else:
            enum_size = len(knob_value)
            enum_index = int(enum_size * action[idx])
            enum_index = min(enum_size - 1, enum_index)
            eval_value = knob_value[enum_index]

        if name == 'innodb_log_file_size':
            max_val = 32 * 1024 * 1024 * 1024 / knobs['innodb_log_files_in_group']
            eval_value = int(max_val * action[idx])
            eval_value = max(eval_value, min_value)
        knobs[name] = eval_value

    return knobs


def save_knobs(knob, metrics, knob_file):
    """ Save Knobs and their metrics to files
    Args:
        knob: dict, knob content
        metrics: list, tps and latency
        knob_file: str, file path
    """
    # format: tps, latency, knobstr: [#knobname=value#]
    knob_strs = []
    for kv in knob.items():
        knob_strs.append('{}:{}'.format(kv[0], kv[1]))
    result_str = '{},{},{},'.format(metrics[0], metrics[1], metrics[2])
    knob_str = "#".join(knob_strs)
    result_str += knob_str

    with open(knob_file, 'a+') as f:
        f.write(result_str+'\n')


