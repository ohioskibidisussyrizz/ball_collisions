from random import *

from pygame import *

from numpy import *

from classes import *

DEFAULT_WIDTH, DEFAULT_HEIGHT = 1000, 1000
DEFAULT_GRAVITY = 0.5
DEFAULT_POS_X, DEFAULT_POS_Y = 100, 0
DEFAULT_VERTICAL_SLOWDOWN, DEFAULT_HORIZONTAL_SLOWDOWN = -0.9, -0.9
DEFAULT_BALL_COLOR = (255, 255, 255)
DEFAULT_SCREEN_COLOR = (0, 0, 0)
DEFAULT_HZ = 120
DEFAULT_RADIUS = 25
DEFAULT_VEL_X, DEFAULT_VEL_Y = 10, 0

def random_x():
    return randint(0, DEFAULT_WIDTH)

def random_vel_x():
    return uniform(-DEFAULT_VEL_X, DEFAULT_VEL_X)

def random_y():
    return randint(0, DEFAULT_HEIGHT)

def random_vel_y():
    return uniform(-DEFAULT_VEL_Y, DEFAULT_VEL_Y)

def random_radius():
    return randint(1, 10)

def get_random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def random_ball_array(number_of_balls):
    balls = []
    for i in range(number_of_balls):
        radius = random_radius()
        mass = radius * 2
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
    new_pos_x = ball.get_pos_x() + ball.get_vel_x()
    radius = ball.get_radius()

    if new_pos_x + radius > screen_width:
        new_pos_x = screen_width - radius
        new_vel_x = ball.get_vel_x() * -1
    elif new_pos_x - radius < 0:
        new_pos_x = radius
        new_vel_x = ball.get_vel_x() * -1
    else:
        new_vel_x = ball.get_vel_x()

    ball.set_pos_x(new_pos_x)
    ball.set_vel_x(new_vel_x)

def vertical_collision_calc(ball: Ball, screen_height, gravity):
    new_pos_y = ball.get_pos_y() + ball.get_vel_y()
    new_vel_y = ball.get_vel_y() + gravity
    radius = ball.get_radius()

    if new_pos_y + radius > screen_height:
        new_pos_y = screen_height - radius
        new_vel_y *= DEFAULT_VERTICAL_SLOWDOWN
        if new_vel_y > -1:
            new_vel_y = 0

    ball.set_pos_y(new_pos_y)
    ball.set_vel_y(new_vel_y)

def simulate_bouncing_ball(ball: Ball, width, height, gravity):
    vertical_collision_calc(ball, height, gravity)
    horizontal_collision_calc(ball, width)

def check_collision(balls: list[Ball]):
    intervals = []

    for ball in balls:
        x_min, x_max = ball.get_pos_x() - ball.get_radius(), ball.get_pos_x() + ball.get_radius()
        y_min, y_max = ball.get_pos_y() - ball.get_radius(), ball.get_pos_y() + ball.get_radius()
        intervals.append([x_min, x_max, y_min, y_max, ball])
    sorted_intervals = sorted(intervals, key=lambda interval: interval[0])
    collisions = []

    for i in range(len(sorted_intervals)):
        current = sorted_intervals[i]
        for j in range(i + 1, len(sorted_intervals)):
            other = sorted_intervals[j]
            if (current[0] <= other[1] and current[1] >= other[0]) and (current[2] <= other[3] and current[3] >= other[2]):
                collisions.append([current[4], other[4]])

    return collisions

def collision_pair(ball1: Ball, ball2: Ball):
    epsilon = 1e-6
    normal_vector = array([ball1.get_pos_x() - ball2.get_pos_x(), ball1.get_pos_y() - ball2.get_pos_y()])
    distance = linalg.norm(normal_vector) + epsilon
    unit_normal = normal_vector / distance
    unit_tangent = array([-unit_normal[1], unit_normal[0]])

    vel1 = array([ball1.get_vel_x(), ball1.get_vel_y()])
    vel2 = array([ball2.get_vel_x(), ball2.get_vel_y()])

    rel_vel = vel1 - vel2
    vel_along_normal = dot(rel_vel, unit_normal)

    if distance < ball1.get_radius() + ball2.get_radius() and vel_along_normal < 0:
        v1n, v1t = dot(vel1, unit_normal), dot(vel1, unit_tangent)
        v2n, v2t = dot(vel2, unit_normal), dot(vel2, unit_tangent)

        m1, m2 = ball1.get_mass(), ball2.get_mass()

        v1n_after = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
        v2n_after = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)

        v1_after = v1n_after * unit_normal + v1t * unit_tangent
        v2_after = v2n_after * unit_normal + v2t * unit_tangent

        ball1.set_vel_x(v1_after[0])
        ball1.set_vel_y(v1_after[1])
        ball2.set_vel_x(v2_after[0])
        ball2.set_vel_y(v2_after[1])

balls_array = random_ball_array(1000)

def start(balls: list[Ball], width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, gravity=DEFAULT_GRAVITY):
    init()
    screen = display.set_mode((width, height))
    clock = time.Clock()

    while True:
        for i in event.get():
            if i.type == QUIT:
                return

        screen.fill(DEFAULT_SCREEN_COLOR)

        for ball in balls:
            simulate_bouncing_ball(ball, width, height, gravity)

        colliding_pairs = check_collision(balls)
        for pair in colliding_pairs:
            collision_pair(pair[0], pair[1])

        for ball in balls:
            draw.circle(screen, ball.get_color(), (ball.get_pos_x(), ball.get_pos_y()), ball.get_radius(), 0)

        clock.tick(DEFAULT_HZ)
        display.update()

start(balls_array)

