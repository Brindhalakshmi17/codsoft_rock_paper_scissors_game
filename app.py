import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Larger window size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT = pygame.font.SysFont('arial', 32)

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rock-Paper-Scissors Game')

# Load images for Rock, Paper, and Scissors
rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissors.png')

# Resize images
rock_img = pygame.transform.scale(rock_img, (120, 120))
paper_img = pygame.transform.scale(paper_img, (120, 120))
scissors_img = pygame.transform.scale(scissors_img, (120, 120))

# Button positions (using images instead of rectangles now)
rock_rect = rock_img.get_rect(topleft=(100, 150))
paper_rect = paper_img.get_rect(topleft=(300, 150))
scissors_rect = scissors_img.get_rect(topleft=(500, 150))

# Game logic
choices = ['rock', 'paper', 'scissors']
user_score, computer_score = 0, 0
rounds_limit = 10  # Set the number of rounds
current_round = 1

# Button for the next round
next_round_btn = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

def get_computer_choice():
    """Simulate computer 'thinking' before making a choice."""
    time.sleep(0.5)  # Adds a delay to simulate randomness
    return random.choice(choices)

def determine_winner(user_choice, computer_choice):
    global user_score, computer_score
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'scissors' and computer_choice == 'paper') or \
         (user_choice == 'paper' and computer_choice == 'rock'):
        user_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "Computer wins!"

def draw_text(text, font, color, x, y):
    """Helper function to draw text on the screen."""
    surface = font.render(text, True, color)
    window.blit(surface, (x, y))

def game():
    """Main game loop."""
    run = True
    clock = pygame.time.Clock()
    user_choice = None
    computer_choice = None
    result = None
    show_result = False
    result_time = 0  # Store when the result should be displayed
    waiting_for_next_round = False

    global current_round

    while run and current_round <= rounds_limit:
        window.fill(WHITE)

        # Display the current round and round limit
        draw_text(f"Round {current_round} / {rounds_limit}", FONT, BLACK, WIDTH // 2 - 100, 20)

        # Display user and computer choices after round completion
        if user_choice and computer_choice:
            draw_text(f"Your Choice: {user_choice.capitalize()}", FONT, BLACK, 50, 50)
            draw_text(f"Computer Choice: {computer_choice.capitalize()}", FONT, BLACK, 350, 50)

        # Display the result of the round after it's determined
        if show_result:
            draw_text(f"Result: {result}", FONT, BLACK, WIDTH // 2 - 150, 100)

        # Display scores (only after result is shown)
        draw_text(f"Your Score: {user_score}", FONT, BLACK, 50, 20)
        draw_text(f"Computer Score: {computer_score}", FONT, BLACK, 550, 20)

        # Mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()

        # Check hover for rock image
        if rock_rect.collidepoint(mouse_pos):
            scaled_rock_img = pygame.transform.scale(rock_img, (130, 130))
            window.blit(scaled_rock_img, (95, 145))
        else:
            window.blit(rock_img, rock_rect.topleft)

        # Check hover for paper image
        if paper_rect.collidepoint(mouse_pos):
            scaled_paper_img = pygame.transform.scale(paper_img, (130, 130))
            window.blit(scaled_paper_img, (295, 145))
        else:
            window.blit(paper_img, paper_rect.topleft)

        # Check hover for scissors image
        if scissors_rect.collidepoint(mouse_pos):
            scaled_scissors_img = pygame.transform.scale(scissors_img, (130, 130))
            window.blit(scaled_scissors_img, (495, 145))
        else:
            window.blit(scissors_img, scissors_rect.topleft)

        # If result is shown, display the "Next Round" button
        if show_result:
            pygame.draw.rect(window, RED, next_round_btn)
            draw_text("Next Round", FONT, WHITE, next_round_btn.x + 30, next_round_btn.y + 10)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not show_result:
                if rock_rect.collidepoint(event.pos):
                    user_choice = 'rock'
                elif paper_rect.collidepoint(event.pos):
                    user_choice = 'paper'
                elif scissors_rect.collidepoint(event.pos):
                    user_choice = 'scissors'

                if user_choice:
                    computer_choice = get_computer_choice()  # Add randomness with slight delay
                    result = determine_winner(user_choice, computer_choice)
                    show_result = True  # After this round, show result
                    result_time = pygame.time.get_ticks()  # Record the time when result is shown

            # Handling the next round button click
            if event.type == pygame.MOUSEBUTTONDOWN and show_result:
                if next_round_btn.collidepoint(event.pos):
                    show_result = False  # Reset for next round
                    user_choice = None
                    computer_choice = None
                    result = None
                    current_round += 1

        pygame.display.update()
        clock.tick(30)

    # Display game over message
    window.fill(WHITE)
    draw_text(f"Game Over! Final Score: You {user_score} - {computer_score} Computer", FONT, BLACK, 100, 250)
    pygame.display.update()
    time.sleep(3)  # Wait for 3 seconds before closing
    pygame.quit()

if __name__ == '__main__':
    game()
