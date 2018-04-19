# -*- coding: utf-8 -*-
"""
Configure Server
"""

import os
import time
import pexpect
import platform
from SimpleXMLRPCServer import SimpleXMLRPCServer


def sudo_exec(cmdline, passwd):
    osname = platform.system()
    if osname == 'Linux':
        prompt = r'\[sudo\] password for %s: ' % os.environ['USER']
    elif osname == 'Darwin':
        prompt = 'Password:'
    else:
        assert False, osname
    child = pexpect.spawn(cmdline)
    idx = child.expect([prompt, pexpect.EOF], 3)
    if idx == 0:
        child.sendline(passwd)
        child.expect(pexpect.EOF)
    return child.before


def start_mysql(instance_name, configs):
    """
    Args:
        instance_name: str, MySQL Server Instance Name eg. ["mysql1", "mysql2"]
        configs: str, Formatted MySQL Parameters, e.g. "--binlog_size=xxx"
    """
    sudo_exec('sudo docker stop %s' % instance_name, '123456')
    sudo_exec('sudo docker rm %s' % instance_name, '123456')
    time.sleep(2)
    cmd = 'sudo docker run --name mysql1 -e MYSQL_ROOT_PASSWORD=12345678 ' \
          '-d -p 0.0.0.0:3365:3306 -v /data/{}/:/var/lib/mysql mysql:5.6 {}'.format(instance_name, configs)
    print(cmd)
    sudo_exec(cmd, '123456')
    return 1


def serve():

    server = SimpleXMLRPCServer(('0.0.0.0', 20000))
    server.register_function(start_mysql)
    server.serve_forever()


if __name__ == '__main__':
    serve()
