import math
import pygame

window_height = 645
window_width = 1250
WIN = pygame.display.set_mode((window_width, window_height))

class Ray:
    def __init__(self, angle):
        self.angle = math.radians(360 - angle)
        self.colour = (100, 100, 100)
        self.width = 2      # Use odd numbers or 2 only
        self.view_distance = 300

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
