"""
File: turtle_test
Contributors: Chung-Kuang Lin, Tessa Chang, Yaun-Chih Chen
----------------------------------------------------------
A graphical simulator for Covid spread. The 2nd iteration trying to make the
ball animation using Turtle library.
For Turtle library documentations, refer to: https://docs.python.org/3/library/turtle.html
The animation is adapted after: https://youtube.com/playlist?list=PLlEgNdBJEO-mRsbxRND_Cu805SCrXoOZB
"""

import turtle
import random

POPULATION = 50
BALL_SPEED = 3
# ball color references:
HEALTHY = '#aac6ca'
INFECTED = '#bb641d'
RECOVERED = '#cb8ac0'


def get_random(base_speed: int, include_zero: False) -> int:
    """The helper function to randomly assign a speed value for one axis of the ball
    To ensure the ball is always moving, zero is taken away from the generated list
    :param: Base_speed: a non-zero integer given by the user
    :param: Include_zero: To include zero in the random pool or not. By default False
    :return: An int for moving value
    TODO: If a numpy.random.randint() might speed up the process
    TODO: A try, exception might needed if the base_speed was a negative number or invalid input(str, special char)
    TODO: A ball only moves horizontally or vertically still exists, need some help for solving this issue
    """
    random_speed_list = list(range(-base_speed, base_speed + 1))
    if include_zero:
        # Remove zero
        random_speed_list.remove(0)
    return random.choice(random_speed_list)


def main():
    # Create a window
    window = turtle.Screen()

    # (Optional) Config the window resolution as 800x600
    window.screensize(800, 600)

    # Set background color as black
    # Both built-in color or html color codes are supported
    window.bgcolor("black")

    # Set the window title
    window.title("test for covid simulator")

    # Start a tracer function to detect all pixel changes in every animation frame
    window.tracer(0)

    # Put 50 balls into the window, the default ball diameter is 20, record the created ball info in a list
    balls = []
    for i in range(POPULATION):
        balls.append(turtle.Turtle())

    # Set the ball attributes and moving speed
    for ball in balls:
        ball.shape("circle")  # Reshape the turtle into a circle
        ball.color(HEALTHY)  # The color code for the healthy people
        ball.penup()  # Turn off the drawing the trace of ball movement
        ball.speed(0)  # Initialize the ball speed as 0
        x_coord = random.randint(-299, 299)  # Get the randomized x position of the ball
        y_coord = random.randint(-299, 299)  # Get the randomized the y position of the ball
        ball.goto(x_coord, y_coord)  # Put the ball at (x_coord, y_coord)
        ball.dx = get_random(BALL_SPEED, False)
        ball.dy = get_random(BALL_SPEED, False)

    # Animation loop, still a non-stop animation so far
    while True:
        for ball in balls:
            ball.sety(ball.ycor() + ball.dy)
            ball.setx(ball.xcor() + ball.dx)

            # Window boundary collision detection
            # Take the dx into consideration, ex: ball.xcor() > 290 and dx > 0
            if ball.xcor() >= 300 and ball.dx > 0:
                ball.dx *= -1
            if ball.xcor() <= -300 and ball.dx < 0:
                ball.dx *= -1
            if ball.ycor() > 300 and ball.dy > 0:
                ball.dy *= -1
            if ball.ycor() < -300 and ball.dy < 0:
                ball.dy *= -1

        # Ball collision detection, detect the ith ball is colliding with the jth ball
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                # Once collide, meaning the distance of two balls is equal or less than 20px
                if balls[i].distance(balls[j]) <= 20:
                    # when two balls collide, they swap moving speed
                    balls[i].dx, balls[i].dy = -balls[j].dx, -balls[j].dy
                    balls[j].dx, balls[j].dy = -balls[i].dx, -balls[i].dy

                    # Once two ball collides, the color will switch to INFECTED color
                    balls[i].color(INFECTED)
                    balls[j].color(INFECTED)
        window.update()  # Update the current animation frame
    window.mainloop()  # Initialize the loop for running a window


if __name__ == "__main__":
    main()
