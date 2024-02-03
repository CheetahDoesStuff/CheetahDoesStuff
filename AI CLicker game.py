import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Game variables
score = 0
click_value = 1

# Function to generate a random position for the circle
def random_circle_position():
    radius = 30
    x = random.randint(radius, WIDTH - radius)
    y = random.randint(radius, HEIGHT - radius)
    return x, y

# Create the game window
screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))
pygame.display.set_caption("Clicker Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
upgrade_font = pygame.font.Font(None, 24)
credits_font = pygame.font.Font(None, 20)

# Upgrades information
num_upgrades = 50
upgrade_prices = [random.randint(1, 30) for _ in range(num_upgrades)]
upgrade_values = [random.randint(1, 20) for _ in range(num_upgrades)]
upgrades = [f"Upgrade {i+1}" for i in range(num_upgrades)]

# Upgrade buttons
upgrade_buttons = []

scroll_y = 0
scroll_speed = 10

for i, upgrade in enumerate(upgrades):
    button_rect = pygame.Rect(WIDTH + 50, 50 + i * 60, 200, 50)
    upgrade_buttons.append(button_rect)

# Load the image
try:
    pog_image = pygame.image.load("pog.jpg")
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit()

pog_rect = pog_image.get_rect()
pog_rect.center = (WIDTH // 2, HEIGHT // 2)

# Load the sounds
try:
    pygame.mixer.init()
    bob_sound = pygame.mixer.Sound("bob.mp3")
    discord_notification_sound = pygame.mixer.Sound("discord-notification.mp3")
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    sys.exit()

bob_sound.set_volume(0.5)  # Adjust the volume if needed
discord_notification_sound.set_volume(0.5)  # Adjust the volume if needed

bob_sound.play(-1)  # Play the bob sound in a loop
discord_notification_sound.play(-1)  # Play the discord-notification sound in a loop

def random_bright_color():
    return random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)

def render_credits():
    credits_text = credits_font.render("Credits: Bravest_Cheetah & ChatGPT", True, (255, 255, 255))
    screen.blit(credits_text, (10, HEIGHT - 30))

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos

                # Check if the click is on the image
                if pog_rect.collidepoint(mouse_x, mouse_y):
                    score += click_value
                    discord_notification_sound.play()

                # Check if the click is on an upgrade button
                for i, button_rect in enumerate(upgrade_buttons):
                    if button_rect.collidepoint(mouse_x, mouse_y) and score >= upgrade_prices[i]:
                        score -= upgrade_prices[i]
                        click_value += upgrade_values[i]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Move Up
                scroll_y += scroll_speed
            elif event.key == pygame.K_DOWN:  # Move Down
                scroll_y -= scroll_speed

    # Update
    screen.fill(random_bright_color())

    # Draw game screen
    score_text = font.render(f"Score: {score}", True, random_bright_color())
    screen.blit(score_text, (10, 10))

    # Draw upgrades information on the sidebar with arrow key navigation
    for i, button_rect in enumerate(upgrade_buttons):
        button_rect.y += scroll_y
        pygame.draw.rect(screen, random_bright_color(), button_rect)
        upgrade_text = upgrade_font.render(f"{upgrades[i]} (+{upgrade_values[i]})", True, (0, 0, 0))
        screen.blit(upgrade_text, (button_rect.x + 10, button_rect.y + 10))
        price_text = upgrade_font.render(f"Price: {upgrade_prices[i]}", True, (0, 0, 0))
        screen.blit(price_text, (button_rect.x + 10, button_rect.y + 30))

    # Draw the image
    screen.blit(pog_image, pog_rect)

    # Draw credits
    render_credits()

    # Refresh display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
