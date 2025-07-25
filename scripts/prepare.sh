#!/usr/bin/env bash

script_path="/home/rmw/sysbench-1.0/src/lua/"

if [ ${1} == "read" ]
then
    run_script=${script_path}"oltp_read_only.lua"
elif [ ${1} == "write" ]
then
    run_script=${script_path}"oltp_write_only.lua"
else
    run_script=${script_path}"oltp_read_write.lua"
fi

sysbench ${run_script} \
	--mysql-host=$2 \
	--mysql-port=$3 \
	--mysql-user=root \
	--mysql-password=$4 \
	--mysql-db=sbtest \
	--db-driver=mysql \
	--tables=8 \
	--table-size=1000000 \
	--report-interval=10 \
	--threads=1000 \
	--time=60 \
	prepare
