## Specs

> **Update**:

### Parameters Setting

* gamma: discount, = 0.95
* batch_size: 128
* update_target: 20 target网络更新频率
* DDPG的tau: 0.01
* Actor Learning Rate: 0.0001
* Critic Learning Rate: 0.001



### Implementation Detailes

##### Reward 函数设计

* 简化版

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

##### Actor 网络

```` python
Actor (
  (layers): Sequential (
    (0): BatchNorm1d(63, eps=1e-05, momentum=0.1, affine=True)
    (1): Linear (63 -> 128)
    (2): LeakyReLU (0.2)
    (3): BatchNorm1d(128, eps=1e-05, momentum=0.1, affine=True)
    (4): Linear (128 -> 128)
    (5): LeakyReLU (0.2)
    (6): Linear (128 -> 64)
    (7): LeakyReLU (0.2)
    (8): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True)
    (9): Linear (64 -> 16)
    (10): LeakyReLU (0.2)
  )
  (act): Sigmoid ()
)
````

##### Critic 网络

```` python
Critic (
  (state_input): Linear (63 -> 128)
  (action_input): Linear (16 -> 128)
  (act): LeakyReLU (0.2)
  (state_bn): BatchNorm1d(63, eps=1e-05, momentum=0.1, affine=True)
  (layers): Sequential (
    (0): Linear (256 -> 256)
    (1): LeakyReLU (0.2)
    (2): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True)
    (3): Linear (256 -> 64)
    (4): LeakyReLU (0.2)
    (5): BatchNorm1d(64, eps=1e-05, momentum=0.1, affine=True)
    (6): Linear (64 -> 1)
  )
)

````