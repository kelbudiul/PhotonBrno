import random
import time
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HALF_HEIGHT = SCREEN_HEIGHT // 2
CREATING_ENEMY_TIME_INTERVAL = 250
SPEED_MIN = 5
SPEED_MAX = 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, HALF_HEIGHT // 2))
        self.in_upper_screen = True
        self.allowable_top = 0
        self.allowable_bottom = HALF_HEIGHT - self.rect.height

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < self.allowable_top:
            self.rect.top = self.allowable_top
        if self.rect.bottom > self.allowable_bottom:
            self.rect.bottom = self.allowable_bottom

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(SPEED_MIN, SPEED_MAX)

    def update(self, pressed_keys):
        self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        
        if self.rect.top < 0:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
        
        if self.rect.right < 0:
            self.kill()

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, CREATING_ENEMY_TIME_INTERVAL)

player = Player()
twin_player = None
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
in_superposition = False
message = ""
message_timer = 0

def apply_not_operator():
    global player, message
    player.in_upper_screen = not player.in_upper_screen
    if player.in_upper_screen:
        player.rect.top -= HALF_HEIGHT
        player.allowable_top = 0
        player.allowable_bottom = HALF_HEIGHT - player.rect.height
    else:
        player.rect.top += HALF_HEIGHT
        player.allowable_top = HALF_HEIGHT
        player.allowable_bottom = SCREEN_HEIGHT - player.rect.height
    message = "NOT operator applied!"

def apply_hadamard_operator():
    global player, twin_player, in_superposition, message
    if not in_superposition:
        twin_player = Player()
        twin_player.rect = player.rect.copy()
        if player.in_upper_screen:
            twin_player.rect.top += HALF_HEIGHT
        else:
            twin_player.rect.top -= HALF_HEIGHT
        all_sprites.add(twin_player)
        in_superposition = True
        message = "HADAMARD operator applied! Entering superposition."
    else:
        all_sprites.remove(twin_player)
        twin_player = None
        in_superposition = False
        message = "HADAMARD operator applied! Exiting superposition."

def measure():
    global player, twin_player, in_superposition, message
    if random.choice([True, False]):
        player, twin_player = twin_player, player
    all_sprites.remove(twin_player)
    twin_player = None
    in_superposition = False
    message = "Measurement applied! Superposition collapsed."

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_ESCAPE]:
        running = False

    if not in_superposition:
        player.update(pressed_keys)
    
    for enemy in enemies:
        enemy.update(pressed_keys)

    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (0, 255, 0), (0, HALF_HEIGHT), (SCREEN_WIDTH, HALF_HEIGHT))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if not in_superposition:
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            message = "Game Over :("
            running = False
    else:
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False) + pygame.sprite.spritecollide(twin_player, enemies, False)
        if collided_enemies:
            measure()
            if pygame.sprite.spritecollideany(player, collided_enemies):
                player.kill()
                message = "Game Over :("
                running = False

    quantum_event = random.randint(0, 300)
    if quantum_event == 100 or quantum_event == 200:
        if not in_superposition:
            apply_not_operator()
    elif quantum_event == 150:
        apply_hadamard_operator()

    if message:
        font = pygame.font.SysFont('Comic Sans MS', 28)
        text_surface = font.render(message, True, (255, 255, 0))
        screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 10))
        message_timer += 1
        if message_timer > 30:  # Show message for about 1 second
            message = ""
            message_timer = 0

    pygame.display.flip()
    clock.tick(30)

if message:
    time.sleep(2)

pygame.quit()