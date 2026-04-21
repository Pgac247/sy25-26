import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player properties
player_base_size = 50  # Base size
player_size = player_base_size

player_pos = [WIDTH // 2, HEIGHT - 50]

# Load your sprite
player_sprite = pygame.image.load('player_sprite.png').convert_alpha()

# Enemy properties
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
base_enemy_speed = 10  # starting speed
enemy_speed = base_enemy_speed

score = 0
game_over = False

# Load enemy Piskel sprite
enemy_sprite = pygame.image.load('enemy_sprite.png').convert_alpha()

# Screenshake variables
shake_duration = 0
shake_magnitude = 5  # How intense the shake is

# Near miss jitter variables
near_miss_jitter = False
near_miss_duration = 0
distance_threshold = 100  # Threshold for near miss detection

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # --- Movement Logic ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5

    # Keep player within bounds
    if player_pos[0] < 0:
        player_pos[0] = 0
    elif player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size

    # Increase difficulty based on score
    enemy_speed = base_enemy_speed + (score // 5) * 2
    max_speed = 25
    if enemy_speed > max_speed:
        enemy_speed = max_speed

    # Increase player size with difficulty
    player_size = player_base_size + (score // 5) * 5  # grow 5 pixels every 5 points
    # Limit the size to prevent it from becoming too big
    if player_size > 100:
        player_size = 100

    # Scale player sprite
    scaled_player_sprite = pygame.transform.scale(player_sprite, (player_size, player_size))

    # Update enemy position
    enemy_pos[1] += enemy_speed

    # Reset enemy if it goes off-screen
    if enemy_pos[1] > HEIGHT:
        enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        score += 1
        print(f"Score: {score}")

    # Collision detection
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)

    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        game_over = True
        shake_duration = 20

    # Detect near miss (enemy close but no collision)
    enemy_center = (enemy_pos[0] + enemy_size / 2, enemy_pos[1] + enemy_size / 2)
    player_center = (player_pos[0] + player_size / 2, player_pos[1] + player_size / 2)
    distance = ((enemy_center[0] - player_center[0]) ** 2 + (enemy_center[1] - player_center[1]) ** 2) ** 0.5

    if not player_rect.colliderect(enemy_rect) and distance < distance_threshold:
        near_miss_jitter = True
        near_miss_duration = 10  # frames

    # Screenshake and jitter logic
    if shake_duration > 0:
        offset_x = random.randint(-shake_magnitude, shake_magnitude)
        offset_y = random.randint(-shake_magnitude, shake_magnitude)
        shake_duration -= 1
    elif near_miss_jitter and near_miss_duration > 0:
        # Add subtle jitter for near miss
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        near_miss_duration -= 1
    else:
        offset_x = 0
        offset_y = 0
        near_miss_jitter = False

    # Drawing
    screen.fill((0, 0, 0))
    # Draw enemy sprite
    screen.blit(enemy_sprite, (enemy_rect.x + offset_x, enemy_rect.y + offset_y))
    # Draw scaled player sprite
    screen.blit(scaled_player_sprite, (player_pos[0] + offset_x, player_pos[1] + offset_y))

    pygame.display.update()
    clock.tick(30)

pygame.quit()