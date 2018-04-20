# -*- coding: utf-8 -*-
"""
desciption: Knob information

"""


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
    pass


def save_knobs(knob, metrics, knob_file):
    """ Save Knobs and their metrics to files
    Args:
        knob: dict, knob content
        metrics: list, tps and latency
        knob_file: str, file path
    """
    pass
