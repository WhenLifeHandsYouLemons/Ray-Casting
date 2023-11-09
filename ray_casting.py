"""
IMPORTS
"""
import sys
from random import randint
import pygame
from Ray import Ray
from Boundary import Boundary

"""
APP WINDOW
"""
bg_colour = 0, 0, 0
window_height = 645
window_width = 1250
WIN = pygame.display.set_mode((window_width, window_height))
WIN.fill(bg_colour)

"""
VARIABLES
"""
margin = 10
def generateNewMaze(bounds):
    bounds = bounds[:4]
    for i in range(7):
        bounds.append(Boundary(randint(margin, window_width-margin), randint(margin, window_height-margin), randint(margin, window_width-margin), randint(margin, window_height-margin), False))

    return bounds

hide = False
boundaries = [
    Boundary(0, 0, window_width-1, 0),
    Boundary(window_width-1, 0, window_width-1, window_height-1),
    Boundary(window_width-1, window_height-1, 0, window_height-1),
    Boundary(0, window_height-1, 0, 0),
    Boundary(40, 175, 40, 482, hide),
    Boundary(40, 482, 700, 482, hide),
    Boundary(247, 259, 247, 421, hide),
    Boundary(247, 421, 375, 421, hide),
    Boundary(375, 421, 375, 259, hide),
    Boundary(587, 124, 1021, 300, hide),
    Boundary(1040, 154, 857, 481, hide)
]

character_pos = [100, 200]
move_speed = 10

fov = 125
facing_angle = 90
left_view_bound = facing_angle + int(fov / 2)
right_view_bound = facing_angle - int(fov / 2)
turning_speed = 10

ray_amount = 360

solid_view = True

"""
MAIN LOOP
"""
clock = pygame.time.Clock()
RUNNING_WINDOW = True

while RUNNING_WINDOW == True:
    clock.tick(30)
    WIN.fill(bg_colour)

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    # RAYS
    if facing_angle > 360:
        facing_angle -= 360
    if facing_angle < 0:
        facing_angle += 360

    left_view_bound = facing_angle + int(fov / 2)
    right_view_bound = facing_angle - int(fov / 2)

    if solid_view:
        view_points = [character_pos.copy()]
        for ray_angle in range(right_view_bound, left_view_bound, int(ray_amount / 360)):
            view_points.append(Ray(ray_angle).calculateEnd(character_pos[0], character_pos[1], boundaries))
        pygame.draw.polygon(WIN, (100, 100, 100), view_points)
    else:
        for ray_angle in range(right_view_bound, left_view_bound, int(ray_amount / 360)):
            Ray(ray_angle).draw(character_pos[0], character_pos[1], boundaries)


    # BOUNDARIES
    for i, j in enumerate(boundaries):
        if i > 3:   # The first 4 boundaries are the edges of the screen
            j.hidden = hide
        j.draw()

    # CHARACTER
    pygame.draw.circle(WIN, (0, 150, 255), character_pos, 10)

    pygame.display.update()

    # KEY INPUTS
    pressed = pygame.key.get_pressed()      # These are consistent key presses
    if pressed[pygame.K_UP]:
        character_pos[1] -= move_speed
        if facing_angle != 90:
            if facing_angle > 90 and facing_angle <= 270:
                facing_angle -= turning_speed
            else:
                facing_angle += turning_speed
    if pressed[pygame.K_LEFT]:
        character_pos[0] -= move_speed
        if facing_angle != 180:
            if facing_angle >= 0 and facing_angle < 180:
                facing_angle += turning_speed
            else:
                facing_angle -= turning_speed
    if pressed[pygame.K_DOWN]:
        character_pos[1] += move_speed
        if facing_angle != 270:
            if facing_angle >= 90 and facing_angle < 270:
                facing_angle += turning_speed
            else:
                facing_angle -= turning_speed
    if pressed[pygame.K_RIGHT]:
        character_pos[0] += move_speed
        if facing_angle != 0:
            if facing_angle > 0 and facing_angle <= 180:
                facing_angle -= turning_speed
            else:
                facing_angle += turning_speed

    for event in pygame.event.get():        # These are single key presses
        if event.type == pygame.QUIT:
            RUNNING_WINDOW = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING_WINDOW = False
                pygame.quit()
            if event.key == pygame.K_SPACE:
                if hide:
                    hide = False
                else:
                    hide = True
            if event.key == pygame.K_g:
                boundaries = generateNewMaze(boundaries)






sys.exit()
