import pygame
import random
import sys
import os
import subprocess

# Activate the virtual environment
venv_activate = os.path.join("venv", "Scripts", "activate")
subprocess.call(venv_activate, shell=True)

# Launch the game script
subprocess.call("python game.py", shell=True)


# Initialize Pygame
pygame.init()

velocity = 5

# Set up the display window
width, height = 300, 300
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Snake and food
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
food_spawn = True

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
direction = RIGHT

clock = pygame.time.Clock()

# Function to draw the snake
def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(window, white, pygame.Rect(pos[0], pos[1], 10, 10))

# Function for the game over animation
def game_over_animation():
    font = pygame.font.SysFont(None, 25)
    for i in range(255, 0, -1):
        window.fill((i, 0, 0))
        text = font.render("Game Over!", True, (255, i, i))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        text1 = font.render("Press Space to exit...", True, (255, i, i))
        text1_rect = text1.get_rect(center=(width // 2, (height // 2) + 50))
        window.blit(text1, text1_rect)
        text2 = font.render("or Enter to restart...", True, (255, i, i))
        text2_rect = text2.get_rect(center=(width // 2, (height // 2) + 100))
        window.blit(text2, text2_rect)
        pygame.display.flip()
        pygame.time.delay(10)

# Function for the menu
def menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    running = False
                elif event.key == pygame.K_1:
                    run_game()

# Main game function
def run_game():
    global direction, food_pos, food_spawn, snake_body, velocity
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    running = False
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # Reset variables for a new game
                    direction = RIGHT
                    velocity = 3 
                    snake_body = [[100, 50], [90, 50], [80, 50]]
                    food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
                    food_spawn = True
                    game_over = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != RIGHT:
            direction = LEFT
        elif keys[pygame.K_RIGHT] and direction != LEFT:
            direction = RIGHT
        elif keys[pygame.K_UP] and direction != DOWN:
            direction = UP
        elif keys[pygame.K_DOWN] and direction != UP:
            direction = DOWN

        if direction == UP:
            snake_pos = [snake_body[0][0], snake_body[0][1] - 10]
        elif direction == DOWN:
            snake_pos = [snake_body[0][0], snake_body[0][1] + 10]
        elif direction == RIGHT:
            snake_pos = [snake_body[0][0] + 10, snake_body[0][1]]
        elif direction == LEFT:
            snake_pos = [snake_body[0][0] - 10, snake_body[0][1]]

        snake_body.insert(0, list(snake_pos))

        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            food_spawn = False
            velocity += 0.5
            food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10, random.randrange(1, (height // 10)) * 10]
            food_spawn = True

        window.fill(blue)
        draw_snake(snake_body)
        pygame.draw.rect(window, green, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
            game_over_animation()
            game_over = True

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over_animation()
                game_over = True

        pygame.display.flip()
        clock.tick(velocity)

run_game()
