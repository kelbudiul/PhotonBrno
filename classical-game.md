# Classical Game

_Prepared by Abuzer Yakaryilmaz (April 2024)_

_Based on the code given in https://realpython.com/pygame-a-primer/_

## Basics

**Step 1.** Open a new python file or project

**Step 2.** Import pygame

We use the following code to install "pygame" if not installed.

```
try:
    import pygame
except:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
```

**Step 3.** Initiate the game screen

Define the screen width and height
```
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
```

Initiate the pygame and define the screen
```
pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
```

**Step 4.** Game loop

FPS (Frame per second): The number of frames will be shown in one second. _E.g., TV shows/movies -> 24fps, live broadcast -> 30 fps, video games -> 30-120 fps._

We prepare each frame and then it is shown on the screen. 

We use an infinite loop, but we can adjust FPS for our game.

To exit from the loop, the user can close the window, which is an event that we can check inside the loop.

```
clock = pygame.time.Clock() # define a clock object to set the FPS later inside the loop

running = True
while running:
    for event in pygame.event.get(): # check all events one by one since the last frame 
        if event.type == pygame.QUIT: # if the window is closed
            running = False
    screen.fill((0, 0, 0)) # the screen background color is set to black (Red=0,Green=0,Blue=0)
    pygame.display.flip() # show everything since the last frame
    clock.tick(30) # set the FPS rate
```

_Note that we can specify color with a tuple (Red,Green,Blue), where each entry is an integer between 0 and 255._

## Our photonic ship

**Step 5:** Define the player as an Sprite object

By using (extending) an existing object, we can also use their pre-defined properties and methods. 

We use Sprite object for our photonic ship. We define a new class "Player" extending "Sprite".

```
class Player(pygame.sprite.Sprite): # define this class before the infinite loop
    def __init__(self):
        super(Player, self).__init__() # execute the __init__ method of the parent (Sprite object)
        self.surf = pygame.Surface((75, 25)) # create a surface <- our photonic ship
        self.surf.fill((255, 255, 255)) # color of our photonic ship
        self.rect = self.surf.get_rect() # create a variable to access the surface as a rectangle

player = Player() # define an instance -> our photonic ship
```

**Step 6:** Show the player on the screen

We use "blit()" method of "screen": Block transfer, "blit(surface,position or rectangle)", the position of rectange is used when rectange is specified

```
    screen.blit(player.surf, player.rect) # player is "transferred as a block" on the screen 
```

**Step 7:** Update the player position with arrows

We start with importing constants associatied with the key arrows to easily access them later.

```
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
)
```

We can directly access all pressed keys by "pygame.key.get_pressed()".

We define an "update" function within the "Player()" class taking "pressed_keys" as the input.

```
    def update(self, pressed_keys): # we move the rectangular with (x,y)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
```

What if our photonic ship goes beyond the border?

```
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
```

Now, let's call "update()" method within the infinite loop: Before "blitting" the player, we will update the player's position.

```
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]: running = False # let's exit the game if the player press "ESC"
    player.update(pressed_keys)
```
## Enemies

**Step 8:** Creating enemies in certain intervals

We define a certain time interval to create each enemy randomly on the right side of the screen.

For this purpose, we will create a new EVENT not listed in the system and call it in every 250 miliseconds. 

```
CREATING_ENEMY_TIME_INTERVAL = 250 # later we can set it to different values if we wish
ADDENEMY = pygame.USEREVENT + 1 # each event is associated with an integer
pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)
```

Now, we have a new event ADDENEMY, and we will catch it within the event loop of the infinite game loop.

```
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == ADDENEMY: # we catch the new event here and then we will create a new enemy
            print("We will create a new enemy here but before that we should define an Enemy() class") # we will replace this line
```

**Step 9.** Enemy() class

Enemies and our photonic ship are the same in principal but their sizes and moves are set differently.

```
import random # we use randomness for the position and speed of enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10)) # Enemies are smaller than our photonic ship
        self.surf.fill((255, 255, 255)) # the color of enemies - would you like to try different colors here?
        self.rect = self.surf.get_rect( # their positions are random but still they should appear on the right side
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), # position of x
                random.randint(0, SCREEN_HEIGHT), # position of y
            )
        )
        self.speed = random.randint(5, 20) # we assign a random speed - how many pixel to move to the left in each frame
```

There should be an update method for enemies as well

```
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0: # remove any enemy moveing out side of the screen
            self.kill() # a nice method inherited from Sprite()
```

**Step 10.** Collection of enemies and the player(s)

To make the things easier, we use sprite groups

```
enemies = pygame.sprite.Group() # keep all enemies - the enemies will be added in the game infinite loop
all_sprites = pygame.sprite.Group() # keep all enemies and player(s)
all_sprites.add(player) # add the player here
```

**Step 11.** Creating and displaying enemies

```
        elif event.type == ADDENEMY:  # we catch the new event here and then we will create a new enemy
            new_enemy = Enemy()
            enemies.add(new_enemy)  # add the new enemy
            all_sprites.add(new_enemy)  # add the new enemy
```

We can call "update()" for all enemies at once

```
    enemies.update() # a nice property of sprite groups
```

By using "all_sprites", we can "blitting" all enemies and the player(s). We should remove the previous "blitting" code for the player

```
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
```

_Basically, we update the player, the enemies, and then "blitting" all of them on the screen._

## Game Over

**Step 12.** Collision detection

Thanks to Sprite and Sprite groups. We can detect if any enemy hits our photonic ship by using a single line of code.

```
    if pygame.sprite.spritecollideany(player, enemies): # check if "player" is hit by any entity in the "enemies" group
        # if so: then remove the player and stop the infinite loop
        player.kill()
        running = False
```

**Step 13.** Game Over

Let's write a game over message before quitting the game. 

This message can stay for example 2 seconds before the exiting the game. So, we define a variable "there_is_message" to set "True" when we have some text to show

```
there_is_message = False
```

Here is the message to appear on the screen.

```
        my_font = pygame.font.SysFont('Comic Sans MS', 28) # create a font object
        # we create a text surface to blit on the screen
        text_surface = my_font.render("Game Over :( ", False, (255,255,0),(0,0,0)) # message / anti-aliasing effect / text color / background color
        screen.blit(text_surface, (SCREEN_WIDTH/8, SCREEN_HEIGHT/2-text_surface.get_height()/2)) # blit the text on the screen with the specified position
        there_is_message = True
```

Put a delay before leaving the infinite loop.

We import "time" library.

```
import time
```

We use "sleep()" method of "time"

```
    if there_is_message: time.sleep(2) # sleep for 2 seconds
```
