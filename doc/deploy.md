## Deployment

> **Update**: 2018.4.20


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

