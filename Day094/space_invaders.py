import turtle
import time
import random
import math

ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_SIZE = 30
SHIELD_BLOCKS = 20


class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("#00ff88")
        self.shapesize(stretch_wid=1, stretch_len=1.5)
        self.setheading(90)
        self.penup()
        self.goto(0, -250)
        self.speed_val = 15

    def move_left(self):
        if self.xcor() > -370:
            self.setx(self.xcor() - self.speed_val)

    def move_right(self):
        if self.xcor() < 370:
            self.setx(self.xcor() + self.speed_val)


class Bullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.3, stretch_len=0.15)
        self.color("#ffff00")
        self.penup()
        self.hideturtle()
        self.active = False
        self.speed = 12

    def fire(self, x, y):
        if not self.active:
            self.active = True
            self.goto(x, y + 15)
            self.showturtle()

    def move(self):
        if self.active:
            self.sety(self.ycor() + self.speed)
            if self.ycor() > 300:
                self.active = False
                self.hideturtle()


class EnemyBullet(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.3, stretch_len=0.15)
        self.color("#ff4444")
        self.penup()
        self.hideturtle()
        self.active = False
        self.speed = 6

    def fire(self, x, y):
        if not self.active:
            self.active = True
            self.goto(x, y - 20)
            self.showturtle()

    def move(self):
        if self.active:
            self.sety(self.ycor() - self.speed)
            if self.ycor() < -300:
                self.active = False
                self.hideturtle()


class Alien(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.8, stretch_len=1.2)
        colors = ["#ff4444", "#ff8844", "#ffaa00", "#ffcc00"]
        self.color(colors[random.randint(0, 3)])
        self.penup()
        self.goto(x, y)
        self.alive = True
        self.points = 10


class Shield(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid=0.4, stretch_len=0.8)
        self.color("#4488ff")
        self.penup()
        self.goto(x, y)
        self.health = 3

    def hit(self):
        self.health -= 1
        colors = ["#4488ff", "#2266cc", "#114488"]
        if self.health > 0:
            self.color(colors[self.health - 1])
        else:
            self.hideturtle()
            self.goto(1000, 1000)
        return self.health > 0


class SpaceInvaders:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 600)
        self.screen.bgcolor("#0a0a1a")
        self.screen.title("Space Invaders")
        self.screen.tracer(0)

        self._draw_stars()
        self.player = Player()
        self.bullet = Bullet()
        self.enemy_bullets = [EnemyBullet() for _ in range(3)]
        self.aliens = []
        self.shields = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.alien_dir = 1
        self.alien_speed = 2
        self.game_running = True

        self._create_aliens()
        self._create_shields()

        self.score_display = turtle.Turtle()
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-380, 270)

        self._setup_controls()
        self._update_score()

    def _draw_stars(self):
        star = turtle.Turtle()
        star.penup()
        star.color("white")
        star.hideturtle()
        for _ in range(80):
            star.goto(random.randint(-390, 390), random.randint(-290, 290))
            size = random.randint(1, 3)
            star.dot(size)
        self.star_turtle = star

    def _create_aliens(self):
        start_x = -200
        start_y = 180 - (self.level - 1) * 30
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLS):
                alien = Alien(start_x + col * 55, start_y - row * 45)
                self.aliens.append(alien)

    def _create_shields(self):
        for shield_x in [-200, -66, 68, 200]:
            for bx in range(-2, 3):
                for by in range(2):
                    shield = Shield(shield_x + bx * 14, -200 + by * 8)
                    self.shields.append(shield)

    def _setup_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.player.move_left, "Left")
        self.screen.onkeypress(self.player.move_right, "Right")
        self.screen.onkeypress(self.player.move_left, "a")
        self.screen.onkeypress(self.player.move_right, "d")
        self.screen.onkeypress(lambda: self.bullet.fire(self.player.xcor(), self.player.ycor()), "space")

    def _update_score(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}",
                                  font=("Courier", 14, "bold"))

    def _move_aliens(self):
        edge_reached = False
        for alien in self.aliens:
            if alien.alive:
                alien.setx(alien.xcor() + self.alien_dir * self.alien_speed)
                if abs(alien.xcor()) > 360:
                    edge_reached = True

        if edge_reached:
            self.alien_dir *= -1
            for alien in self.aliens:
                if alien.alive:
                    alien.sety(alien.ycor() - 15)

    def _enemy_shoot(self):
        if random.random() < 0.02:
            alive_aliens = [a for a in self.aliens if a.alive]
            if alive_aliens:
                shooter = random.choice(alive_aliens)
                for eb in self.enemy_bullets:
                    if not eb.active:
                        eb.fire(shooter.xcor(), shooter.ycor())
                        break

    def _check_collisions(self):
        # Player bullet vs aliens
        if self.bullet.active:
            for alien in self.aliens:
                if alien.alive and abs(self.bullet.xcor() - alien.xcor()) < 20 and abs(self.bullet.ycor() - alien.ycor()) < 15:
                    alien.alive = False
                    alien.hideturtle()
                    alien.goto(1000, 1000)
                    self.bullet.active = False
                    self.bullet.hideturtle()
                    self.score += alien.points
                    break

        # Player bullet vs shields
        if self.bullet.active:
            for shield in self.shields:
                if shield.health > 0 and abs(self.bullet.xcor() - shield.xcor()) < 10 and abs(self.bullet.ycor() - shield.ycor()) < 8:
                    shield.hit()
                    self.bullet.active = False
                    self.bullet.hideturtle()
                    break

        # Enemy bullets vs player
        for eb in self.enemy_bullets:
            if eb.active and abs(eb.xcor() - self.player.xcor()) < 18 and abs(eb.ycor() - self.player.ycor()) < 18:
                eb.active = False
                eb.hideturtle()
                self.lives -= 1
                break

        # Enemy bullets vs shields
        for eb in self.enemy_bullets:
            if eb.active:
                for shield in self.shields:
                    if shield.health > 0 and abs(eb.xcor() - shield.xcor()) < 10 and abs(eb.ycor() - shield.ycor()) < 8:
                        shield.hit()
                        eb.active = False
                        eb.hideturtle()
                        break

        # Aliens reaching bottom
        for alien in self.aliens:
            if alien.alive and alien.ycor() < -230:
                self.lives = 0
                return

    def _check_level_complete(self):
        if all(not a.alive for a in self.aliens):
            self.level += 1
            self.alien_speed += 1
            self._create_aliens()
            self._create_shields()
            return True
        return False

    def run(self):
        while self.game_running:
            self.screen.update()
            time.sleep(0.03)

            self.bullet.move()
            for eb in self.enemy_bullets:
                eb.move()

            self._move_aliens()
            self._enemy_shoot()
            self._check_collisions()
            self._update_score()

            if self.lives <= 0:
                self._game_over("GAME OVER")
                return

            if self._check_level_complete():
                self._update_score()

            if self._aliens_too_low():
                self._game_over("GAME OVER - Aliens Landed!")
                return

    def _aliens_too_low(self):
        return any(a.alive and a.ycor() < -200 for a in self.aliens)

    def _game_over(self, message):
        self.game_running = False
        t = turtle.Turtle()
        t.color("#ff4444")
        t.penup()
        t.hideturtle()
        t.write(f"{message}\nFinal Score: {self.score}\nLevel: {self.level}",
                align="center", font=("Courier", 20, "bold"))
        self.screen.exitonclick()


if __name__ == "__main__":
    SpaceInvaders().run()
