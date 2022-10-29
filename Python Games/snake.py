import pygame
import sys
import random
# [1pt] Score - Add scoring system to the game.
# Every time snake eats food player earns some points which should be displayed at the upper part of the screen.
# [0.5pt] Forbid 180 degree turns - If the snake is moving upwards and the player presses
# S or Down Arrow it should not be counted as collision and the snake should continue moving in the initial direction.
# These rules should apply to all 4 directions.
# [0.5pt] Crash sound - Add sound when collision happens.
class Snake():
    def __init__(self):
        self.length = 5
        self.positions = [((screen_width/4), (screen_height/4))]
        self.direction = right
        self.color = pygame.Color("orange")
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))), (cur[1]+(y*gridsize)))
        if len(self.positions) > 2 and new in self.positions[2:]:
            sound = pygame.mixer.Sound("crash.mp3")
            pygame.mixer.Sound.play(sound)
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.circle(surface, self.color, (p[0] + 9, p[1] + 9), 9)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.turn(up)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.turn(down)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.color = (0, 170, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.circle(surface,self.color,(self.position[0] + 9, self.position[1] + 9),9)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)



screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)



class App:

    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None

    def run(self):
        pygame.init()
        self.running = True

        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

        surface = pygame.Surface(self.screen.get_size())
        surface = surface.convert()
        drawGrid(surface)

        self.snake = Snake()
        food = Food()

        myfont = pygame.font.SysFont("monospace", 25)

        while (self.running):
            clock.tick(10)
            self.snake.handle_keys()
            drawGrid(surface)
            self.snake.move()
            if (self.snake.get_head_position()[0] > 480 or self.snake.get_head_position()[0] < 0):
                sound = pygame.mixer.Sound("crash.mp3")
                pygame.mixer.Sound.play(sound)
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            if (self.snake.get_head_position()[1] > 480 or self.snake.get_head_position()[1] < 0):
                sound = pygame.mixer.Sound("crash.mp3")
                pygame.mixer.Sound.play(sound)
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            if self.snake.get_head_position() == food.position:
                self.snake.length += 1
                self.snake.score += 1
                food.randomize_position()
            self.snake.draw(surface)
            food.draw(surface)
            self.screen.blit(surface, (0, 0))
            text = myfont.render("Score {0}".format(self.snake.score), 1, (0, 0, 0))
            self.screen.blit(text, (5, 10))
            pygame.display.update()

        self.cleanUp()

    def init(self):
        pass


    def update(self):
        self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        pass

    def cleanUp(self):
        self.screen = pygame.display.set_mode((480, 480))
        self.screen.fill((0, 0, 0))
        surface = pygame.Surface(self.screen.get_size())
        myfont = pygame.font.SysFont("monospace", 25)
        self.screen.blit(surface, (0,0))
        text = myfont.render("Game is Over: Your Score is {0}".format(self.snake.score), 1, pygame.Color("blue"))
        self.screen.blit(text, (240, 240))



if __name__ == "__main__":
        app = App()
        app.run()