# -*- coding: utf-8 -*-
"""
Deep Deterministic Policy Gradient Model

"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optimizer
from torch.autograd import Variable

from OUProcess import OUProcess
from replay_memory import ReplayMemory
from utils import Logger, get_timestamp


def totensor(x):
    return Variable(torch.FloatTensor(x))


class ActorLow(nn.Module):

    def __init__(self, n_states, n_actions, ):
        super(ActorLow, self).__init__()
        self.layers = nn.Sequential(
            nn.BatchNorm1d(n_states),
            nn.Linear(n_states, 32),
            nn.LeakyReLU(negative_slope=0.2),
            nn.BatchNorm1d(32),
            nn.Linear(32, n_actions),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self._init_weights()
        self.out_func = nn.Tanh()

    def _init_weights(self):

        for m in self.layers:
            if type(m) == nn.Linear:
                m.weight.data.normal_(0.0, 1e-3)
                m.bias.data.uniform_(-0.1, 0.1)

    def forward(self, x):

        out = self.layers(x)

        return self.out_func(out)


class CriticLow(nn.Module):

    def __init__(self, n_states, n_actions):
        super(CriticLow, self).__init__()
        self.state_input = nn.Linear(n_states, 32)
        self.action_input = nn.Linear(n_actions, 32)
        self.act = nn.LeakyReLU(negative_slope=0.2)
        self.state_bn = nn.BatchNorm1d(n_states)
        self.layers = nn.Sequential(
            nn.Linear(64, 1),
            nn.LeakyReLU(negative_slope=0.2),
        )
        self._init_weights()

    def _init_weights(self):
        self.state_input.weight.data.normal_(0.0, 1e-3)
        self.state_input.bias.data.uniform_(-0.1, 0.1)

        self.action_input.weight.data.normal_(0.0, 1e-3)
        self.action_input.bias.data.uniform_(-0.1, 0.1)

        for m in self.layers:
            if type(m) == nn.Linear:
                m.weight.data.normal_(0.0, 1e-3)
                m.bias.data.uniform_(-0.1, 0.1)

    def forward(self, x, action):
        x = self.state_bn(x)
        x = self.act(self.state_input(x))
        action = self.act(self.action_input(action))

        _input = torch.cat([x, action], dim=1)
        value = self.layers(_input)
        return value


class Actor(nn.Module):

    def __init__(self, n_states, n_actions, ):
        super(Actor, self).__init__()
        self.layers = nn.Sequential(
            nn.BatchNorm1d(n_states),
            nn.Linear(n_states, 128),
            nn.LeakyReLU(negative_slope=0.2),
            nn.BatchNorm1d(128),
            nn.Linear(128, 128),
            nn.LeakyReLU(negative_slope=0.2),
            nn.Linear(128, 64),
            nn.LeakyReLU(negative_slope=0.2),
            nn.BatchNorm1d(64),
            nn.Linear(64, n_actions),
            nn.LeakyReLU(negative_slope=0.2)
        )
        self._init_weights()
        self.act = nn.Tanh()

    def _init_weights(self):

        for m in self.layers:
            if type(m) == nn.Linear:
                m.weight.data.normal_(0.0, 1e-3)
                m.bias.data.uniform_(-0.1, 0.1)

    def forward(self, x):

        out = self.act(self.layers(x))
        return out


class Critic(nn.Module):

    def __init__(self, n_states, n_actions):
        super(Critic, self).__init__()
        self.state_input = nn.Linear(n_states, 128)
        self.action_input = nn.Linear(n_actions, 128)
        self.act = nn.LeakyReLU(negative_slope=0.2)
        self.state_bn = nn.BatchNorm1d(n_states)
        self.layers = nn.Sequential(
            nn.Linear(256, 256),
            nn.LeakyReLU(negative_slope=0.2),
            nn.BatchNorm1d(256),
            nn.Linear(256, 64),
            nn.LeakyReLU(negative_slope=0.2),
            nn.BatchNorm1d(64),
            nn.Linear(64, 1),
            nn.LeakyReLU(negative_slope=0.2),
        )
        self._init_weights()

    def _init_weights(self):
        self.state_input.weight.data.normal_(0.0, 1e-3)
        self.state_input.bias.data.uniform_(-0.1, 0.1)

        self.action_input.weight.data.normal_(0.0, 1e-3)
        self.action_input.bias.data.uniform_(-0.1, 0.1)

        for m in self.layers:
            if type(m) == nn.Linear:
                m.weight.data.normal_(0.0, 1e-3)
                m.bias.data.uniform_(-0.1, 0.1)

    def forward(self, x, action):
        x = self.state_bn(x)
        x = self.act(self.state_input(x))
        action = self.act(self.action_input(action))

        _input = torch.cat([x, action], dim=1)
        value = self.layers(_input)
        return value


class DDPG(object):

    def __init__(self, n_states, n_actions, opt):

        self.n_states = n_states
        self.n_actions = n_actions

        _time = get_timestamp()
        self.logger = Logger('DDPG', log_file='../logs/{}_train.log'.format(_time))
        del _time
        # Params
        self.alr = opt['alr']
        self.clr = opt['clr']
        self.model_name = opt['model']
        self.batch_size = opt['batch_size']
        self.gamma = opt['gamma']
        self.tau = opt['tau']

        # Build Network
        self._build_network()
        self.logger.info('Finish Initializing Networks')
        self.replay_memory = ReplayMemory(capacity=10000)
        self.noise = OUProcess(n_actions)
        self.logger.info('DDPG Initialzed!')

    def _build_network(self):

        self.actor = ActorLow(self.n_states, self.n_actions)
        self.target_actor = ActorLow(self.n_states, self.n_actions)
        self.critic = CriticLow(self.n_states, self.n_actions)
        self.target_critic = CriticLow(self.n_states, self.n_actions)

        # if model params are provided, load them
        if len(self.model_name):
            self.load_model(model_name=self.model_name)

        # Copy actor's parameters
        self._update_target(self.target_actor, self.actor, tau=1.0)

        # Copy critic's parameters
        self._update_target(self.target_critic, self.critic, tau=1.0)

        self.loss_criterion = nn.MSELoss()
        self.actor_optimizer = optimizer.Adam(lr=self.alr, params=self.actor.parameters())
        self.critic_optimizer = optimizer.Adam(lr=self.clr, params=self.critic.parameters())

    def _update_target(self, target, source, tau):
        for (target_param, param) in zip(target.parameters(), source.parameters()):
            target_param.data.copy_(
                target_param.data * (1-tau) + param.data * tau
            )

    def reset(self):
        self.noise.reset()

    def _sample_batch(self):
        batch = self.replay_memory.sample(self.batch_size)
        states = map(lambda x: x.state.tolist(), batch)
        next_states = map(lambda x: x.next_state.tolist(), batch)
        actions = map(lambda x: x.action.tolist(), batch)
        rewards = map(lambda x: x.reward, batch)
        terminates = map(lambda x: x.terminate, batch)

        return states, next_states, actions, rewards, terminates

    def update(self):

        states, next_states, actions, rewards, terminates = self._sample_batch()
        batch_states = totensor(states)
        batch_next_states = Variable(torch.FloatTensor(next_states), volatile=True)
        batch_actions = totensor(actions)
        batch_rewards = totensor(rewards)
        mask = [0 if x else 1 for x in terminates]
        mask = totensor(mask)

        target_next_actions = self.target_actor(batch_next_states)
        target_next_value = self.target_critic(batch_next_states, target_next_actions).squeeze(1)
        target_next_value.volatile = False
        current_value = self.critic(batch_states, batch_actions)
        next_value = batch_rewards + mask * target_next_value * self.gamma
        # Update Critic

        loss = self.loss_criterion(current_value, next_value)
        self.critic_optimizer.zero_grad()
        loss.backward()
        self.critic_optimizer.step()

        # Update Actor
        self.critic.eval()
        policy_loss = -self.critic(batch_states, self.actor(batch_states))
        policy_loss = policy_loss.mean()
        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()
        self.critic.train()

        self.logger.info('Critic Loss:{} Actor Loss: {}'.format(loss.data[0], policy_loss.data[0]))

        self._update_target(self.target_critic, self.critic, tau=self.tau)
        self._update_target(self.target_actor, self.actor, tau=self.tau)

    def choose_action(self, x):
        self.actor.eval()
        act = self.actor(totensor([x.tolist()])).squeeze(0)
        self.actor.train()
        action = act.data.numpy()

        action += self.noise.noise()
        return action

    def apply_action(self, env, action):
        next_state, reward, done, _ = env.step(action)
        return next_state, reward, done

    def load_model(self, model_name):

        self.actor.load_state_dict(
            torch.load('{}_actor.pth'.format(model_name))
        )
        self.critic.load_state_dict(
            torch.load('{}_critic.pth'.format(model_name))
        )

    def save_model(self, model_dir, title):

        torch.save(
            self.actor.state_dict(),
            '{}/{}_actor.pth'.format(model_dir, title)
        )

        torch.save(
            self.critic.state_dict(),
            '{}/{}_critic.pth'.format(model_dir, title)
        )
