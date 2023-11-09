"""
IMPORTS
"""
import sys
from random import randint
import pygame
import math

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

class Ray:
    def __init__(self, angle):
        self.angle = math.radians(360 - angle)
        self.colour = (100, 100, 100)
        self.width = 2      # Use odd numbers or 2 only
        self.view_distance = 3000

    def draw(self, x, y, bounds):
        end_x, end_y = self.calculateEnd(x, y, bounds)
        pygame.draw.line(WIN, self.colour, (x, y), (end_x, end_y), self.width)

    def calculateEnd(self, x, y, bounds):
        if bounds == []:
            return (self.view_distance * math.cos(self.angle)) + x, (self.view_distance * math.sin(self.angle)) + y
        else:
            x1 = x
            y1 = y
            x2 = round((self.view_distance * math.cos(self.angle)) + x)
            y2 = round((self.view_distance * math.sin(self.angle)) + y)

            if x1 != x2:
                ray_line_gradient = (y1 - y2) / (x1 - x2)
                ray_line_intercept = y1 - (ray_line_gradient * x1)
                # ray line equation: y = mx + c

            closest_intersection_x = 10000
            closest_intersection_y = 10000

            for bound in bounds:
                x3 = bound.x1
                y3 = bound.y1
                x4 = bound.x2
                y4 = bound.y2

                if max(x1, x2) < min(x3, x4):
                    continue
                elif x1 == x2 and x3 == x4:
                    continue
                elif x3 == x4:
                    intersection_x = x3
                    intersection_y = (ray_line_gradient * intersection_x) + ray_line_intercept

                    if intersection_x >= max(min(x1, x2), min(x3, x4)) and intersection_x <= min(max(x1, x2), max(x3, x4)) and intersection_y >= max(min(y1, y2), min(y3, y4)) and intersection_y <= min(max(y1, y2), max(y3, y4)):
                        if abs(intersection_x - x1) < abs(closest_intersection_x - x1):
                            closest_intersection_x = intersection_x
                            closest_intersection_y = intersection_y
                elif x1 == x2:
                    boundary_line_gradient = ((y3 - y4)) / (x3 - x4)
                    boundary_line_intercept = y3 - (boundary_line_gradient * x3)

                    intersection_x = x2
                    intersection_y = (boundary_line_gradient * intersection_x) + boundary_line_intercept

                    if intersection_x >= max(min(x1, x2), min(x3, x4)) and intersection_x <= min(max(x1, x2), max(x3, x4)) and intersection_y >= max(min(y1, y2), min(y3, y4)) and intersection_y <= min(max(y1, y2), max(y3, y4)):
                        if abs(intersection_y - y1) < abs(closest_intersection_y - y1):
                            closest_intersection_x = intersection_x
                            closest_intersection_y = intersection_y
                else:
                    boundary_line_gradient = ((y3 - y4)) / (x3 - x4)
                    boundary_line_intercept = y3 - (boundary_line_gradient * x3)
                    # boundary line equation: y = mx + c

                    if boundary_line_gradient != ray_line_gradient:
                        intersection_x = (boundary_line_intercept - ray_line_intercept) / (ray_line_gradient - boundary_line_gradient)
                        intersection_y = (ray_line_gradient * intersection_x) + ray_line_intercept

                        if intersection_x >= max(min(x1, x2), min(x3, x4)) and intersection_x <= min(max(x1, x2), max(x3, x4)):
                            if abs(intersection_x - x1) < abs(closest_intersection_x - x1) or abs(intersection_y - y1) < abs(closest_intersection_y - y1):
                                closest_intersection_x = intersection_x
                                closest_intersection_y = intersection_y

            if closest_intersection_x == 10000 and closest_intersection_y == 10000:
                return x2, y2

            return closest_intersection_x, closest_intersection_y

class Boundary:
    def __init__(self, x1, y1, x2, y2, hidden=False):
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.hidden = hidden
        self.show_colour = (255, 255, 255)
        self.hide_colour = (0, 0, 0)
        self.width = 3

    def draw(self):
        if self.hidden:
            pygame.draw.line(WIN, self.hide_colour, self.start, self.end, self.width)
        else:
            pygame.draw.line(WIN, self.show_colour, self.start, self.end, self.width)

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

"""
SETS FPS
"""
clock = pygame.time.Clock()

"""
MAIN LOOP
"""
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
