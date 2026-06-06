import turtle
import time
import random
import json
import os

GROUND_Y = -200
HIGH_SCORE_FILE = os.path.join(os.path.dirname(__file__), "high_score.json")


class DinoGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 400)
        self.screen.bgcolor("#f7f7f7")
        self.screen.title("Dino Runner")
        self.screen.tracer(0)

        self._draw_ground()
        self.dino = Dino()
        self.obstacles = []
        self.score = 0
        self.speed = 6
        self.game_running = True
        self.high_score = self._load_high_score()

        self.score_display = turtle.Turtle()
        self.score_display.color("#535353")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(350, 160)
        self._update_score_display()

        self.game_over_display = turtle.Turtle()
        self.game_over_display.penup()
        self.game_over_display.hideturtle()

        self.screen.listen()
        self.screen.onkeypress(self.dino.jump, "space")
        self.screen.onkeypress(self.dino.jump, "Up")

    def _draw_ground(self):
        ground = turtle.Turtle()
        ground.penup()
        ground.goto(-400, GROUND_Y)
        ground.pendown()
        ground.goto(400, GROUND_Y)
        ground.hideturtle()
        ground.color("#535353")

    def _load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE) as f:
                return json.load(f).get("high_score", 0)
        return 0

    def _save_high_score(self):
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump({"high_score": self.high_score}, f)

    def _update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  HI: {self.high_score}",
                                  font=("Courier", 14, "bold"))

    def run(self):
        frame = 0
        while self.game_running:
            self.screen.update()
            time.sleep(0.02)

            self.dino.update()
            self.score += 1
            if self.score % 100 == 0:
                self.speed += 0.3

            # Spawn obstacles
            if frame % 60 == 0:
                obs_type = random.choice(["cactus", "cactus", "cactus", "pterodactyl"])
                if obs_type == "cactus":
                    self.obstacles.append(Cactus(self.speed))
                else:
                    self.obstacles.append(Pterodactyl(self.speed))

            for obs in self.obstacles[:]:
                obs.move()
                if obs.xcor() < -420:
                    obs.hideturtle()
                    self.obstacles.remove(obs)
                elif self.dino.check_collision(obs):
                    self._game_over()
                    return

            self._update_score_display()
            frame += 1

        self.screen.exitonclick()

    def _game_over(self):
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()

        self.game_over_display.goto(0, 0)
        self.game_over_display.color("#535353")
        self.game_over_display.write(
            f"GAME OVER\nScore: {self.score}\nHigh Score: {self.high_score}\nPress space to restart",
            align="center", font=("Courier", 16, "bold")
        )

        def restart():
            self.game_over_display.clear()
            for obs in self.obstacles:
                obs.hideturtle()
            self.obstacles.clear()
            self.dino.reset()
            self.score = 0
            self.speed = 6
            self.game_running = True
            self._update_score_display()
            self.run()

        self.screen.onkeypress(restart, "space")


class Dino(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=2, stretch_len=1.5)
        self.color("#535353")
        self.penup()
        self.goto(-300, GROUND_Y + 20)
        self.vy = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.vy = 14
            self.jumping = True

    def update(self):
        if self.jumping:
            self.sety(self.ycor() + self.vy)
            self.vy -= 0.8
            if self.ycor() <= GROUND_Y + 20:
                self.sety(GROUND_Y + 20)
                self.vy = 0
                self.jumping = False

    def reset(self):
        self.goto(-300, GROUND_Y + 20)
        self.vy = 0
        self.jumping = False

    def check_collision(self, other):
        return abs(self.xcor() - other.xcor()) < 25 and abs(self.ycor() - other.ycor()) < 25


class Cactus(turtle.Turtle):
    def __init__(self, speed):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=1.5, stretch_len=0.8)
        self.color("#2d2d2d")
        self.penup()
        self.goto(420, GROUND_Y + 15)
        self.speed = speed

    def move(self):
        self.setx(self.xcor() - self.speed)


class Pterodactyl(turtle.Turtle):
    def __init__(self, speed):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.8, stretch_len=1.5)
        self.color("#8b4513")
        self.penup()
        self.goto(420, GROUND_Y + random.choice([50, 70, 90]))
        self.speed = speed

    def move(self):
        self.setx(self.xcor() - self.speed)


if __name__ == "__main__":
    game = DinoGame()
    game.run()
