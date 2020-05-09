import pygame
import os
import random
import time
# import threading


WIDTH = 800
HEIGHT = 500
FPS = 30
playerspeed = 10

LEFT = "left"
RIGHT = "right"
DOWN = "down"
UP = "up"
STOP = 'stop'
ANIMA = "animation"


#Files
gamef = os.path.dirname(__file__)
imgf = os.path.join(gamef, "imagesforgame")
playimg = pygame.image.load(os.path.join(imgf, "p1_jump.png"))
playimg2 = pygame.image.load(os.path.join(imgf, "p1_left.png"))
enemyimg = pygame.image.load(os.path.join(imgf, "blockerMad.png"))
bg = pygame.image.load(os.path.join(imgf, "bg.png"))
anim2 = pygame.image.load(os.path.join(imgf, "hud_p1.png"))

#COLORSSS$!
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


#COOOL!!

#GAME SETTINGS
pygame.init()
pygame.mixer.music.load(os.path.join(imgf, 'loop3.mp3'))
sound1 = pygame.mixer.Sound(os.path.join(imgf, 'round_end.wav'))
sound2 = pygame.mixer.Sound(os.path.join(imgf, 'Metal Click.wav'))
pygame.mixer.music.play(loops=-1)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PLATES")
clock = pygame.time.Clock()

#Player (you)
class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = anim2
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
    #Updating to right    
    def updater(self):
        self.rect.x += playerspeed
        if self.rect.right > WIDTH:
            self.rect.right = 0

    #Updating to left
    def updatel(self):
        self.rect.x -= playerspeed
        if self.rect.left < 0:
            self.rect.left = WIDTH
    #Updating to top
    def updatet(self):
        self.rect.y -= playerspeed
        if self.rect.top < 0:
            self.rect.y = 0
    #Updating to down
    def updateb(self):
        self.rect.y += playerspeed
        if self.rect.top  > HEIGHT:
            self.rect.bottom = 0


#TROL! FACE (AHAHA it's only mobs!)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemyimg
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 12)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 12)



#Groups of sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#Start variables
move = ""
font = pygame.font.Font(None, 100)
text = font.render("GAME OVER", 1, BLACK)
place = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

font3 = pygame.font.Font(None, 50)
text3 = font3.render("PRESS R TO CONTINUE", 1, BLACK)
place3 = text3.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))

running = True
start = time.time()


#Main loop!
while running:
    pygame.mixer.music.unpause()

    #Score and losing
    sudo = True
    font2 = pygame.font.SysFont(None, 25)
    writing = str(int((time.time() - start) // 3))
    count = 0
    text2 = font2.render("Score: " + writing, 1, BLACK)
    place2 = text2.get_rect(center=(WIDTH - 50, HEIGHT - 25))
    screen.blit(text2, place2)
    if int(writing) != count:
        pygame.display.update()
        count += 1
    mobs.update()


    #Die?
    clock.tick(FPS)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        pygame.mixer.music.pause()
        sound1.play()
        while sudo:
            screen.blit(text, place)
            screen.blit(text3, place3)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sudo = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False;
                        sudo = False
                        
                    elif event.key == pygame.K_r:
                        while True:
                            start = time.time()
                            player.rect.x = random.randrange(70, WIDTH - 50)
                            player.rect.y = random.randrange(70, HEIGHT - 50)
                            if pygame.sprite.spritecollide(player, mobs, False):
                                continue;
                            move = ANIMA
                            running = True
                            sudo = False
                            break;
                        
    #Buttons
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False;

            if event.key == pygame.K_LEFT:
                sound2.play()
                move = LEFT
            elif event.key == pygame.K_RIGHT:
                sound2.play()
                move = RIGHT
            elif event.key == pygame.K_UP:
                sound2.play()
                move = UP
            elif event.key == pygame.K_DOWN:
                sound2.play()
                move = DOWN
            elif event.key == pygame.K_SPACE:
                sound2.play()
                
                if int(writing) >= 10:
                    pass;
                else:
                    move = ANIMA
                    # playerspeed += 1 

    #Moving
    if move == LEFT:
        player.image = playimg2
        player.updatel()
    elif move == RIGHT:
        player.image = playimg 
        player.updater()
    elif move == UP:
        player.image = playimg
        player.updatet()
    elif move == DOWN:
        player.image = playimg
        player.updateb()
    elif move == ANIMA:
        timing = time.time()
        player.image = anim2

    #Drawing :)
    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    pygame.display.flip()


