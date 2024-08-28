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


QUANTUM_CHECK_INTERVAL = 30  # Check every 30 frames (about 1 second at 30 FPS)
NOT_PROBABILITY = 2 / 301
HADAMARD_PROBABILITY = 1 / 301

frame_count = 0

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
        if pressed_keys is None:
            # Normal movement when not in superposition
            self.rect.move_ip(-self.speed, 0)
        else:
            # Movement based on arrow keys when in superposition
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
        
        # Border wrapping logic remains the same
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
    print("#")
    global player, twin_player, in_superposition, message
    if random.choice([True, False]):
        player, twin_player = twin_player, player
    player.in_upper_screen = player.rect.top < HALF_HEIGHT
    all_sprites.remove(twin_player)
    twin_player = None
    in_superposition = False
    message = "Measurement applied! Superposition collapsed."

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDENEMY and not in_superposition:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


    pressed_keys = pygame.key.get_pressed()

    if not in_superposition:
        player.update(pressed_keys)
        # Enemies should move automatically (as they do now)
        for enemy in enemies:
            enemy.update(None)  # Pass None to indicate no key presses
    else:
        # In superposition, only move enemies based on arrow keys
        for enemy in enemies:
            enemy.update(pressed_keys)

    # Draw game elements
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (0, 255, 0), (0, HALF_HEIGHT), (SCREEN_WIDTH, HALF_HEIGHT))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check for collisions
    if not in_superposition:
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            message = "Game Over :("
            running = False
    else:
        # Check collisions when in superposition
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False) + pygame.sprite.spritecollide(twin_player, enemies, False)
        if collided_enemies:
            # Perform measurement (collapse superposition)
            measure()
            # Check if any collided enemy is in the same screen as the collapsed player
            game_over = False
            for enemy in collided_enemies:
                if (player.in_upper_screen and enemy.rect.top < HALF_HEIGHT) or \
                (not player.in_upper_screen and enemy.rect.top >= HALF_HEIGHT):
                    game_over = True
                    break
            
            if game_over:
                player.kill()
                message = "Game Over :("
                running = False
                print(1)
            else:
                message = "Close call! Superposition collapsed, but you survived."
            
            # Remove the collided enemies
            for enemy in collided_enemies:
                enemy.kill()
    # The randomization occurs every frame, which at 30 FPS means 
    # about 30 chances per second to apply an operator. 
    # This might lead to more frequent operator applications 
    # than intended.
    frame_count += 1
    if frame_count >= QUANTUM_CHECK_INTERVAL:
        frame_count = 0
    if not in_superposition and random.random() < NOT_PROBABILITY:
        apply_not_operator()
    elif random.random() < HADAMARD_PROBABILITY:
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

# Display final message before quitting
if message:
    time.sleep(10)

pygame.quit()