import pygame
import random
import sys
import time
# [1.5pt] Instead of ending the game when a player crosses the right side,
# move the player on the left side (Y coordinate should stay the same),
# display a new set of pipes and continue the game.
# [0.5pt] Crash sound - Add sound when collision happens.
class Ball:
    def __init__(self):
        self.speed = 20
        self.posX = 20
        self.posY = 350
        self.radius = 15
        self.color = (252, 3, 173)

    def update(self):
        self.posY -= self.speed
        self.posX += 2.5

    def move(self):
        self.posY += 4.5
        self.posX += 2.5

    def render(self,screen):
        pygame.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)

class Pipe:
    def __init__(self, posY, posX, height):
        self.height = height
        self.color = pygame.Color("purple")
        self.posX = posX
        self.width = 30
        self.posY = posY

    def render(self, screen):
        if(self.posY == 700):
            pygame.draw.line(screen, self.color,[self.posX,self.posY - self.height],[self.posX, self.posY], self.width)
        else:
            pygame.draw.line(screen, self.color, [self.posX, self.posY + self.height], [self.posX, self.posY], self.width)

class App:
    
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        self.ball = None
        self.pipes = []

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy Bird")
        self.ball = Ball()
        posX = 300
        height = random.randint(200,400)
        for k in range(5):
            self.pipes.append(Pipe(700, posX, height))
            self.pipes.append(Pipe(0, posX, 500 - height))
            posX += random.randint(150,200)
            height = random.randint(200,400)
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        self.events()
        self.ball.move()
        if(self.ball.posX > 1200):
            self.pipes = []
            self.ball = Ball()
            posX = 300
            height = random.randint(200, 400)
            for k in range(5):
                self.pipes.append(Pipe(700, posX, height))
                self.pipes.append(Pipe(0, posX, 500 - height))
                posX += random.randint(150, 200)
                height = random.randint(200, 400)
        self.collides()

    def collides(self):
        if(self.ball.posY - 15 < 0 or self.ball.posY + 15 > 700):
            sound = pygame.mixer.Sound("crash.mp3")
            pygame.mixer.Sound.play(sound)
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        for pipe in self.pipes:
            if(pipe.posY == 0):
              if(self.ball.posX + 15 >= pipe.posX and self.ball.posX + 15 <= pipe.posX + pipe.width and
                 self.ball.posY - 15 <= pipe.height):
                 sound = pygame.mixer.Sound("crash.mp3")
                 pygame.mixer.Sound.play(sound)
                 pygame.time.delay(2000)
                 pygame.quit()
                 sys.exit()
            elif ((self.ball.posX + 15 >= pipe.posX and self.ball.posX + 15 <= pipe.posX + pipe.width and
                    self.ball.posY + 15 >= 700 - pipe.height
            )):
                    sound = pygame.mixer.Sound("crash.mp3")
                    pygame.mixer.Sound.play(sound)
                    pygame.time.delay(2000)
                    pygame.quit()
                    sys.exit()



    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        mouse = pygame.mouse.get_pressed()
        pressed = pygame.key.get_pressed()
        if(pressed[pygame.K_SPACE] or mouse[0]):
            self.ball.update()



    def render(self):
        self.screen.fill(pygame.Color("pink"))
        self.ball.render(self.screen)
        for pipe in self.pipes:
          pipe.render(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        self.screen.fill(0, 0, 0)
        myfont = pygame.font.SysFont("monospace", 30)
        self.screen.blit(self.screen, (0, 0))
        text = myfont.render("Game is Over: You Lose!!!", True, (0, 0, 255))
        self.screen.blit(text, (600, 350))
        self.endgame = False

if __name__ == "__main__":
    app = App()
    app.run()