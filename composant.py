from random import shuffle, randrange, uniform
from math import exp, log
import networkx as nx
import matplotlib.pyplot as plt
import time

nb_pic = 0

def random_permutation(grid):
    i1 = randrange(0, N * N)
    i2 = randrange(0, N * N)
    while i1 == i2:
        i2 = randrange(0, N * N)
    swap = grid[i1]
    grid[i1] = grid[i2]
    grid[i2] = swap

def composant(links, p=0.7):
    ### Init
    tentatives = 0
    success = 0
    grid = [i for i in range(N * N)]
    shuffle(grid)
    e_init = compute_len(grid, links)
    e = 0
    for i in range(100):
        new_e = compute_len(grid, links)
        e += abs(new_e - e_init)
        e_init = new_e
        shuffle(grid)
    mean = e // 100
    print("Mean: " + str(mean))
    T = -mean / log(p)
    print("Initial T: " + str(T))

    draw_graph(grid, links)

    ### Loop
    looping = True
    while looping:
        tentatives += 1
        e = compute_len(grid, links)
        cpy = grid.copy()
        random_permutation(grid)
        new_e = compute_len(grid, links)
        d_e = new_e - e

        if d_e <= 0:
            success += 1

        else:
            p = exp(-d_e / T)
            r = uniform(0, 1)
            if r < p:
                # accepted
                success += 1
            else:
                # declined, roll back
                grid = cpy

        if success == 12 * N * N or tentatives == 100 * N * N:
            T *= 0.9
            success = 0
            tentatives = 0
            print("Equilibre thermodynamique")
            print("E = " + str(e))
            print("Temp = " + str(T))
            draw_graph(grid, links)
            continue

        if T <= 1:
            print("System blocked")
            break
            looping = False

        #print("New T: %f" % T)

    print(grid)
    print(compute_len(grid, links))
    draw_graph(grid, links, pause=False)



def nb(x, y):
    return y * N + x

def gen_links():
    links = []
    for j in range(N - 1):
        for i in range(N - 1):
            num = nb(i, j)
            links.append((num, num + 1)) # right link
            links.append((num, num + N)) # down link
        num = nb(N - 1, j) # last node of current row
        links.append((num, num + N))
    for i in range(N - 1): # last row has only right links
        num = nb(i, N - 1)
        links.append((num, num + 1)) # right link
    return links

def draw_graph(nodes, links, pause=True):
    global nb_pic
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(links)

    pos = {}
    for i, v in zip(nodes, range(N * N)):
        pos[v] = (i // N, i % N)
    # Save fig
    fig = plt.gcf()
    filename = "output/p08_" + str(nb_pic).zfill(2) + ".png"
    nb_pic += 1
    plt.savefig(filename, dpi=fig.dpi)

    plt.gcf().clear()
    nx.draw_networkx(g, pos=pos)
    if pause:
        plt.pause(0.1)
        plt.draw()
    else:
        plt.show()

def coord(i, grid):
    ind = grid.index(i)
    return (ind % N, ind // N)

def compute_len(grid, links):
    length = 0
    for link in links:
        v1 = coord(link[0], grid)
        v2 = coord(link[1], grid)
        length += (abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])) * 5
    return length

# main
N = 5
composant(gen_links(), p=0.8)
