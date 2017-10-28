import numpy as np
from functions import *
import sys

class Agent():
    def __init__(self, D, low_pos, high_pos):
        self.reset(D, low_pos, high_pos)

    def reset(self, D, low_pos, high_pos):
        self.x = np.random.uniform(low_pos, high_pos, D)
        self.v = np.zeros(D)

    def update(self):
        pass

class Swarm(object):
    def __init__(self, f, D, low_pos, high_pos, nb_iter, nb_agents, c, phi1, phi2):
        self.f = f
        self.D = D
        self.nb_iter = nb_iter
        #self.nb_agents = nb_agents
        self.c = c
        self.phi1 = phi1
        self.phi2 = phi2

        self.agents = [Agent(D, low_pos, high_pos) for i in range(nb_agents)]

    def resolve(self):
        min_value = sys.maxsize
        for a in self.agents:
            a.update()
            y = self.f(a.x)
            if y < min_value:
                min_value = y
        print("Minimum value found for {} in {} dimensions:\n{:.4f}".format(self.f.__name__, self.D, min_value))
        print("Parameters are:\n")

s = Swarm(DeJongF1, 3, -5.12, 5.12, 2000, 50, 1, 2, 2)
s.resolve()