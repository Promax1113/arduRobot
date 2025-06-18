import pygame
import time

def get_inputs():
    clock = pygame.time.Clock()

    pygame.joystick.init()
    pygame.init()
    print(pygame.joystick.get_count())
    joy = pygame.joystick.Joystick(0)
    print(joy.get_numaxes())
    while True:
        pygame.event.pump()
        print(round(joy.get_axis(0), 4))
        time.sleep(0.2)
        clock.tick(60)
get_inputs()
