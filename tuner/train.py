# -*- coding: utf-8 -*-
"""
Train the model
"""

import os
import sys
import utils
import pickle
import argparse
import tuner_configs
sys.path.append('../')
import models
import environment


parser = argparse.ArgumentParser()
parser.add_argument('--tencent', action='store_true', help='Use Tencent Server')
parser.add_argument('--params', type=str, default='', help='Load existing parameters')
parser.add_argument('--workload', type=str, default='read', help='Workload type [`read`, `write`, `readwrite`]')
parser.add_argument('--instance', type=str, default='mysql1', help='Choose MySQL Instance')
parser.add_argument('--method', type=str, default='ddpg', help='Choose Algorithm to solve [`ddpg`,`dqn`]')

opt = parser.parse_args()

# Create Environment
if opt.tencent:
    env = environment.TencentServer(wk_type=opt.workload,instance_name=opt.instance, request_url=tuner_configs.TENCENT_URL)
else:
    env = environment.DockerServer(wk_type=opt.workload, instance_name=opt.instance)

tconfig = tuner_configs.config

# Build models
if opt.method == 'ddpg':

    ddpg_opt = dict()
    ddpg_opt['tau'] = 0.01
    ddpg_opt['alr'] = 0.0005
    ddpg_opt['clr'] = 0.001
    ddpg_opt['model'] = opt.params
    ddpg_opt['gamma'] = tconfig['gamma']
    ddpg_opt['batch_size'] = tconfig['batch_size']
    ddpg_opt['memory_size'] = tconfig['memory_size']

    model = models.DDPG(n_states=tconfig['num_states'], n_actions=tconfig['num_actions'], opt=ddpg_opt)
else:

    model = models.DQN()
    pass

if not os.path.exists('log'):
    os.mkdir('log')

if not os.path.exists('save_memory'):
    os.mkdir('save_memory')

if not os.path.exists('save_knobs'):
    os.mkdir('save_knobs')

expr_name = '{}_{}'.format(opt.method, str(utils.get_timestamp()))

logger = utils.Logger(
    name=opt.method,
    log_file='log/{}.log'.format(expr_name)
)

# Load mean value and variance
with open('mean_var.pkl', 'rb') as f:
    mean, var = pickle.load(f)

current_knob = environment.get_init_knobs()


def generate_knob(action, method):
    if method == 'ddpg':
        return environment.gen_continuous(action)
    else:
        return environment.gen_discrete(action, current_knob)


step_counter = 0
train_step = 0
if opt.method == 'ddpg':
    accumulate_loss = [0, 0]
else:
    accumulate_loss = 0

for episode in xrange(tconfig['epoches']):
    current_state = env.initialize()
    t = 0
    while t < 30:
        state = current_state
        action = model.choose_action(state)
        if opt.method == 'ddpg':
            current_knob = generate_knob(action, 'ddpg')
            logger.info("[ddpg] Action: {}".format(action))
        else:
            action, qvalue = action
            current_knob = generate_knob(action, 'dqn')
            logger.info("[dqn] Q:{} Action: {}".format(qvalue, action))

        reward, state_, done, score = env.step(current_knob)
        logger.info("[{}][Episode: {}][Step: {}] Reward: {} Score: {} Done: {}".format(
            opt.method, episode, t, reward, score, done
        ))

        next_state = state_

        model.replay_memory.push(
            state=state,
            reward=reward,
            action=action,
            next_state=next_state,
            terminate=done
        )

        current_state = next_state
        t = t + 1
        step_counter += 1

        if len(model.replay_memory) > 2 * tconfig['batch_size']:
            losses = []
            for i in xrange(5):
                losses.append(model.update())
                train_step += 1

            if opt.method == 'ddpg':
                accumulate_loss[0] += sum([x[0] for x in losses])
                accumulate_loss[1] += sum([x[1] for x in losses])
                logger.info('[{}][Episode: {}][Step: {}] Critic: {} Actor: {}'.format(
                    opt.method, episode, t, accumulate_loss[0]/train_step, accumulate_loss[1]/train_step
                ))
            else:
                accumulate_loss += sum(losses)
                logger.info('[{}][Episode: {}][Step: {}] Loss: {}'.format(
                    opt.method, episode, t, accumulate_loss/train_step
                ))

        if step_counter % 10 == 0:
            model.replay_memory.save('save_memory/{}.pkl'.format(expr_name))

        if done:
            break



