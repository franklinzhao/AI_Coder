import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set title of the game window
pygame.display.set_caption("Snake Game")

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set the clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to draw the snake
def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 20, 20))

# Function to draw the food
def draw_food(food_pos):
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

# Function to display the score
def display_score(score):
    font = pygame.font.SysFont('Arial', 25)
    score_surface = font.render(f"Score: {score}", True, white)
    screen.blit(score_surface, (10, 10))

# Function to generate new food position
def generate_food(snake_body):
    while True:
        food_pos = (random.randint(0, screen_width - 20) // 20 * 20, random.randint(0, screen_height - 20) // 20 * 20)
        if food_pos not in snake_body:
            return food_pos

def main():
    try:
        # Initialize snake and food positions
        snake_body = [(200, 200), (220, 200), (240, 200)]
        snake_head = snake_body[0]
        snake_direction = 'right'
        score = 0
        stopped = False
        food_pos = generate_food(snake_body)
        
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake_direction != 'right':
                        snake_direction = 'left'
                    elif event.key == pygame.K_RIGHT and snake_direction != 'left':
                        snake_direction = 'right'
                    elif event.key == pygame.K_UP and snake_direction != 'down':
                        snake_direction = 'up'
                    elif event.key == pygame.K_DOWN and snake_direction != 'up':
                        snake_direction = 'down'
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_s:
                        stopped = not stopped

            if not stopped:
                if snake_direction == 'left':
                    snake_head = (snake_head[0] - 20, snake_head[1])
                elif snake_direction == 'right':
                    snake_head = (snake_head[0] + 20, snake_head[1])
                elif snake_direction == 'up':
                    snake_head = (snake_head[0], snake_head[1] - 20)
                elif snake_direction == 'down':
                    snake_head = (snake_head[0], snake_head[1] + 20)

                # Check for collisions with walls or itself
                if snake_head[0] < 0 or snake_head[0] >= screen_width or snake_head[1] < 0 or snake_head[1] >= screen_height or snake_head in snake_body:
                    print(f"Game over! Final score: {score}")
                    pygame.quit()
                    sys.exit()

                snake_body.insert(0, snake_head)

                # Check if the snake has eaten the food
                if snake_head == food_pos:
                    score += 1
                    food_pos = generate_food(snake_body)
                else:
                    snake_body.pop()

            # Draw everything
            screen.fill(black)
            draw_snake(snake_body)
            draw_food(food_pos)
            display_score(score)
            pygame.display.update()

            # Control the speed of the snake
            clock.tick(15 + score // 5)  # Increase speed as score increases

    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()

    finally:
        # Add a delay before exiting to see any final message
        time.sleep(5)

if __name__ == "__main__":
    main()
