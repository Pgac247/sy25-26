import pygame
import math
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")
font = pygame.font.SysFont(None, 36)

# Track parameters
center_x = WIDTH // 2
center_y = HEIGHT // 2
track_radius_x = 350
track_radius_y = 250

# Global variables: Initialize victories list
victories = [0, 0, 0, 0, 0]
money = 100

# Load the single horse sprite
horse_sprite_sheet = pygame.image.load('assets/horse_spritesheet.png').convert_alpha()
num_frames = 4  # Adjust to your sprite sheet frames
frame_width = 64
frame_height = 64
horse_frames = []

for f in range(num_frames):
    frame = horse_sprite_sheet.subsurface(pygame.Rect(f * frame_width, 0, frame_width, frame_height))
    horse_frames.append(frame)

# Initialize animation frame index
horse_current_frame = 0
animation_timer = 0
animation_speed = 0.2  # seconds per frame

# Create horses with unique IDs
horses = []
colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
for i in range(5):
    speed = 0.02 + random.uniform(0, 0.005)
    horses.append({
        'angle': 0,
        'prev_angle': 0,
        'speed': speed,
        'laps': 0,
        'radius_x': track_radius_x,
        'radius_y': track_radius_y,
        'id': i+1,  # Horse number
        'color': colors[i]
    })

def draw_pixel_background():
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT - 150, WIDTH, 150))
    pygame.draw.ellipse(screen, (210, 180, 140),
                        (center_x - track_radius_x, center_y - track_radius_y,
                         2 * track_radius_x, 2 * track_radius_y))

def draw_horses(horses, frame_idx):
    for horse in horses:
        x = center_x + horse['radius_x'] * math.cos(horse['angle'])
        y = center_y + horse['radius_y'] * math.sin(horse['angle'])
        frame = horse_frames[frame_idx]
        # Draw sprite centered at (x, y)
        screen.blit(frame, (int(x) - frame_width//2, int(y) - frame_height//2))
        # Draw horse number above sprite
        number_text = font.render(f"H{horse['id']}", True, (0, 0, 0))
        text_rect = number_text.get_rect(center=(int(x), int(y) - frame_height//2 - 10))
        screen.blit(number_text, text_rect)

def show_text(text, y):
    render = font.render(text, True, (0, 0, 0))
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def show_stats():
    y = 250
    for i, v in enumerate(victories):
        show_text(f"Horse {i+1}: {v} wins", y + i*30)

def check_passed_start(horse):
    prev_angle = horse['prev_angle']
    angle = horse['angle']
    return prev_angle > 2*math.pi - 0.1 and angle < 0.1

def betting():
    global money
    bet = 0
    selected = 0
    confirmed = False
    while not confirmed:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_data()
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if bet + 10 <= money:
                        bet += 10
                elif e.key == pygame.K_DOWN:
                    if bet - 10 >= 0:
                        bet -= 10
                elif e.key == pygame.K_1:
                    selected = 0
                elif e.key == pygame.K_2:
                    selected = 1
                elif e.key == pygame.K_3:
                    selected = 2
                elif e.key == pygame.K_4:
                    selected = 3
                elif e.key == pygame.K_5:
                    selected = 4
                elif e.key == pygame.K_RETURN:
                    if bet > 0 and bet <= money:
                        confirmed = True
        draw_pixel_background()
        show_text(f"Money: {money}", 50)
        show_text(f"Bet: {bet}", 100)
        show_text(f"Horse: {selected+1}", 150)
        show_text("Use UP/DOWN to bet, 1-5 to select, ENTER to confirm", 200)
        pygame.display.flip()
    return bet, selected

def save_data():
    import json
    data = {"money": money, "victories": victories}
    with open("save_game.json", "w") as f:
        json.dump(data, f)

def run_race():
    global money, victories, horse_frames, horse_current_frame, animation_timer
    horses = []
    start_angle = 0
    for i in range(5):
        speed = 0.02 + random.uniform(0, 0.005)
        horses.append({
            'angle': start_angle,
            'prev_angle': start_angle,
            'speed': speed,
            'laps': 0,
            'radius_x': track_radius_x,
            'radius_y': track_radius_y,
            'id': i+1,
        })

    bet, chosen = betting()

    clock = pygame.time.Clock()
    winner = None
    finished = False
    horse_frames_idx = [0 for _ in range(5)]
    animation_timer = 0

    while not finished:
        dt = clock.tick(60) / 1000
        animation_timer += dt

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_data()
                pygame.quit()
                sys.exit()

        # Update horse positions
        for horse in horses:
            horse['prev_angle'] = horse['angle']
            horse['angle'] += horse['speed']
            if horse['angle'] > 2 * math.pi:
                horse['angle'] -= 2 * math.pi
            if check_passed_start(horse):
                horse['laps'] += 1

        # Animate sprite frames
        if animation_timer >= animation_speed:
            for i in range(5):
                horse_frames_idx[i] = (horse_frames_idx[i] + 1) % num_frames
            animation_timer = 0

        # Check for winner
        for i, h in enumerate(horses):
            if h['laps'] >= 3:
                winner = i
                finished = True
                break

        # Draw everything
        draw_pixel_background()
        draw_horses(horses, horse_frames_idx)
        pygame.display.flip()

    # Update victories
    victories[winner] += 1

    # Payout
    if bet == winner:
        money += bet * 2
        result_text = "You Win!"
    else:
        money -= bet
        result_text = "You Lose!"

    # Show result for a few seconds
    for _ in range(120):
        draw_pixel_background()
        draw_horses(horses, horse_frames_idx)
        show_text(f"Horse {winner+1} wins!", 50)
        show_text(result_text, 100)
        show_stats()
        pygame.display.flip()
        pygame.time.wait(16)

# Main game loop
def main():
    global money, victories, horse_frames_idx, animation_timer
    # Load previous data if exists
    try:
        with open("save_game.json", "r") as f:
            import json
            data = json.load(f)
            money = data["money"]
            victories = data["victories"]
    except:
        pass

    # Initialize animation timer
    animation_timer = 0

    while True:
        draw_pixel_background()
        show_text("Press SPACE to start the race", HEIGHT - 80)
        show_stats()
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    save_data()
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        waiting = False
        run_race()
        # Ask if they want to play again
        waiting_continue = True
        while waiting_continue:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    save_data()
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        save_data()
                        pygame.quit()
                        sys.exit()
                    elif e.key == pygame.K_SPACE:
                        waiting_continue = False

if __name__ == "__main__":
    main()