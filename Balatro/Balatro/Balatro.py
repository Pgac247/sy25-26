import pygame
import random
import os
import json

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balatro Poker - No Sounds")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 40)

# Card dimensions
CARD_WIDTH, CARD_HEIGHT = 80, 120

# Card suits and ranks
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Save high scores / levels
scores_file = "highscores_levels.json"
if os.path.exists(scores_file):
    with open(scores_file, 'r') as f:
        save_data = json.load(f)
else:
    save_data = {
        'slots': {
            '1': {'highscore': 0, 'level': 1},
            '2': {'highscore': 0, 'level': 1},
            '3': {'highscore': 0, 'level': 1}
        }
    }

def save_progress():
    with open(scores_file, 'w') as f:
        json.dump(save_data, f)

# Game variables
chips = 1000
current_slot = '1'
current_level = 1
hand = []
deck = []
hold_flags = []
evaluate_result = ""

# Level parameters
def get_level_params(level):
    num_cards = 5 + level  # increase number of cards with level
    starting_chips = max(1000 - level*200, 200)
    return num_cards, starting_chips

def load_level():
    global num_cards, chips, level
    level_info = save_data['slots'][str(current_slot)]
    level = level_info['level']
    num_cards, chips = get_level_params(level)

def create_deck():
    deck_list = [{'suit': s, 'rank': r} for s in suits for r in ranks]
    random.shuffle(deck_list)
    return deck_list

def start_level():
    global deck, hand, chips, hold_flags, evaluate_result
    deck = create_deck()
    load_level()
    deal_hand()
    hold_flags = [False] * len(hand)
    evaluate_result = ""

def deal_hand():
    global deck, hand
    num_cards, _ = get_level_params(level)
    if len(deck) < num_cards:
        deck = create_deck()
    hand = [deck.pop() for _ in range(num_cards)]

def evaluate_hand(hand):
    ranks_in_hand = [card['rank'] for card in hand]
    suits_in_hand = [card['suit'] for card in hand]
    rank_counts = {r: ranks_in_hand.count(r) for r in set(ranks_in_hand)}
    counts = list(rank_counts.values())

    is_flush = len(set(suits_in_hand)) == 1
    sorted_ranks = sorted([ranks.index(r) for r in ranks_in_hand])
    is_straight = all([sorted_ranks[i] - sorted_ranks[i - 1] == 1 for i in range(1, len(sorted_ranks))])

    if 4 in counts:
        return ('Four of a Kind', 25)
    elif 3 in counts and 2 in counts:
        return ('Full House', 9)
    elif is_flush and is_straight:
        return ('Straight Flush', 50)
    elif is_flush:
        return ('Flush', 6)
    elif is_straight:
        return ('Straight', 4)
    elif 3 in counts:
        return ('Three of a Kind', 3)
    elif counts.count(2) == 2:
        return ('Two Pair', 2)
    elif 2 in counts:
        return ('One Pair', 1)
    else:
        return ('High Card', 0)

# UI Elements
slot_buttons = [
    pygame.Rect(50, 20, 130, 40),
    pygame.Rect(200, 20, 130, 40),
    pygame.Rect(350, 20, 130, 40)
]
reset_button = pygame.Rect(500, 20, 150, 40)
start_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 80, 120, 40)
bet_button_rect = pygame.Rect(WIDTH // 2 + 60, HEIGHT - 150, 80, 50)

# Game state
game_state = 'menu'  # 'menu', 'playing'
bet_input_active = False
bet_input_text = ""
bet = 0

# Functions
def start_game():
    global deck, hand, chips, hold_flags, evaluate_result
    deck = create_deck()
    load_level()
    deal_hand()
    hold_flags = [False] * len(hand)
    evaluate_result = ""

def draw_ui():
    # Show highscore, level, chips
    info = save_data['slots'][str(current_slot)]
    highscore = info['highscore']
    level = info['level']
    chips_text = font.render(f"Chips: {chips}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(chips_text, (10, 80))
    screen.blit(highscore_text, (10, 110))
    screen.blit(level_text, (10, 140))

def draw_game():
    draw_ui()
    # Draw hand
    for i, card in enumerate(hand):
        rect = pygame.Rect(50 + i*150, HEIGHT//2 - CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        # Draw face
        font_small = pygame.font.SysFont(None, 24)
        rank_text = font_small.render(card['rank'], True, BLACK)
        suit_text = font_small.render(card['suit'][0], True, BLACK)
        screen.blit(rank_text, (rect.x + 10, rect.y + 10))
        screen.blit(suit_text, (rect.x + 10, rect.y + 40))
        # Hold highlight
        if hold_flags[i]:
            pygame.draw.rect(screen, YELLOW, rect, 3)
    # Show current bet
    screen.blit(font.render(f"Bet: {bet}", True, WHITE), (10, 170))
    # Show evaluation result
    screen.blit(font.render(evaluate_result, True, WHITE), (WIDTH // 2 - 150, 20))
    # Deal button
    pygame.draw.rect(screen, GRAY, pygame.Rect(WIDTH//2 - 50, HEIGHT - 150, 100, 50))
    screen.blit(font.render("Deal", True, BLACK), (WIDTH//2 - 15, HEIGHT - 135))
    # Bet button
    pygame.draw.rect(screen, GRAY, pygame.Rect(WIDTH//2 + 60, HEIGHT - 150, 80, 50))
    screen.blit(font.render("Bet", True, BLACK), (WIDTH//2 + 70, HEIGHT - 135))
    # If chips depleted
    if chips <= 0:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        game_over_text = big_font.render("Out of Chips! Game Over.", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 20))
        save_progress()
        pygame.display.flip()
        pygame.time.wait(3000)
        # Restart
        game_state = 'menu'

# Main loop
running = True
while running:
    screen.fill(DARK_GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if game_state == 'menu':
                # Slot selection
                for i, rect in enumerate(slot_buttons, start=1):
                    if rect.collidepoint(mx, my):
                        current_slot = str(i)
                # Reset highscore
                if reset_button.collidepoint(mx, my):
                    save_data['slots'][str(current_slot)]['highscore'] = 0
                # Start game
                if start_button.collidepoint(mx, my):
                    start_game()
                    game_state = 'playing'
            elif game_state == 'playing':
                # Hold toggle
                for i in range(len(hand)):
                    rect = pygame.Rect(50 + i*150, HEIGHT//2 - CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT)
                    if rect.collidepoint(mx, my):
                        hold_flags[i] = not hold_flags[i]
                # Deal
                deal_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 150, 100, 50)
                if deal_rect.collidepoint(mx, my):
                    if bet > 0 and bet <= chips:
                        # Deal with animation (skipped here for simplicity)
                        for i, card in enumerate(hand):
                            rect = pygame.Rect(50 + i*150, HEIGHT//2 - CARD_HEIGHT//2, CARD_WIDTH, CARD_HEIGHT)
                            # Animation could be added here
                        for i in range(len(hand)):
                            if not hold_flags[i]:
                                if len(deck) == 0:
                                    deck = create_deck()
                                hand[i] = deck.pop()
                        # Evaluate hand
                        hand_rank, payout_multiplier = evaluate_hand(hand)
                        payout = bet * payout_multiplier
                        chips += payout
                        # Update highscore
                        if chips > save_data['slots'][str(current_slot)]['highscore']:
                            save_data['slots'][str(current_slot)]['highscore'] = chips
                        # Level up
                        if chips > 2000 and save_data['slots'][str(current_slot)]['level'] < 10:
                            save_data['slots'][str(current_slot)]['level'] += 1
                        hold_flags = [False] * len(hand)
                        evaluate_result = f"{hand_rank}! Payout: {payout} chips."
                    else:
                        evaluate_result = "Place a valid bet!"
                # Bet button
                bet_rect = pygame.Rect(WIDTH//2 + 60, HEIGHT - 150, 80, 50)
                if bet_rect.collidepoint(mx, my):
                    bet_input_active = True
                    bet_input_text = ""
        elif event.type == pygame.KEYDOWN:
            if bet_input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        new_bet = int(bet_input_text)
                        if new_bet > chips:
                            evaluate_result = "Bet exceeds chips!"
                        elif new_bet <= 0:
                            evaluate_result = "Bet must be positive!"
                        else:
                            bet = new_bet
                            evaluate_result = f"Bet of {bet} chips."
                        bet_input_active = False
                    except:
                        evaluate_result = "Invalid bet!"
                        bet_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    bet_input_text = bet_input_text[:-1]
                elif event.unicode.isdigit():
                    bet_input_text += event.unicode

    # Draw interface
    if 'game_state' not in locals() or game_state == 'menu':
        # Draw menu
        title = big_font.render("Balatro Poker - Select Slot & Level", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 10))
        for i, rect in enumerate(slot_buttons, start=1):
            info = save_data['slots'][str(i)]
            label = f"Slot {i} - High: {info['highscore']} - Lvl {info['level']}"
            color = LIGHT_BLUE if str(i)==str(current_slot) else GRAY
            pygame.draw.rect(screen, color, rect)
            txt = font.render(label, True, BLACK)
            screen.blit(txt, (rect.x+5, rect.y+5))
        pygame.draw.rect(screen, GRAY, reset_button)
        screen.blit(font.render("Reset Highscore", True, BLACK), (reset_button.x+10, reset_button.y+10))
        pygame.draw.rect(screen, GREEN, start_button)
        screen.blit(font.render("Start", True, BLACK), (start_button.x+30, start_button.y+10))
        instr = font.render("Click slot, reset if needed, then start!", True, WHITE)
        screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT - 50))
    elif 'game_state' in locals() and game_state == 'playing':
        draw_game()

    # Draw betting input box if active
    if 'bet_input_active' in locals() and bet_input_active:
        input_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 80, 100, 40)
        pygame.draw.rect(screen, LIGHT_BLUE, input_rect)
        txt_surface = font.render(bet_input_text, True, BLACK)
        screen.blit(txt_surface, (input_rect.x+5, input_rect.y+5))
        prompt = font.render("Enter Bet:", True, WHITE)
        screen.blit(prompt, (input_rect.x - 100, input_rect.y + 10))
    pygame.display.flip()
    clock.tick(60)