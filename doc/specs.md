## Specs

> **Update**:

### Parameters Setting

* gamma: discount, = 0.85
* batch_size: 16
* update_target: 20 target网络更新频率
* DDPG的tau: 0.01


### Implementation Detailes

##### Reward 函数设计

*简化版

```` python
tps = 并发提高百分比
latency = 延迟下降百分比

reward = 0  # tps - latency
if tps < 0:
    reward += 2 * tps
else:
    reward += tps
if latency > 0:
    reward -= 2 * latency
else:
    reward -= latency
````