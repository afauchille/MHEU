import numpy as np
from functions import *
import sys
import random

class Agent():

    best_x = []
    best_y = sys.maxsize
    timestamp = 0

    def __init__(self, f, D, low_pos, high_pos):
        self.reset(f, D, low_pos, high_pos)

    def reset(self, f, D, low_pos, high_pos):
        self.x = np.random.uniform(low_pos, high_pos, D)
        self.v = np.random.uniform(low_pos - high_pos , high_pos - low_pos, D)
        self.low_pos = low_pos
        self.high_pos = high_pos
        self.bx = np.copy(self.x)
        self.by = f(self.x)

    def init(D):
        Agent.best_x = np.zeros(D)

    def update(self, f, c, phi1, phi2, cur_iter):
        c2 = random.uniform(0, phi1)
        c3 = random.uniform(0, phi2)
        self.v = c * self.v + c2 * (self.bx - self.x) + c3 * (Agent.best_x - self.x)

        # Could update v to real speed in case of clipping
        self.x += self.v
        self.x = np.clip(self.x, self.low_pos, self.high_pos)

        # Update best values
        y = f(self.x)

        if y < self.by:
            self.bx = np.copy(self.x)
            self.by = y

        if y < Agent.best_y:
            Agent.best_x = np.copy(self.x)
            Agent.best_y = y
            Agent.timestamp = cur_iter

class Swarm:
    def __init__(self, f, D, low_pos, high_pos, nb_iter, nb_agents, c, phi1, phi2):
        self.f = f
        self.D = D
        self.low_pos = low_pos
        self.high_pos = high_pos
        self.nb_iter = nb_iter
        self.nb_agents = nb_agents
        self.c = c
        self.phi1 = phi1
        self.phi2 = phi2

        self.agents = [Agent(f, D, low_pos, high_pos) for i in range(nb_agents)]
        Agent.init(D)

    def resolve(self, verbose=False):
        for i in range(self.nb_iter):
            for a in self.agents:
                a.update(self.f, self.c, self.phi1, self.phi2, i)
            if verbose:
                print("Best value at iteration #{}: f({}) = {}".format(i, Agent.best_x, Agent.best_y))
        if verbose:
            print("Minimum value found for {} in {} dimensions:\nf({}) = {:.4f}".format(self.f.__name__, self.D, Agent.best_x, Agent.best_y))
            print("\nX boundaries:\n- Low: {}\n- High: {}\n\nSwarm:\n- Number of agents: {}\n- Number of iterations: {}\n\nConstants:\n- c: {}\n- Phi1: {}\n- Phi2: {}"
                    .format(self.low_pos, self.high_pos, self.nb_agents, self.nb_iter, self.c, self.phi1, self.phi2))
        return {
        'y_min' : Agent.best_y,
        'x_min' : Agent.best_x,
        'iter_needed' : Agent.timestamp
        }

def t_mean(t):
    return (t[1] + t[0]) / 2

class HyperSwarm:
    def __init__(self):
        pass

    def run(self, f, D, nb_iter, nb_agents, c_b, phi1_b, phi2_b):
        random.seed()
        nb_ech = 10

        best_c, best_phi1, best_phi2 = t_mean(c_b), t_mean(phi1_b), t_mean(phi2_b)

        print("Optimizing c...")

        minx, miny = [], sys.maxsize
        for c in np.linspace(c_b[0], c_b[1], nb_ech):
            s = Swarm(f.f, D, f.low, f.high, nb_iter, nb_agents, c, best_phi1, best_phi2)
            meta = s.resolve(verbose=False)
            if meta['y_min'] < miny:
                miny = meta['y_min']
                minx = meta['x_min']
                best_c = c

        print("Optimizing phi1...")

        minx, miny = [], sys.maxsize
        for phi1 in np.linspace(phi1_b[0], phi1_b[1], nb_ech):
            s = Swarm(f.f, D, f.low, f.high, nb_iter, nb_agents, best_c, phi1, best_phi2)
            meta = s.resolve(verbose=False)
            if meta['y_min'] < miny:
                miny = meta['y_min']
                minx = meta['x_min']
                best_phi1 = phi1

        print("Optimizing phi2...")

        minx, miny = [], sys.maxsize
        for phi2 in np.linspace(phi2_b[0], phi2_b[1], nb_ech):
            s = Swarm(f.f, D, f.low, f.high, nb_iter, nb_agents, best_c, best_phi1, phi2)
            meta = s.resolve(verbose=False)
            if meta['y_min'] < miny:
                miny = meta['y_min']
                minx = meta['x_min']
                best_phi2 = phi2

        #print('Minimum found for function {}: {} for x = {} after #{} iterations'.format(f.f.__name__, meta['y_min'], meta['x_min'], meta['iter_needed']))
        print("Best configuration found: c = {}, phi1 = {}, phi2 = {}".format(c, phi1, phi2))

#s = Swarm(DeJongF1, 10, -5.12, 5.12, nb_iter=10, nb_agents=200, c=1, phi1=2, phi2=2)
#s.resolve()

gen_test_functions()
ss = HyperSwarm()
ss.run(test_functions['DeJongF1'], 5, 1000, 100, (0., 2.), (0., 2.), (0., 2.))
