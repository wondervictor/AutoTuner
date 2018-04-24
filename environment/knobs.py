# -*- coding: utf-8 -*-
"""
desciption: Knob information

"""

import utils

KNOBS = ['skip_name_resolve',
         'table_open_cache',
         'max_connections',
         'innodb_buffer_pool_size',
         'innodb_buffer_pool_instances',
         'innodb_log_files_in_group',
         'innodb_log_file_size',
         'innodb_purge_threads',
         'innodb_read_io_threads',
         'innodb_write_io_threads',
         'innodb_file_per_table',
         'binlog_checksum',
         'binlog_cache_size',
         'max_binlog_cache_size',
         'max_binlog_size',
         'binlog_format'
         ]

KNOB_DETAILS = {
    'skip_name_resolve': ['enum', ['OFF', 'ON'], None],
    'table_open_cache': ['integer', [1, 524288, 2000], None],
    'max_connections': ['integer', [1, 100000, 151], None],
    'innodb_buffer_pool_size': ['integer', [1, 34359738368, 17179869184], None],
    # WARN: innodb_buffer_pool_size 80% of memory
    'innodb_buffer_pool_instances': ['integer', [1, 64, 8], None],
    'innodb_log_files_in_group': ['integer', [2, 100, 2], None],
    'innodb_log_file_size': ['integer', [1048576, 5497558138, 50331648], ['innodb_log_files_in_group']],
    'innodb_purge_threads': ['integer', [1, 32, 1], None],
    'innodb_read_io_threads': ['integer', [1, 64, 4], None],
    'innodb_write_io_threads': ['integer', [1, 64, 4], None],
    'innodb_file_per_table': ['enum', ['OFF', 'ON'], None],
    'binlog_checksum': ['enum', ['NONE', 'CRC32'], None],
    'binlog_cache_size': ['integer', [4096, 34359738368, 32768], None],
    'max_binlog_cache_size': ['integer', [4096, 18446744073709551615, 18446744073709551615], None],
    'max_binlog_size': ['integer', [4096, 1073741824, 1073741824], None],
    'binlog_format': ['enum', ['ROW', 'STATEMENT', 'MIXED'], None],

}

# TENCENT Mysql Instance Memory
memory_size = 4 * 1024 * 1024 * 1024
memory_size = utils.read_machine()
# MB
memory_size = memory_size / (1024*1024)

print("Machine Memory: {} MiB".format(memory_size))

UNIFIED_KNOBS = {
    'skip_name_resolve': ['enum', ['OFF', 'ON'], None],
    'table_open_cache': ['integer', [1, 524288, 2000], None],
    'max_connections': ['integer', [1, 100000, 151], None],
    # innodb_buffer_pool_size unit: MB
    'innodb_buffer_pool_size': ['integer_MB', [1, memory_size, 16384], None],
    # WARN: innodb_buffer_pool_size 80% of memory
    'innodb_buffer_pool_instances': ['integer', [1, 64, 8], None],
    'innodb_log_files_in_group': ['integer', [2, 100, 2], None],
    # innodb_log_file_size unit: MB
    'innodb_log_file_size': ['integer_MB', [1, 5424, 48], ['innodb_log_files_in_group']],
    'innodb_purge_threads': ['integer', [1, 32, 1], None],
    'innodb_read_io_threads': ['integer', [1, 64, 4], None],
    'innodb_write_io_threads': ['integer', [1, 64, 4], None],
    'innodb_file_per_table': ['enum', ['OFF', 'ON'], None],
    'binlog_checksum': ['enum', ['NONE', 'CRC32'], None],
    # binlog_cache_size unit: MB
    'binlog_cache_size': ['integer_MB', [0.001, 32124, 0.03125], None],
    # max_binlog_cache_size unit: GB
    'max_binlog_cache_size': ['integer_GB', [4096, 17179869183, 17179869183], None],
    # max_binlog_size unit: MB
    'max_binlog_size': ['integer_MB', [0.00390625, 1024, 1024], None],
    'binlog_format': ['enum', ['ROW', 'MIXED'], None],

}

num_knobs = len(KNOBS)


def get_init_knobs():

    knobs = {}
    for idx in xrange(num_knobs):
        name = KNOBS[idx]
        value = KNOB_DETAILS[name]
        knob_type = value[0]
        knob_value = value[1]

        if knob_type == 'integer':
            init_value = knob_value[-1]
        else:
            init_value = knob_value[0]
        knobs[name] = init_value

    return knobs


def gen_discrete(action, knobs):

    result = {}
    for idx in xrange(num_knobs):
        name = KNOBS[idx]
        value = KNOB_DETAILS[name]
        knob_type = value[0]
        knob_value = value[1]

        if knob_type == 'integer':
            max_val = knob_value[1]
            min_val = knob_value[0]
            if name == 'innodb_log_file_size':
                # warning: 512GB / innodb_log_files_in_group
                max_val = 16*1024*1024*1024 / result['innodb_log_files_in_group']

            if action[idx] == 0:
                val = int((knobs[name] + max_val) / 2)
                if val > max_val:
                    val = max_val
            elif action[idx] == 1:
                if knobs[name] > max_val:
                    val = max_val
                elif knobs[name] < min_val:
                    val = min_val
                else:
                    val = knobs[name]
            else:
                val = int((knobs[name] + min_val) / 2)

            if val > max_val:
                val = max_val

        else:
            enums = knob_value
            current_index = enums.index(knobs[name])

            if action[idx] == 0:
                current_index += 1
                if current_index >= len(enums):
                    current_index = 0
                val = enums[current_index]
            elif action[idx] == 1:
                val = enums[current_index]
            else:
                current_index -= 1
                if current_index < 0:
                    current_index = len(enums)-1
                val = enums[current_index]

        result[name] = val

    return result


def gen_continuous(action):
    result = {}
    for idx in xrange(num_knobs):
        name = KNOBS[idx]
        value = UNIFIED_KNOBS[name]
        knob_type = value[0]
        knob_value = value[1]
        if knob_type == 'integer_MB':
            max_val = knob_value[1]
            eval_value = int(max_val * action[idx])*1024*1024
        elif knob_type == 'integer_GB':
            max_val = knob_value[1]
            eval_value = int(max_val * action[idx])*1024*1024*1024
        elif knob_type == 'integer':
            max_val = knob_value[1]
            eval_value = int(max_val * action[idx])
        else:
            enum_size = len(knob_value)
            enum_index = int(enum_size * action[idx])
            enum_index = min(enum_size - 1, enum_index)
            eval_value = knob_value[enum_index]

        if name == 'innodb_log_file_size':
            max_val = 16 * 1024 / result['innodb_log_files_in_group']
            eval_value = int(max_val * action[idx])*1024*1024
        result[name] = eval_value

    return result


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
    result_str = '{},{},'.format(metrics[0], metrics[1])
    knob_str = "#".join(knob_strs)
    result_str += knob_str

    with open(knob_file, 'a+') as f:
        f.write(result_str+'\n')


