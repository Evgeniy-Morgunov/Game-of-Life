from random import randint
import numpy as np
import pygame
import sys


def compute_neighbours(Z, X):
    # start_time = pygame.time.get_ticks()

    N = np.zeros_like(Z)
    M = np.zeros_like(Z)

    N[1:-1,1:-1] = Z[:-2, :-2] + Z[1:-1, :-2] + Z[:-2, 1:-1] \
                 + Z[2:,  :-2]                + Z[2:,  1:-1] \
                 + Z[:-2,  2:] + Z[1:-1,  2:] + Z[2:,    2:]

    M[1:-1,1:-1] = X[:-2, :-2] + X[1:-1, :-2] + X[:-2, 1:-1] \
                 + X[2:,  :-2]                + X[2:,  1:-1] \
                 + X[:-2,  2:] + X[1:-1,  2:] + X[2:,    2:]

    # print("compute neighbours ", (pygame.time.get_ticks() - start_time)/1000)
    return N, M, N + M


def iterate(Z, X):
    # start_time = pygame.time.get_ticks()

    N, M, NM = compute_neighbours(Z, X)

    Z[np.where(NM > 3)] = 0
    Z[np.where(NM < 2)] = 0
    Z[np.where((NM == 3)&(N > M))] = 1

    X[np.where(NM > 3)] = 0
    X[np.where(NM < 2)] = 0
    X[np.where((NM == 3)&(M > N))] = 1
    
    # print("iterate ", (pygame.time.get_ticks() - start_time)/1000)


def draw_blocks(screen, xlen, ylen, world):
    # start_time = pygame.time.get_ticks()

    surf = pygame.surfarray.make_surface(world)
    
    screen.blit(surf, (-1, -1))
    
    # print("draw ", (pygame.time.get_ticks() - start_time)/1000)


def make_random_grid(x, y):
    Zgrid = np.random.randint(0, 2, size=(x, y))
    Xgrid = np.random.randint(0, 2, size=(x, y))
    Zgrid[:, 0] *= 0
    Zgrid[:, -1] *= 0
    Zgrid[0:x//2] *= 0
    Zgrid[-1] *= 0
    
    Xgrid[:, 0] *= 0
    Xgrid[:, -1] *= 0
    Xgrid[x//2:] *= 0
    Xgrid[0] *= 0
    
    return Zgrid, Xgrid


def make_clear_grid(x, y):
    grid = np.zeros((x, y))
    
    return grid


def main():
    xmax = int(sys.argv[1])
    ymax = int(sys.argv[2])

    screen = pygame.display.set_mode((xmax, ymax), pygame.SCALED)
    clock = pygame.time.Clock()

    h = 0
    xlen = xmax + 2
    ylen = ymax + 2
    Zworld, Xworld = make_random_grid(xlen, ylen)
    play = False
    
    while True:
        screen.fill("black")

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play

        draw_blocks(screen, xlen, ylen, (Zworld * 20) + (Xworld * 100))
        
        if play:
            iterate(Zworld, Xworld)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 2)))

        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    main()
