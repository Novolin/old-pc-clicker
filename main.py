import pygame
import engine
import ui
import gamedata

pygame.init()

clock = pygame.time.Clock()
running = True
dt = 0 # frame delta



# Import our font, set up our basic screen space.
font = pygame.font.Font("ibmfont.ttf", 32)
gamescreen = engine.ScreenRenderer(80,35, font)
screen = pygame.display.set_mode(gamescreen.res)
cursor = gamescreen.cursor # set a shorthand
gamescreen.move_cursor(None, [0,0])

kb_state = pygame.key.get_pressed() # Should be empty, or at least a base state

# Input Handling function, broken out to make it a bit easier to read
# Will need tweaks once we do text input


def handle_keypress(pressed_keys):
    if pressed_keys == None:
        return
    if pressed_keys[pygame.K_UP]:
        gamescreen.move_cursor([0,-1])
    if pressed_keys[pygame.K_DOWN]:
        gamescreen.move_cursor([0,1])
    if pressed_keys[pygame.K_LEFT]:
        gamescreen.move_cursor([-1,0])
    if pressed_keys[pygame.K_RIGHT]:
        gamescreen.move_cursor([1,0])
    if pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_RETURN]:
        gamescreen.do_cursor_action()
    if pressed_keys[pygame.K_f]:
        gamescreen.state.add_window(ui.build_test_window())
    if pressed_keys[pygame.K_w]:
        gamescreen.state.windows[0].move_viewport(y_move = -1)
    if pressed_keys[pygame.K_s]:
        gamescreen.state.windows[0].move_viewport(y_move = 1)
    if pressed_keys[pygame.K_a]:
        gamescreen.state.windows[0].move_viewport(x_move = -1)
    if pressed_keys[pygame.K_d]:
        gamescreen.state.windows[0].move_viewport(x_move = 1)

def move_cursor_with_mouse():
    # Moves the in-game cursor to the current mouse position.
    mouse_pos = pygame.mouse.get_pos() # get the data before we do any calcs, so it doesn't change partway through lmao
    # DEBUG: for now just return whether or not hte mouse is in the cursor's position
    if not cursor.get_abs_pos().collidepoint(mouse_pos):
        current_mouse_relative_pos = [mouse_pos[0]// gamescreen.tilesize[0], mouse_pos[1] // gamescreen.tilesize[1] ]
        mouse_delta = [current_mouse_relative_pos[0] - cursor.position[0], current_mouse_relative_pos[1] - cursor.position[1]]
        gamescreen.move_cursor(mouse_delta, source = "mouse")

# Main logic loop:
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    keys = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEMOTION:
            move_cursor_with_mouse()
        if event.type == pygame.MOUSEBUTTONUP:
            gamescreen.do_cursor_action() # For now just do this, change once we actually fix shit.



    # Blank screen and tell our UI system to refresh:
    screen.fill((0,0,0))
    screen.blit(gamescreen.game_tick(clock.get_time()), (0,0))


    # Handle inputs
    
    handle_keypress(keys)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(30) / 1000

pygame.quit()
