from random import shuffle, randrange, uniform
from math import exp, log

def random_permutation(grid):
    i1 = randrange(0, N * N)
    i2 = randrange(0, N * N)
    while i1 == i2:
        i2 = randrange(0, N * N)
    swap = grid[i1]
    grid[i1] = grid[i2]
    grid[i2] = swap

def composant(links):
    ### Init
    tentatives = 0
    success = 0
    successive_fails = 0
    grid = [i for i in range(N * N)]
    shuffle(grid)
    e = 0
    for i in range(100):
        e += compute_len(grid, links)
        shuffle(grid)
    mean = e // 100
    print(mean)
    p = 0.70
    T = -mean / log(p)
    print(T)

    ### Loop
    while True:
        tentatives += 1
        e = compute_len(grid, links)
        cpy = grid.copy()
        random_permutation(grid)
        new_e = compute_len(grid, links)
        if new_e < e:
            print("Progressing...")
            success += 1
            successive_fails = 0
        else:
            print("Regressing...")
            p = exp((e - new_e) / T)
            r = uniform(0, 1)
            print(p)
            if r < p:
                # accepted
                success += 1
                successive_fails = 0
            else:
                # declined, roll back
                grid = cpy
                successive_fails += 1

        if success == 12 * N or tentatives == 100 * N:
            # abort
            print("System balanced")
            break

        if successive_fails == 100:
            print("System blocked")
            break

        T *= 0.9

    print(grid)
    print(compute_len(grid, links))



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
composant(gen_links())