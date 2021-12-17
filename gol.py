from random import randint
import numpy as np
import pygame


n = 256
#Du, Dv, F, k = 0.16, 0.08, 0.035, 0.065  # Bacteria 1
# Du, Dv, F, k = 0.14, 0.06, 0.035, 0.065  # Bacteria 2
# Du, Dv, F, k = 0.16, 0.08, 0.060, 0.062  # Coral
# Du, Dv, F, k = 0.19, 0.05, 0.060, 0.062  # Fingerprint
# Du, Dv, F, k = 0.10, 0.10, 0.018, 0.050  # Spirals
# Du, Dv, F, k = 0.12, 0.08, 0.020, 0.050  # Spirals Dense
Du, Dv, F, k = 0.10, 0.16, 0.020, 0.050  # Spirals Fast
#Du, Dv, F, k = 0.16, 0.08, 0.020, 0.055  # Unstable
# Du, Dv, F, k = 0.16, 0.08, 0.050, 0.065  # Worms 1
#Du, Dv, F, k = 0.16, 0.08, 0.054, 0.063  # Worms 2
#Du, Dv, F, k = 0.16, 0.08, 0.035, 0.060  # Zebrafish

def iterate(U, V, u, v):
    for i in range(10):
        Lu = (                  U[0:-2, 1:-1] +
              U[1:-1, 0:-2] - 4*U[1:-1, 1:-1] + U[1:-1, 2:] +
                                U[2:  , 1:-1])
        Lv = (                  V[0:-2, 1:-1] +
              V[1:-1, 0:-2] - 4*V[1:-1, 1:-1] + V[1:-1, 2:] +
                                V[2:  , 1:-1])
        uvv = u*v*v
        u += (Du*Lu - uvv + F*(1-u))
        v += (Dv*Lv + uvv - (F+k)*v)

def draw_blocks(screen, xlen, ylen, world):

    surf = pygame.surfarray.make_surface(world*255)
    
    screen.blit(surf, (-1, -1))
    

def main():

    Z = np.zeros(((n+2), (n+2)), [('U', np.double),
                            ('V', np.double)])

    U, V = Z['U'], Z['V']
    u, v = U[1:-1, 1:-1], V[1:-1,1:-1]

    r = 20
    u[...] = 1.0
    U[n//2-r:n//2+r, n//2-r:n//2+r] = 0.50
    V[n//2-r:n//2+r, n//2-r:n//2+r] = 0.25
    u += 0.05*np.random.uniform(-1, 1,(n,n))
    v += 0.05*np.random.uniform(-1, 1,(n,n))


    xmax = n
    ymax = n

    screen = pygame.display.set_mode((xmax, ymax), pygame.SCALED)
    clock = pygame.time.Clock()

    h = 0
    scale = 1
    xlen = xmax // scale + 2
    ylen = ymax // scale + 2

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

        draw_blocks(screen, xlen, ylen,np.stack((V, V, V), axis=2 ))

        if play:
            iterate(U, V, u, v)

        pygame.display.set_caption("$~GoL ~fps: " + str(round(clock.get_fps(), 3)))

        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    main()
