#!/usr/bin/env bash

# $1 IP
# $2 port
# $3 passwd
# $4 filename


# -w: warehouse num
# -c: thread nums
# -r: warmup time
# -l: lasting time
# -i: report interval
# -f: report file name

tpcc_start -h${1} -d -P ${2} tpcc_test -uroot -p${3} -w 1000 -c 1000 -r 20 -l 100 -i 5 >> $4
