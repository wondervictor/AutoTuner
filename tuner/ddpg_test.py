# -*- coding: utf-8 -*-
"""
Deep Deterministic Policy Gradient Model Test

"""

import gym
from ddpg import DDPG
from utils import Logger

config = {
    'model': '',
    'alr': 0.001,
    'clr': 0.001,
    'gamma': 0.9,
    'batch_size': 32,
    'tau': 0.002
}

logger = Logger('DDPG_TEST')
env = gym.make('Hopper-v1')

n_actions = 3
n_states = 11

ddpg = DDPG(
    n_actions=n_actions,
    n_states=n_states,
    opt=config
)

max_steps = 100

for i in xrange(100):
    ddpg.reset()
    state = env.reset()
    t = 0
    while t < max_steps:

        action = ddpg.choose_action(state)
        next_state, reward, done = ddpg.apply_action(env, action)
        env.render()
        ddpg.replay_memory.push(
            state=state,
            action=action,
            next_state=next_state,
            terminate=done,
            reward=reward
        )

        t += 1
        logger.info('Episode: {}/{100} Step: {} Reward: {} Action: {} Terminate: {}'
                    .format(i, t, reward, action, done)
                    )

        state = next_state
        if done:
            break
