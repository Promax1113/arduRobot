import pygame
import time
import os
os.environ['SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS'] = '1'

def get_inputs():
    clock = pygame.time.Clock()

    pygame.init()
    pygame.joystick.init()
    
    joystick_count = pygame.joystick.get_count()
    print(f"Number of joysticks: {joystick_count}")
    
    if joystick_count == 0:
        print("No joysticks found!")
        return
    
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(joy.get_numaxes())
    while True:
        pygame.event.pump()
        print(round(joy.get_axis(0), 4))
        time.sleep(0.2)
        clock.tick(60)
get_inputs()
