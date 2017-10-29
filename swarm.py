import numpy as np
from functions import *
import sys
from random import uniform

class Agent():

    best_x = []
    best_y = sys.maxsize
    best_best_x = []
    best_best_y = sys.maxsize

    def __init__(self, D, low_pos, high_pos):
        self.reset(D, low_pos, high_pos)

    def reset(self, D, low_pos, high_pos):
        self.x = np.random.uniform(low_pos, high_pos, D)
        self.v = np.zeros(D)
        self.low_pos = low_pos
        self.high_pos = high_pos

    def init(D):
        Agent.best_x = np.zeros(D)
        Agent.best_best_x = np.zeros(D)

    def update(self, f, c, phi1, phi2):
        c2 = uniform(0, phi1)
        c3 = uniform(0, phi2)
        self.v = c * self.v + c2 * (Agent.best_x - self.x) + c3 * (Agent.best_best_x - self.x)

        # Could update v to real speed in case of clipping
        self.x += self.v
        self.x = np.clip(self.x, self.low_pos, self.high_pos)

        # Update best values
        y = f(self.x)
        if y < Agent.best_y:
            Agent.best_x = self.x
            Agent.best_y = y

    def update_best():
        if Agent.best_y < Agent.best_best_y:
            Agent.best_best_x = Agent.best_x
            Agent.best_best_y = Agent.best_y

class Swarm(object):
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

        self.agents = [Agent(D, low_pos, high_pos) for i in range(nb_agents)]
        Agent.init(D)

    def resolve(self):
        for i in range(self.nb_iter):
            for a in self.agents:
                a.update(self.f, self.c, self.phi1, self.phi2)
            Agent.update_best()
            print("Best value at iteration #{}: f({}) = {}".format(i, Agent.best_x, Agent.best_y))
        print("Minimum value found for {} in {} dimensions:\nf({}) = {:.4f}".format(self.f.__name__, self.D, Agent.best_best_x, Agent.best_best_y))
        print("\nX boundaries:\n- Low: {}\n- High: {}\n\nSwarm:\n- Number of agents: {}\n- Number of iterations: {}\n\nConstants:\n- c: {}\n- Phi1: {}\n- Phi2: {}"
                .format(self.low_pos, self.high_pos, self.nb_agents, self.nb_iter, self.c, self.phi1, self.phi2))

s = Swarm(DeJongF1, 3, -5.12, 5.12, 100, 10, 1, 2, 2)
s.resolve()