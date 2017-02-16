import pygame
import sys
import random
stars=pygame.image.load("bg.png")
background = (0, 0, 0)
entity_color = (255, 255, 255,255)
listAsteroid=[]
listLaser=[]
creationTime=100
all_sprites_list = pygame.sprite.Group()
lives=3
dead=False

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Ship(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Ship, self).__init__(x, y, width, height)

        self.image = pygame.Surface([self.width, self.height])

        ship = pygame.image.load('SpaceShip1.png')
        self.image.blit(ship, (0, 0))



class Player(Ship):
    """The player controlled Ship"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Ship should move on a given frame.
        self.y_change = 0
        # How many pixels the Ship should move each frame a key is pressed.
        self.y_dist = 5

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_UP):
            self.y_change += -self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += self.y_dist

    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_UP):
            self.y_change += self.y_dist
        elif (key == pygame.K_DOWN):
            self.y_change += -self.y_dist

    def update(self):
        """
        Moves the Ship while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(0, self.y_change)

        # If the Ship moves off the screen, put it back on.
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > window_height - self.height:
            self.rect.y = window_height - self.height


class Asteroid(Entity):
    """
    The Asteroid!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)


        self.image = pygame.Surface([width, height])
        self.image.fill(entity_color)

        self.x_direction = 5
        # Positive = down, negative = up
        # self.y_direction = 1
        # # Current speed.
        self.speed = 5

    def update(self):
        # Move the Asteroid!
        #self.rect.move_ip(self.speed * self.x_direction)
        self.rect.x-=5
        # Keep the Asteroid in bounds, and make it bounce off the sides.
        # if self.rect.y < 0:
        #     self.y_direction *= -1
        # elif self.rect.y > window_height - 20:
        #     self.y_direction *= -1

def checkAsteroid(all):
    for i in all:
        if i.rect.x<=0:
            i.remove(all_sprites_list)
            all.remove(i)

def checkKill(all):
    global lives
    for i in all:
        if i.rect.colliderect(player.rect):
            all.remove(i)
            killed=True
            print('dead')
            lives-=1
            print(lives)





pygame.init()

window_width = 700
window_height = 400
screen = pygame.display.set_mode((window_width, window_height))
screen.blit(stars,(0,0))
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

one = Asteroid(window_width, random.randint(10,window_height-10), 20, 20)
listAsteroid.append(one)
player = Player(20, window_height / 2, 40, 37)
#y = Enemy(window_width - 40, window_height / 2, 64, 64)


all_sprites_list.add(one)
all_sprites_list.add(player)
#all_sprites_list.add(enemy)

while True:
    checkKill(listAsteroid)
    if creationTime==0:
        x=Asteroid(window_width-1, random.randint(20,window_height-10), 20, 20)
        listAsteroid.append(x)
        all_sprites_list.add(x)
        checkAsteroid(listAsteroid)

        creationTime=100
    # Event processing here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)

    for ent in all_sprites_list:
        ent.update()

    screen.blit(stars,(0,0))

    all_sprites_list.draw(screen)
    creationTime-=1
    pygame.display.flip()

    clock.tick(60)
