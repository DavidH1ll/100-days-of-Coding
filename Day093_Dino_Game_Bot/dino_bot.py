import turtle
import time


class DinoBot:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

    def decide(self):
        dino_x = self.game.dino.xcor()
        dino_y = self.game.dino.ycor()

        for obs in self.game.obstacles:
            dist = obs.xcor() - dino_x
            if 30 < dist < 150:
                if obs.ycor() > GROUND_Y + 30:
                    if dino_y <= GROUND_Y + 25 and not self.game.dino.jumping:
                        return
                else:
                    if not self.game.dino.jumping:
                        self.game.dino.jump()
                        return

    def run_with_bot(self):
        frame = 0
        while self.game.game_running:
            self.screen.update()
            time.sleep(0.015)

            self.decide()
            self.game.dino.update()
            self.game.score += 1
            if self.game.score % 100 == 0:
                self.game.speed += 0.3

            if frame % 60 == 0:
                import random
                obs_type = random.choice(["cactus", "cactus", "cactus", "pterodactyl"])
                if obs_type == "cactus":
                    self.game.obstacles.append(Cactus(self.game.speed))
                else:
                    self.game.obstacles.append(Pterodactyl(self.game.speed))

            for obs in self.game.obstacles[:]:
                obs.move()
                if obs.xcor() < -420:
                    obs.hideturtle()
                    self.game.obstacles.remove(obs)
                elif self.game.dino.check_collision(obs):
                    self.game._game_over()
                    return

            self.game._update_score_display()
            frame += 1


GROUND_Y = -200


if __name__ == "__main__":
    print("Starting Dino Game with AI Bot...")
    print("The bot analyzes obstacle distance and type to decide when to jump.")
    print("Watch the turtle window!")

    from dino_game import DinoGame, Cactus, Pterodactyl

    game = DinoGame()
    bot = DinoBot(game)
    bot.run_with_bot()
