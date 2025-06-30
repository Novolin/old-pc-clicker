import pygame
from engine import *
from ui import *
from GameData.game import GameState


pygame.init()


# Basic pygame init stuff:
clock = pygame.time.Clock()
_delta = 0 # ms since last frame change

# Grid, state managers:
grid = GridManager(80,26)
state = GameState(grid)
screen = pygame.display.set_mode(grid.surface.get_size())

pygame.mouse.set_visible(False)



while state.run:
    # Check inputs

    # pass our events to the state object.
    state.event_handler(pygame.event.get()) 

        
    # Logic process:

    state.tick(_delta)



    # Blank and draw data from grid:
    screen.fill((0,0,0))
    screen.blit(grid.update_screen(state), [0,0])
    pygame.display.flip()
    

    # cap frame rate at 60
    _delta = clock.tick(60)