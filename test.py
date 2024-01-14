import pygame

def print_joystick_positions():
    # Initialize Pygame
    pygame.init()

    # Check for connected joysticks
    if pygame.joystick.get_count() == 0:
        print("No joystick found.")
        return

    # Initialize the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    try:
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            # Print joystick positions
            axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
            print("Joystick Axes:", axes)

            # Add a small delay to avoid printing too frequently
            pygame.time.delay(100)

    finally:
        # Clean up
        pygame.quit()

if __name__ == "__main__":
    print_joystick_positions()
