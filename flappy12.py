import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Set initial screen size (dynamic)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird with Buttons")
print(screen)
# Set the clock for framerate
clock = pygame.time.Clock()

# Load Images (you can replace these with actual images)
bird_img = pygame.image.load('C:/Users/manju/OneDrive/Desktop/python3/bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 50))

bg_img = pygame.image.load('C:/Users/manju/OneDrive/Desktop/python3/bg.png') 
bg_img= pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_img = pygame.image.load('C:/Users/manju/OneDrive/Desktop/python3/pipe2.png')

# Button properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 60
BUTTON_FONT = pygame.font.SysFont(None, 40)



# Button rendering function
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    global bg_img
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    text_surface = BUTTON_FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=((x + (width // 2)), (y + (height // 2))))
    screen.blit(text_surface, text_rect)
    bg_img= pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Button actions
def start_game():
    game_loop()  # Start the actual game loop when Start is pressed

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'p' to unpause
                    paused = False

        screen.blit(bg_img, (0, 0))

        font = pygame.font.SysFont(None, 75)
        pause_text = font.render("Game Paused", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        pygame.display.flip()
        clock.tick(5)  # Slow down the frame rate while paused

def exit_game():
    pygame.quit()
    sys.exit()

# Game loop function
def game_loop():
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT,bg_img,pipe_img
    # Bird variables
    bird_x = 50
    bird_y = SCREEN_HEIGHT // 2
    bird_y_change = 0
    gravity = 0.5
    jump = -10

    # Pipe variables
    pipe_width = 50
    pipe_gap = 150
    pipe_speed = 4
    pipe_x = SCREEN_WIDTH
    pipe_height = random.randint(150, 450)
    pipe_img= pygame.transform.scale(pipe_img, (50, SCREEN_HEIGHT))
    score = 0
    running = True
    while running:
        screen.blit(bg_img, (0, 0))  # Draw the background image

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = jump
                if event.key == pygame.K_p:  # Press 'p' to pause the game
                    pause_game()

        # Bird movement
        bird_y_change += gravity
        bird_y += bird_y_change

        # Draw the bird
        screen.blit(bird_img, (bird_x, bird_y))
        bg_img= pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Pipe movement and drawing
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = SCREEN_WIDTH
            pipe_height = random.randint(150, 450)
            score += 1

        # Draw pipes (two parts: top and bottom)
        screen.blit(pipe_img, (pipe_x, pipe_height+pipe_gap+50))  # Bottom pipe
        top_pipe = pygame.transform.flip(pipe_img, False, True)  # Flip the image for the top pipe
        screen.blit(top_pipe, (pipe_x, pipe_height - pipe_img.get_height()))  # Top pipe

        # Check for collisions
        if bird_y < 0 or bird_y > SCREEN_HEIGHT:
            running = False

        if (pipe_x <= bird_x + bird_img.get_width() or pipe_x+pipe_img.get_width() <= bird_x) and (
            bird_y < pipe_height or bird_y > pipe_height + pipe_gap):
            running = False

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Framerate
        clock.tick(60)

    main_menu()  # Return to the main menu after the game ends

# Main menu loop
def main_menu():
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT,bg_img
    running = True
    while running:
        screen.blit(bg_img, (0, 0))

        # Get the current screen size
        current_width, current_height = pygame.display.get_surface().get_size()

        # Draw buttons with dynamic positioning based on the current window size
        draw_button("Start", current_width // 2 - BUTTON_WIDTH // 2, current_height // 2 - 150,
                    BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, WHITE, start_game)
        draw_button("Pause", current_width // 2 - BUTTON_WIDTH // 2, current_height // 2 - 50,
                    BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, WHITE, pause_game)
        draw_button("Exit", current_width // 2 - BUTTON_WIDTH // 2, current_height // 2 + 50,
                    BUTTON_WIDTH, BUTTON_HEIGHT, DARK_GRAY, WHITE, exit_game)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                # Dynamically adjust screen size if window is resized
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Start the main menu
main_menu()
