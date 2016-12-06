# profile tpcc benchmark.

import os
import sys
import time
import subprocess
import re
from subprocess import call


cwd = os.getcwd()
OLTP_HOME = "%s/oltpbench" % (cwd)

db_host = 'dev1.db.pdl.cmu.local'

db_port = '54321'
db_user = 'haibinl'
thread_num = 1
new_order_ratio = 100
payment_ratio = 0
order_status_ratio = 0
delivery_ratio = 0
stock_level_ratio = 0
scale_factor = 1
test_time = 60

# Requires that peloton-testbed is in the home directory
config_filename = "tpcc_config.xml"
start_benchmark_script = "%s/oltpbenchmark -b tpcc -c " % (OLTP_HOME) + cwd + "/" + config_filename + " --histograms  --create=true --load=true --execute=true -s 5 -o "

parameters={}

def prepare_parameters():
    os.chdir(cwd)
    parameters["$THREAD_NUMBER"] = str(thread_num)
    parameters["$NEW_ORDER_RATIO"] = str(new_order_ratio)
    parameters["$PAYMENT_RATIO"] = str(payment_ratio)
    parameters["$ORDER_STATUS_RATIO"] = str(order_status_ratio)
    parameters["$DELIVERY_RATIO"] = str(delivery_ratio)
    parameters["$STOCK_LEVEL_RATIO"] = str(stock_level_ratio)
    parameters["$SCALE_FACTOR"] = str(scale_factor)
    parameters["$IP"] = db_host
    parameters["$PORT"] = db_port
    parameters["$TIME"] = str(test_time)
    parameters["$USER"] = db_user

    template = ""
    with open("tpcc_template.xml") as in_file:
        template = in_file.read()
    for param in parameters:
        template = template.replace(param, parameters[param])
    with open(config_filename, "w") as out_file:
        out_file.write(template)

def get_result_path():
  global cwd
  return "%s/outputfile_%d_%d_%d_%d_%d_%d" % (cwd, new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio, scale_factor)

def start_bench():
    # go to oltpbench directory
    os.chdir(os.path.expanduser(OLTP_HOME))
    call("git pull origin master", shell=True)
    call("ant", shell=True)
    cmd = start_benchmark_script + get_result_path() + " 2>&1 | tee > %s.log" % (get_result_path())
    call(cmd, shell=True)

def collect_data(result_dir_name):
    os.chdir(cwd)
    os.system("rm -rf " + result_dir_name)
    os.system("mkdir " + result_dir_name)
    os.system("mv callgrind.out.* " + result_dir_name)
    call("cat %s.log" % (get_result_path()), shell=True)
    os.system("mv %s.* %s/" % (get_result_path(), result_dir_name))

if __name__ == "__main__":
    # 45:43:4:4:4
    # thread_num = 20
    # new_order_ratio = 50
    # payment_ratio = 50
    # order_status_ratio = 0
    # delivery_ratio = 0
    # stock_level_ratio = 0

    new_order_ratio =  44
    payment_ratio = 44
    order_status_ratio = 4
    delivery_ratio = 4
    stock_level_ratio = 4
    test_time = 60
    for thread_num in [1, 2, 4, 6, 8, 10, 11, 12, 16,20,24,28,32,40,48,56,64]:
        scale_factor = thread_num
        prepare_parameters()
        start_bench()
        result_dir_name = "tpcc_collected_data_%d_%d_%d_%d_%d_%d_%d" % (new_order_ratio, payment_ratio, order_status_ratio, delivery_ratio, stock_level_ratio, scale_factor, thread_num)
        collect_data(result_dir_name)
