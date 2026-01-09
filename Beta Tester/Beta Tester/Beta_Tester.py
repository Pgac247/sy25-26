import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Isaac-Style Large Rooms with Keys")

# Colors
BLACK = (0, 0, 0)
ROOM_COLOR = (60, 60, 60)
BORDER_COLOR = (100, 100, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()

# Rooms and connections
rooms = [(0, 0), (1, 0), (0, 1), (1, 1)]
connections = {
    (0, 0): [{'room': (1, 0), 'side': 'right'}],
    (1, 0): [{'room': (0, 0), 'side': 'left'}, {'room': (1, 1), 'side': 'down'}],
    (0, 1): [{'room': (0, 0), 'side': 'up'}, {'room': (1, 1), 'side': 'right'}],
    (1, 1): [{'room': (1, 0), 'side': 'up'}, {'room': (0, 1), 'side': 'left'}],
}

MIN_X, MIN_Y = 0, 0
ROOM_SIZE = 300
MARGIN = 50

def world_to_screen(x, y):
    return ((x - MIN_X) * ROOM_SIZE + MARGIN, (y - MIN_Y) * ROOM_SIZE + MARGIN)

# Initialize room keys dictionary
room_keys = {}
for room in rooms:
    room_keys[room] = []

# Place a key in a random room (excluding the first)
key_room = random.choice(rooms[1:])
room_keys[key_room].append('red_key')

# Current room
current_room = (0, 0)

def get_player_position(room):
    rx, ry = world_to_screen(*room)
    return [rx + (ROOM_SIZE - 20) / 2, ry + (ROOM_SIZE - 20) / 2]

player_pos = get_player_position(current_room)

# Enemies (none in first room)
enemies = []

def spawn_enemies(room):
    rx, ry = world_to_screen(*room)
    enemies_list = []
    if room != (0, 0):
        for _ in range(3):
            x = rx + random.randint(50, ROOM_SIZE - 50)
            y = ry + random.randint(50, ROOM_SIZE - 50)
            enemies_list.append([x, y, 20])
    return enemies_list

enemies = spawn_enemies(current_room)

def draw_room(x, y):
    pygame.draw.rect(screen, ROOM_COLOR, (x, y, ROOM_SIZE, ROOM_SIZE))
    # Walls
    pygame.draw.rect(screen, BORDER_COLOR, (x, y, ROOM_SIZE, 10))
    pygame.draw.rect(screen, BORDER_COLOR, (x, y + ROOM_SIZE - 10, ROOM_SIZE, 10))
    pygame.draw.rect(screen, BORDER_COLOR, (x, y, 10, ROOM_SIZE))
    pygame.draw.rect(screen, BORDER_COLOR, (x + ROOM_SIZE - 10, y, 10, ROOM_SIZE))

def draw_doors(x, y, room, connections):
    for conn in connections.get(room, []):
        side = conn['side']
        if side == 'up':
            rect = pygame.Rect(x + ROOM_SIZE/2 - 40, y - 10, 80, 10)
        elif side == 'down':
            rect = pygame.Rect(x + ROOM_SIZE/2 - 40, y + ROOM_SIZE, 80, 10)
        elif side == 'left':
            rect = pygame.Rect(x - 10, y + ROOM_SIZE/2 - 40, 10, 80)
        elif side == 'right':
            rect = pygame.Rect(x + ROOM_SIZE, y + ROOM_SIZE/2 - 40, 10, 80)
        pygame.draw.rect(screen, (150, 150, 150), rect)

def get_door_rects(x, y, room, connections):
    rects = []
    for conn in connections.get(room, []):
        side = conn['side']
        if side == 'up':
            rects.append(pygame.Rect(x + ROOM_SIZE/2 - 40, y - 10, 80, 10))
        elif side == 'down':
            rects.append(pygame.Rect(x + ROOM_SIZE/2 - 40, y + ROOM_SIZE, 80, 10))
        elif side == 'left':
            rects.append(pygame.Rect(x - 10, y + ROOM_SIZE/2 - 40, 10, 80))
        elif side == 'right':
            rects.append(pygame.Rect(x + ROOM_SIZE, y + ROOM_SIZE/2 - 40, 10, 80))
    return rects

def main():
    global current_room, enemies, player_pos
    running = True
    while running:
        screen.fill(BLACK)

        # Draw rooms and doors
        for room in rooms:
            x, y = world_to_screen(*room)
            draw_room(x, y)
            draw_doors(x, y, room, connections)

        # Player always in the center
        rx, ry = world_to_screen(*current_room)
        player_pos = [rx + (ROOM_SIZE - 20) / 2, ry + (ROOM_SIZE - 20) / 2]
        pygame.draw.rect(screen, GREEN, (*player_pos, 20, 20))

        # Check for 'E' key press to go through doors
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or keys[pygame.K_e]:
            mouse_pos = pygame.mouse.get_pos()
            door_rects = get_door_rects(rx, ry, current_room, connections)
            for rect in door_rects:
                if rect.collidepoint(mouse_pos):
                    # Find the connection and change room
                    for conn in connections.get(current_room, []):
                        side = conn['side']
                        neighbor = conn['room']
                        # Match the door rect
                        if side == 'up' and rect == pygame.Rect(rx + ROOM_SIZE/2 - 40, ry - 10, 80, 10):
                            current_room = neighbor
                        elif side == 'down' and rect == pygame.Rect(rx + ROOM_SIZE/2 - 40, ry + ROOM_SIZE, 80, 10):
                            current_room = neighbor
                        elif side == 'left' and rect == pygame.Rect(rx - 10, ry + ROOM_SIZE/2 - 40, 10, 80):
                            current_room = neighbor
                        elif side == 'right' and rect == pygame.Rect(rx + ROOM_SIZE, ry + ROOM_SIZE/2 - 40, 10, 80):
                            current_room = neighbor
                    enemies = spawn_enemies(current_room)
                    break

        # Draw enemies (none in first room)
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 20, 20))
            # Enemies are static

        # Check collision with enemies
        for enemy in enemies:
            if pygame.Rect(enemy[0], enemy[1], 20, 20).colliderect(pygame.Rect(player_pos[0], player_pos[1], 20, 20)):
                print("You got caught! Game Over.")
                running = False

        # Draw keys
        for room in room_keys:
            for key in room_keys[room]:
                pos = world_to_screen(*room)
                pygame.draw.rect(screen, YELLOW, (pos[0] + ROOM_SIZE/2 - 10, pos[1] + ROOM_SIZE/2 - 10, 20, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()