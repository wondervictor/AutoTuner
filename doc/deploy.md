## Deployment

> **Update**: 2018.4.26


#### Configure

1. 修改 `mysql.py` 文件路径

````python

# Tencent
TEMP_FILES = "/data/AutoTuner/train_result/tmp/"
PROJECT_DIR = "/data/"
# Local
TEMP_FILES = "/home/rmw/train_result/tmp/"
PROJECT_DIR = "/home/rmw/"
````

2. 修改 `knobs.py`

* 修改memory读取

````python
# TENCENT Mysql Instance Memory
memory_size = 4 * 1024 * 1024 * 1024
memory_size = utils.read_machine()
# MB
memory_size = memory_size / (1024*1024)
````

* 修改 `KNOB_DETAILS` 里的默认参数。

3. 修改 `run_sysbench.sh`

````bash

script_path="/home/rmw/sysbench-1.0/src/lua/"
# script_path="/usr/share/sysbench/"
````


#### Train

````bash
python train.py 
````

###### args

* `--tencent`: 如果在腾讯云上训练，开启这个选项
* `--params`: 如果有已经训练的模型参数文件，直接添加参数文件，模型加载时会加载参数(格式：`<path>/xxx`，在代码里会转为 `<path>/xxx_actor.pth 和 <path>/xxx_critic.pth`) 
* `--workload`: workload选择，`read`: 只读， `write`: 只写，`readwrite`: 读写混合
* `--instance`: 实例名称，和`environment/configs.py`里的参数对应
* `--method`: 选择算法，DDPG或者DQN，默认DDPG 

