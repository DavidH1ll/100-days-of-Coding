import turtle
import time

BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_GAP = 6
BRICK_COLORS = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db"]
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BALL_SPEED = 4


class Paddle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.7, stretch_len=6)
        self.color("white")
        self.penup()
        self.goto(0, -250)

    def move_left(self):
        if self.xcor() > -340:
            self.setx(self.xcor() - 30)

    def move_right(self):
        if self.xcor() < 340:
            self.setx(self.xcor() + 30)


class Ball(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, -230)
        self.dx = BALL_SPEED * 0.7
        self.dy = BALL_SPEED

    def move(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1


class Brick(turtle.Turtle):
    def __init__(self, x, y, color):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=BRICK_HEIGHT / 20, stretch_len=BRICK_WIDTH / 20)
        self.color(color)
        self.penup()
        self.goto(x, y)

    def destroy(self):
        self.hideturtle()
        self.goto(1000, 1000)


class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = 3
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-380, 270)
        self._update_display()

    def _update_display(self):
        self.clear()
        self.write(f"Score: {self.score}  Lives: {self.lives}", font=("Courier", 16, "bold"))

    def add_score(self, points):
        self.score += points
        self._update_display()

    def lose_life(self):
        self.lives -= 1
        self._update_display()


class BreakoutGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.screen.bgcolor("#0a0a0a")
        self.screen.title("Breakout")
        self.screen.tracer(0)

        self.paddle = Paddle()
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.bricks = []
        self.game_running = True
        self.paused = False

        self._create_bricks()
        self._setup_controls()

    def _create_bricks(self):
        start_x = -((BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)) / 2) + BRICK_WIDTH / 2 + BRICK_GAP
        start_y = 200
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = start_y - row * (BRICK_HEIGHT + BRICK_GAP)
                brick = Brick(x, y, BRICK_COLORS[row])
                self.bricks.append(brick)

    def _setup_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeypress(self.paddle.move_right, "Right")
        self.screen.onkeypress(self.paddle.move_left, "a")
        self.screen.onkeypress(self.paddle.move_right, "d")
        self.screen.onkey(self._toggle_pause, "p")

    def _toggle_pause(self):
        self.paused = not self.paused

    def _check_collisions(self):
        # Wall collisions
        if self.ball.xcor() > 390 or self.ball.xcor() < -390:
            self.ball.bounce_x()
        if self.ball.ycor() > 290:
            self.ball.bounce_y()

        # Paddle collision
        if (self.ball.ycor() < -235 and self.ball.ycor() > -260 and
            abs(self.ball.xcor() - self.paddle.xcor()) < PADDLE_WIDTH / 2 + BALL_RADIUS):
            offset = self.ball.xcor() - self.paddle.xcor()
            self.ball.dx = offset * 0.15
            self.ball.dy = abs(self.ball.dy)

        # Bottom
        if self.ball.ycor() < -290:
            self.scoreboard.lose_life()
            if self.scoreboard.lives > 0:
                self.ball.goto(0, -230)
                self.ball.dx = BALL_SPEED * 0.7
                self.ball.dy = BALL_SPEED
            else:
                self._game_over("Game Over")

        # Brick collisions
        for brick in self.bricks[:]:
            if brick.isvisible() and abs(self.ball.xcor() - brick.xcor()) < BRICK_WIDTH / 2 + BALL_RADIUS:
                if abs(self.ball.ycor() - brick.ycor()) < BRICK_HEIGHT / 2 + BALL_RADIUS:
                    self.ball.bounce_y()
                    brick.destroy()
                    self.bricks.remove(brick)
                    self.scoreboard.add_score(10)
                    break

        if not self.bricks:
            self._game_over("You Win!")

    def _game_over(self, message):
        self.game_running = False
        t = turtle.Turtle()
        t.color("white" if "Win" in message else "#e74c3c")
        t.penup()
        t.hideturtle()
        t.write(f"{message}\nFinal Score: {self.scoreboard.score}", align="center",
                font=("Courier", 24, "bold"))

    def run(self):
        while self.game_running:
            if not self.paused:
                self.ball.move()
                self._check_collisions()
            self.screen.update()
            time.sleep(0.01)

        self.screen.exitonclick()


if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
