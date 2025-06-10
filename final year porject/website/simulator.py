import pygame
import sys
import time
import math
import os 

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLUE = (0, 0, 255)

# Create Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Speedometer Simulator")

# Load Background Image
background_image = pygame.image.load("C:/Users/prath/Desktop/website/images.jpg")  # Replace with your background image path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load Sound Effect
decrease_sound = pygame.mixer.Sound("C:/Users/prath/Desktop/website/civil-defense-siren-128262.mp3")

# Fonts
font = pygame.font.Font(None, 36)  # Smaller font for speedometer
large_font = pygame.font.Font(None, 74)

# Speed Variables
speed = 0
max_speed = 125
running = True
exit_timer_start = None  # Timer for exiting
start_time = time.time()

# Clock for FPS
clock = pygame.time.Clock()


# Path to the text file for key press signal
file_path = "simulator_command.txt"

# Draw Small Speedometer in Bottom-Right Corner
def draw_small_speedometer(current_speed):
    center_x, center_y = WIDTH - 100, HEIGHT - 200  # Bottom-right corner
    radius = 80

    # Draw Outer Circle
    pygame.draw.circle(screen, GRAY, (center_x, center_y), radius + 5)
    pygame.draw.circle(screen, BLACK, (center_x, center_y), radius)

    # Draw Speed Ticks
    for angle in range(-60, 241, 30):  # Tick angles
        start_x = center_x + (radius - 10) * math.cos(math.radians(angle))
        start_y = center_y + (radius - 10) * math.sin(math.radians(angle))
        end_x = center_x + radius * math.cos(math.radians(angle))
        end_y = center_y + radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 2)

    # Draw Needle
    needle_angle = -60 + (240 * current_speed / max_speed)  # Map speed to needle angle
    needle_x = center_x + (radius - 20) * math.cos(math.radians(needle_angle))
    needle_y = center_y + (radius - 20) * math.sin(math.radians(needle_angle))
    pygame.draw.line(screen, RED, (center_x, center_y), (needle_x, needle_y), 3)

    # Draw Speed Text Inside the Speedometer
    speed_text = font.render(f"{current_speed} km/h", True, BLUE)
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2, center_y - speed_text.get_height() // 2))

# Draw Full Background and Main Speed Text
def draw_screen(current_speed):
    # Display Background
    screen.blit(background_image, (0, 0))

    # Draw Main Speed Text at Center
    main_speed_text = large_font.render(f"Speed: {current_speed} km/h", True, WHITE)
    screen.blit(main_speed_text, (WIDTH // 2 - main_speed_text.get_width() // 2, HEIGHT // 2 - 50))

    # Draw Small Speedometer
    draw_small_speedometer(current_speed)

    pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get Pressed Keys
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and speed < max_speed:
        speed += 1
        time.sleep(0.1)

    if keys[pygame.K_DOWN] and speed > 0:
        speed -= 1
        time.sleep(0.1)
    
    # if keys[pygame.K_x]:
    #     if exit_timer_start is None:  # Start the timer when "X" is pressed
    #         exit_timer_start = time.time()

    #     # Gradually reduce speed to 20 km/h over 10 seconds
    #     total_time = 10  # seconds
    #     fps = 30  # Frames per second
    #     decrement_step = (speed - 20) / (total_time * fps)

    #     for _ in range(int(total_time * fps)):
    #         if speed > 20:
    #             speed -= decrement_step
    #             speed = max(speed, 20)  # Ensure it doesn't go below 20
    #             pygame.mixer.Sound.play(decrease_sound)
    #             draw_screen(int(speed))
    #             time.sleep(1 / fps)

    #     if speed <= 20:
    #         pygame.mixer.Sound.play(decrease_sound)
    #         max_speed = 20

    # # Check if the timer has reached 30 seconds
    # if exit_timer_start is not None:
    #     elapsed_time = time.time() - exit_timer_start
    #     if elapsed_time >= 30:
    #         running = False  # Exit the program

    # # Disable UP button if Speed > 20
    # if speed > 20 and keys[pygame.K_UP]:
    #     pass  # Do nothing (effectively disables the UP key)
    
    
    # Check if "X" command is written in the text file

    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            command = file.read().strip()
            if command == "X":
                # Execute the X key sequence
                print("Simulating 'X' key press")
                if exit_timer_start is None:  # Start the timer when "X" is pressed
                    exit_timer_start = time.time()
                # Gradually reduce speed to 20 km/h over 10 seconds
                total_time = 10  # seconds
                fps = 30  # Frames per second
                decrement_step = (speed - 20) / (total_time * fps)

                for _ in range(int(total_time * fps)):
                    if speed > 20:
                        speed -= decrement_step
                        speed = max(speed, 20)  # Ensure it doesn't go below 20
                        pygame.mixer.Sound.play(decrease_sound)
                        draw_screen(int(speed))
                        time.sleep(1 / fps)

                if speed <20:
                    pygame.mixer.Sound.play(decrease_sound)
                max_speed = 20

                # Clear the command after processing
                with open(file_path, "w") as file:
                    file.write("")
    # Check if the timer has reached 30 seconds
    if exit_timer_start is not None:
        elapsed_time = time.time() - exit_timer_start
        if elapsed_time >= 30:
            running = False  # Exit the program

    # Disable UP button if Speed > 20
    if speed > 20 and keys[pygame.K_UP]:
        pass  # Do nothing (effectively disables the UP key)

    # Draw the Screen with Speedometer
    draw_screen(int(speed))

    # Limit FPS
    clock.tick(30)

pygame.quit()
sys.exit()
