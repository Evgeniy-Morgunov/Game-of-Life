from random import randint
import numpy as np
import pygame
import sys

def compute_neighbours(Z, N):

    N[1:-1,1:-1] = Z[:-2,:-2] + Z[1:-1,:-2] + Z[:-2,1:-1] \
                 + Z[2:,:-2]                + Z[2:,1:-1] \
                 + Z[:-2,2:]  + Z[1:-1,2:]  + Z[2:,2:]



def iterate(Z, N, M):
    
    birth = ((N == 3) & (Z == 0))
    survive = ((N == 2) | (N == 3)) & (Z == 1) 
    
    Z[...] = 0
    Z[birth | survive] = 1
    
    M[M > 0.25] = 0.25
    M *= 0.995
    M[Z == 1] = 1



def draw_blocks(screen, xlen, ylen, world):

    surf = pygame.surfarray.make_surface(world * 255)
    
    screen.blit(surf, (-1, -1))
    


def make_random_grid(x, y):
    grid = np.random.randint(0, 2, size=(x, y))
    grid[:, 0] *= 0
    grid[:, -1] *= 0
    grid[0] *= 0
    grid[-1] *= 0
    
    return grid


def main():
    xmax = int(sys.argv[1])
    ymax = int(sys.argv[2])

    screen = pygame.display.set_mode((xmax, ymax), pygame.SCALED)
    clock = pygame.time.Clock()

    h = 0
    scale = 1
    xlen = xmax // scale + 2
    ylen = ymax // scale + 2
    world = make_random_grid(xlen, ylen)
    all_world = np.zeros(world.shape)

    play = False

    N = np.zeros_like(world)

    while True:
        screen.fill("black")

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = not play

        draw_blocks(screen, xlen, ylen,np.stack((all_world, all_world, all_world), axis=2 ))

        compute_neighbours(world, N)

        if play:
            iterate(world, N, all_world)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 3)))

        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    main()
