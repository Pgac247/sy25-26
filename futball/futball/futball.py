import pygame
import sys
import math
import random

# Basic settings
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penalty Kick - Direction and Force")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font
font = pygame.font.SysFont(None, 36)

# Goal dimensions and position
goal_width = 350
goal_height = 20
goal_x = (WIDTH - goal_width) // 2
goal_y = 50

# Ball parameters
ball_radius = 10
ball_start_pos = (WIDTH // 2, HEIGHT - 100)
ball_pos = list(ball_start_pos)
ball_velocity = [0, 0]
ball_moving = False

# Goalkeeper parameters
goalkeeper_width = 100
goalkeeper_height = 80
goalkeeper_x = (WIDTH - goalkeeper_width) // 2
goalkeeper_y = goal_y + goal_height + 10
goalkeeper_speed_base = 3

# Load pixel art assets
ball_sprite = pygame.image.load("assets_ball.png")  # Replace with your file path
ball_sprite = pygame.transform.scale(ball_sprite, (ball_radius * 5, ball_radius * 5))  # Scale to match ball size

# Load pixel art assets for the goalkeeper
goalkeeper_sprite = pygame.image.load("goalkeeper.png")  # Replace with your file path
goalkeeper_sprite = pygame.transform.scale(goalkeeper_sprite, (goalkeeper_width, goalkeeper_height))  # Scale to match goalkeeper size

# Load the background image
background_image = pygame.image.load("background.png")  # Replace with your file path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load the Piskel-drawn goal image
goal_image = pygame.image.load("goal_image.png")  # Replace with your file path
goal_image = pygame.transform.scale(goal_image, (300, 150))  # Adjust size as needed

# Direction and force
angle_deg = 90
angle_speed = 2
force = 0
force_max = 20
force_charge_speed = 0.2

# Shot type
shot_type = "normal"

# Level
level = 1
score = 0
goal_count = 0
score_for_next_level = 3

# Achievements
achievements = {"First Goal": False, "10 Goals": False, "Perfect Shot": False}

# Obstacles & goalkeepers (will be initialized per level)
obstacles = []
goalkeepers = []

# Goal display
goal_display_active = False
goal_display_timer = 0
goal_display_duration = 60  # Display for 1 second (60 frames)

def initialize_level():
    global obstacles, goalkeepers
    obstacles.clear()
    goalkeepers.clear()

    if level == 1:
        # Level 1: Single goalkeeper, no obstacles
        g_x = (WIDTH - goalkeeper_width) // 2
        g_y = goal_y + goal_height + 10
        goalkeepers.append({"x": g_x, "y": g_y, "speed": goalkeeper_speed_base, "direction": 1})
    else:
        # Level 2 and above: Add obstacles
        num_obstacles = min(level - 1, 3)  # 1 obstacle at level 2, up to 3 at higher levels
        for _ in range(num_obstacles):
            obs_x = random.randint(goal_x, goal_x + goal_width - 100)
            obs_y = goal_y + 80 + random.randint(0, 50)
            speed = 2 + level * 0.5
            obstacles.append({"x": obs_x, "y": obs_y, "speed": speed, "direction": 1})

        # Goalkeepers get faster as levels increase
        g_x = (WIDTH - goalkeeper_width) // 2
        g_y = goal_y + goal_height + 10
        g_speed = goalkeeper_speed_base + level * 0.5
        goalkeepers.append({"x": g_x, "y": g_y, "speed": g_speed, "direction": 1})

initialize_level()

def reset_ball():
    global ball_pos, ball_velocity, ball_moving
    ball_pos = list(ball_start_pos)
    ball_velocity = [0, 0]
    ball_moving = False

def draw_goal():
    pygame.draw.rect(screen, WHITE, (goal_x, goal_y, goal_width, goal_height))

def draw_aim():
    length = 100
    rad = math.radians(angle_deg)
    end_x = ball_pos[0] + length * math.cos(rad)
    end_y = ball_pos[1] - length * math.sin(rad)
    pygame.draw.line(screen, BLUE, ball_pos, (end_x, end_y), 3)
    # Show force, angle, shot type, level
    force_text = font.render(f'Force: {int(force)}', True, BLACK)
    screen.blit(force_text, (20, HEIGHT - 40))
    angle_text = font.render(f'Angle: {angle_deg}', True, BLACK)
    screen.blit(angle_text, (20, HEIGHT - 80))
    shot_text = font.render(f'Shot: {shot_type}', True, BLACK)
    screen.blit(shot_text, (20, HEIGHT - 120))
    level_text = font.render(f'Level: {level}', True, BLACK)
    screen.blit(level_text, (WIDTH - 150, 50))

def check_goal():
    goal_rect = pygame.Rect(goal_x, goal_y, goal_width, goal_height)
    ball_rect = pygame.Rect(int(ball_pos[0] - ball_radius), int(ball_pos[1] - ball_radius),
                            ball_radius * 2, ball_radius * 2)
    return goal_rect.colliderect(ball_rect)

def check_goalkeeper_collision():
    for gk in goalkeepers:
        rect = pygame.Rect(int(gk["x"]), int(gk["y"]), goalkeeper_width, goalkeeper_height)
        ball_rect = pygame.Rect(int(ball_pos[0] - ball_radius), int(ball_pos[1] - ball_radius),
                                ball_radius * 2, ball_radius * 2)
        if rect.colliderect(ball_rect):
            return True
    return False

def check_obstacle_collision():
    for obs in obstacles:
        rect = pygame.Rect(int(obs["x"]), int(obs["y"]), 100, 10)
        ball_rect = pygame.Rect(int(ball_pos[0] - ball_radius), int(ball_pos[1] - ball_radius),
                                ball_radius * 2, ball_radius * 2)
        if rect.colliderect(ball_rect):
            return True
    return False

# Main game loop
running = True
while running:
    # Draw the background
    screen.blit(background_image, (0, 0))

    draw_goal()

    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, YELLOW, (obs["x"], obs["y"], 100, 10))
        # Animate obstacles
        obs["x"] += obs["speed"] * obs["direction"]
        if obs["x"] <= goal_x or obs["x"] + 100 >= goal_x + goal_width:
            obs["direction"] *= -1

    # Animate and draw goalkeepers
    for gk in goalkeepers:
        gk["x"] += gk["speed"] * gk["direction"]
        if gk["x"] <= goal_x:
            gk["x"] = goal_x
            gk["direction"] = 1
        elif gk["x"] + goalkeeper_width >= goal_x + goal_width:
            gk["x"] = goal_x + goal_width - goalkeeper_width
            gk["direction"] = -1
        # Draw goalkeeper sprite
        screen.blit(goalkeeper_sprite, (gk["x"], gk["y"]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_deg = (angle_deg + angle_speed) % 360
            elif event.key == pygame.K_RIGHT:
                angle_deg = (angle_deg - angle_speed) % 360
            elif event.key == pygame.K_SPACE:
                charging = True
            elif event.key == pygame.K_c:
                shot_type = "curve" if shot_type == "normal" else "normal"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if not ball_moving:
                    rad = math.radians(angle_deg)
                    force_x = force * math.cos(rad)
                    force_y = -force * math.sin(rad)
                    if shot_type == "curve":
                        spin = 2 if random.choice([True, False]) else -2
                        ball_velocity = [force_x + spin, force_y]
                    else:
                        ball_velocity = [force_x, force_y]
                    ball_moving = True
                force = 0

    # Force charging
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        force += force_charge_speed
        if force > force_max:
            force = force_max

    # Move ball physics
    if ball_moving:
        ball_velocity[1] += 0.2  # gravity
        ball_pos[0] += ball_velocity[0]
        ball_pos[1] += ball_velocity[1]
        # Friction
        ball_velocity[0] *= 0.99
        ball_velocity[1] *= 0.99
        # Collisions with walls
        if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > WIDTH:
            ball_velocity[0] *= -1
        if ball_pos[1] - ball_radius < 0:
            ball_velocity[1] *= -1
        if ball_pos[1] + ball_radius > HEIGHT:
            ball_velocity[1] *= -1
        # Collisions with obstacle
        if check_obstacle_collision():
            ball_velocity[1] *= -1
        # Collisions with goalkeeper
        if check_goalkeeper_collision():
            reset_ball()
        # Goal check
        if check_goal():
            score += 1
            goal_count += 1
            goal_display_active = True  # Activate the goal display
            goal_display_timer = 0  # Reset the display timer
            # Level up check
            if goal_count >= score_for_next_level:
                level += 1
                goal_count = 0
                initialize_level()
            # Achievements
            if not achievements["First Goal"]:
                achievements["First Goal"] = True
            if score >= 10:
                achievements["10 Goals"] = True
            if int(force) == force_max:
                achievements["Perfect Shot"] = True
            reset_ball()
        elif ball_pos[1] > HEIGHT - ball_radius:
            reset_ball()

    # Draw ball
    screen.blit(ball_sprite, (int(ball_pos[0] - ball_radius), int(ball_pos[1] - ball_radius)))

    # Display the goal image
    if goal_display_active:
        screen.blit(goal_image, (WIDTH // 2 - goal_image.get_width() // 2, HEIGHT // 2 - goal_image.get_height() // 2))
        goal_display_timer += 1
        if goal_display_timer > goal_display_duration:
            goal_display_active = False

    # Draw aim and info
    length = 100
    rad = math.radians(angle_deg)
    end_x = ball_pos[0] + length * math.cos(rad)
    end_y = ball_pos[1] - length * math.sin(rad)
    pygame.draw.line(screen, BLUE, ball_pos, (end_x, end_y), 3)
    # Show info
    screen.blit(font.render(f'Force: {int(force)}', True, BLACK), (20, HEIGHT - 40))
    screen.blit(font.render(f'Angle: {angle_deg}', True, BLACK), (20, HEIGHT - 80))
    screen.blit(font.render(f'Shot: {shot_type}', True, BLACK), (20, HEIGHT - 120))
    screen.blit(font.render(f'Level: {level}', True, BLACK), (WIDTH - 150, 50))
    screen.blit(font.render(f'Goals: {score}', True, BLACK), (WIDTH - 150, 10))
    # Achievements
    for i, (k, v) in enumerate(achievements.items()):
        text = f"{k}: {'Yes' if v else 'No'}"
        screen.blit(font.render(text, True, BLACK), (10, 150 + i*30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()