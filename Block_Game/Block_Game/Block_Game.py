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
player_pos = [WIDTH // 2, HEIGHT - 50]
player_size = 50

# Enemy properties
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 10

score = 0
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # --- Corrected Movement Logic ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5  # Move left
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5  # Move right

    # Keep player within bounds
    if player_pos[0] < 0:
        player_pos[0] = 0
    elif player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size

    # Update enemy position
    enemy_pos[1] += enemy_speed

    # --- Corrected Enemy Reset ---
    if enemy_pos[1] > HEIGHT:
        enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        score += 1
        print(f"Score: {score}")

    # --- Corrected Collision Detection ---
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], enemy_size, enemy_size)

    if player_rect.colliderect(enemy_rect):
        print("Game Over!")
        game_over = True

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, RED, enemy_rect)
    pygame.draw.rect(screen, BLUE, player_rect)

    pygame.display.update()
    clock.tick(30)

pygame.quit()