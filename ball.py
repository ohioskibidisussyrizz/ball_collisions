import random

import pygame

import math

import numpy as np

from ball_class import Ball

DEFAULT_WIDTH, DEFAULT_HEIGHT = 1000, 1000
DEFAULT_GRAVITY = 0.5
DEFAULT_POS_X, DEFAULT_POS_Y = 100, 0
DEFAULT_VERTICAL_SLOWDOWN, DEFAULT_HORIZONTAL_SLOWDOWN = -0.9, -0.9
DEFAULT_BALL_COLOR = (255, 255, 255)
DEFAULT_SCREEN_COLOR = (0, 0, 0)
DEFAULT_HZ = 120
DEFAULT_RADIUS = 25
DEFAULT_VEL_X, DEFAULT_VEL_Y = 10 , 0


def random_x():
    return random.randint(0, DEFAULT_WIDTH)

def random_vel_x():
    return random.uniform(-DEFAULT_VEL_X, DEFAULT_VEL_X)

def random_y():
    return random.randint(0, DEFAULT_HEIGHT)

def random_vel_y():
    return random.uniform(-DEFAULT_VEL_Y, DEFAULT_VEL_Y)

def random_radius():
    return random.randint(20, 50)

def get_random_color():
    return (random.randint(0, 255), random.randint(0,255), random.randint(0,255))



def random_ball_array(number_of_balls):
    balls = []
    for i in range(number_of_balls):
        radius = random_radius()
        mass = radius*2
        random_ball = Ball(
            random_x(),
            random_vel_x(),
            random_y(),
            random_vel_y(),
            radius,
            mass,
            get_random_color(),
        )
        balls.append(random_ball)
    return balls

def horizontal_collision_calc(ball: Ball, screen_width):
    # Update position based on velocity
    new_pos_x = ball.get_pos_x() + ball.get_vel_x()
    radius = ball.get_radius()

    # Check for collision with right wall
    if new_pos_x + radius > screen_width:
        new_pos_x = screen_width - radius
        new_vel_x = ball.get_vel_x()
        new_vel_x *= -1
    # Check for collision with left wall
    elif new_pos_x - radius < 0:
        new_pos_x = radius
        new_vel_x = ball.get_vel_x()
        new_vel_x *= -1
    else:
        new_vel_x = ball.get_vel_x()
    # Update ball state
    ball.set_pos_x(new_pos_x)
    ball.set_vel_x(new_vel_x)

def vertical_collision_calc(ball: Ball, screen_height, gravity):
    # Update vertical position and velocity
    new_pos_y = ball.get_pos_y() + ball.get_vel_y()
    new_vel_y = ball.get_vel_y() + gravity
    radius = ball.get_radius()

    # Check for collision with the bottom of the screen
    if new_pos_y + radius > screen_height:
        new_pos_y = screen_height - radius
        new_vel_y *= DEFAULT_VERTICAL_SLOWDOWN

        if new_vel_y > -1:
            new_vel_y = 0

    # Update the ball's position and velocity
    ball.set_pos_y(new_pos_y)
    ball.set_vel_y(new_vel_y)





def simulate_bouncing_ball(ball: Ball,
                           width,
                           height,
                           initial_gravity,
                           ):
    vertical_collision_calc(ball, height, initial_gravity)
    horizontal_collision_calc(ball, width)

def collision(balls: list[Ball]):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            dx, dy = balls[i].get_pos_x()- balls[j].get_pos_x(), balls[i].get_pos_y()- balls[j].get_pos_y()
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if balls[i].get_radius() + balls[j].get_radius() >= distance:
                normal_vector = np.array([balls[i].get_pos_x() - balls[j].get_pos_x(), balls[i].get_pos_y() - balls[j].get_pos_y()])
                unit_vector = normal_vector / np.linalg.norm(normal_vector)
                unit_tangent_vector = np.array([-unit_vector[1], unit_vector[0]])
                v1n, v1t, v2n, v2t = np.dot(unit_vector, balls[i].vel), np.dot(unit_tangent_vector, balls[i].vel), np.dot(unit_vector, balls[j].vel), np.dot(unit_tangent_vector, balls[j].vel)
                v1_tangent_after, v2_tangent_after = v1t, v2t
                v1_normal_after, v2_normal_after = (v1n * (balls[i].get_mass() - balls[j].get_mass()) + 2 * balls[j].get_mass() * v2n) / (balls[i].get_mass() + balls[j].get_mass()), (v2n * (balls[j].get_mass() - balls[i].get_mass()) + 2 * balls[i].get_mass() * v1n) / (balls[i].get_mass() + balls[j].get_mass())
                v1_normal_vector_after, v1_tangent_vector_after = v1_normal_after * unit_vector, v1_tangent_after * unit_tangent_vector
                v2_normal_vector_after, v2_tangent_vector_after = v2_normal_after * unit_vector, v2_tangent_after * unit_tangent_vector
                v1_vel_after, v2_vel_after = v1_normal_vector_after + v1_tangent_vector_after, v2_normal_vector_after + v2_tangent_vector_after

                balls[i].set_vel_x(v1_vel_after[0])
                balls[i].set_vel_y(v1_vel_after[1])
                balls[j].set_vel_x(v2_vel_after[0])
                balls[j].set_vel_y(v2_vel_after[1])

def start(
        balls: list[Ball],
        width=DEFAULT_WIDTH,
        height=DEFAULT_HEIGHT,
        initial_gravity=DEFAULT_GRAVITY):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(DEFAULT_SCREEN_COLOR)
        for ball in balls:
            simulate_bouncing_ball(ball, width, height, initial_gravity)

        collision(balls)

        for ball in balls:
            pygame.draw.circle(screen, ball.get_color(), (int(ball.get_pos_x()), int(ball.get_pos_y())),
                               ball.get_radius(), 0)

        clock.tick(DEFAULT_HZ)
        pygame.display.update()




start(random_ball_array(3))


