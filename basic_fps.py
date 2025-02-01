import pygame
import sys
import math

# ------------------------------
# Configuration & Map Setup
# ------------------------------

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2

# Field of view and raycasting parameters
FOV = math.pi / 3          # 60� field of view
NUM_RAYS = 320             # Number of rays (each ray draws a vertical slice)
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 800            # Maximum depth (how far a ray can go)

# Size of a single map block (in "world" pixels)
TILE_SIZE = 64

# Distance from the player to the projection plane
PROJ_PLANE_DIST = (SCREEN_WIDTH / 2) / math.tan(FOV / 2)

# Define a very simple map.
# '1' represents a wall; '.' represents empty space.
GAME_MAP = [
    "111111111111",
    "1..........1",
    "1...11.....1",
    "1..........1",
    "1.....11...1",
    "1..........1",
    "111111111111",
]
MAP_WIDTH = len(GAME_MAP[0])
MAP_HEIGHT = len(GAME_MAP)

# ------------------------------
# Player Setup
# ------------------------------

# Start the player at 1.5 tiles from the top-left corner (in world pixels)
player_x = TILE_SIZE * 1.5
player_y = TILE_SIZE * 1.5
player_angle = 0

# Movement and rotation speeds
MOVE_SPEED = 2.0      # pixels per frame
ROT_SPEED = 0.03      # radians per frame

# ------------------------------
# Helper Functions
# ------------------------------

def is_wall(map_x, map_y):
    """Return True if the given map cell is a wall."""
    if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
        return True
    return GAME_MAP[map_y][map_x] == '1'

# ------------------------------
# Main Game Loop (Raycasting Engine)
# ------------------------------

def main():
    global player_x, player_y, player_angle

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Basic FPS Raycaster")
    clock = pygame.time.Clock()

    running = True
    while running:
        # Process input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Handle Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= ROT_SPEED
        if keys[pygame.K_RIGHT]:
            player_angle += ROT_SPEED
        if keys[pygame.K_UP]:
            # Move forward
            new_x = player_x + math.cos(player_angle) * MOVE_SPEED
            new_y = player_y + math.sin(player_angle) * MOVE_SPEED
            # Simple collision detection: Check map cell (convert world to map coordinates)
            if not is_wall(int(new_x // TILE_SIZE), int(new_y // TILE_SIZE)):
                player_x = new_x
                player_y = new_y
        if keys[pygame.K_DOWN]:
            # Move backward
            new_x = player_x - math.cos(player_angle) * MOVE_SPEED
            new_y = player_y - math.sin(player_angle) * MOVE_SPEED
            if not is_wall(int(new_x // TILE_SIZE), int(new_y // TILE_SIZE)):
                player_x = new_x
                player_y = new_y

        # ------------------------------
        # Rendering: Draw Floor/Ceiling and Walls via Raycasting
        # ------------------------------

        # Clear screen: fill with black (background)
        screen.fill((0, 0, 0))

        # Draw ceiling and floor
        pygame.draw.rect(screen, (100, 100, 100), (0, 0, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))  # Ceiling (light gray)
        pygame.draw.rect(screen, (50, 50, 50), (0, HALF_SCREEN_HEIGHT, SCREEN_WIDTH, HALF_SCREEN_HEIGHT))  # Floor (darker gray)

        # Start raycasting: from the left-most ray to the right-most
        ray_angle = player_angle - (FOV / 2)
        for ray in range(NUM_RAYS):
            # For each ray, step forward until a wall is hit or MAX_DEPTH is reached
            for depth in range(1, MAX_DEPTH):
                # Calculate the ray?s target point (in world coordinates)
                target_x = player_x + depth * math.cos(ray_angle)
                target_y = player_y + depth * math.sin(ray_angle)

                # Convert world coordinates to map grid coordinates
                map_x = int(target_x // TILE_SIZE)
                map_y = int(target_y // TILE_SIZE)

                # If out of bounds, treat it as a wall
                if map_x < 0 or map_x >= MAP_WIDTH or map_y < 0 or map_y >= MAP_HEIGHT:
                    break

                # If a wall is hit, render a vertical slice for this ray
                if GAME_MAP[map_y][map_x] == '1':
                    # Correct the fish-eye effect by adjusting the distance
                    depth *= math.cos(player_angle - ray_angle)
                    # Avoid division by zero
                    if depth == 0:
                        depth = 1
                    # Calculate the projected wall slice height
                    wall_height = int((TILE_SIZE / depth) * PROJ_PLANE_DIST)
                    # Create a simple shading effect based on distance
                    shade = 255 / (1 + depth * depth * 0.0001)
                    color = (shade, shade, shade)
                    # Determine horizontal position of this vertical slice
                    slice_width = SCREEN_WIDTH / NUM_RAYS
                    ray_screen_x = int(ray * slice_width)
                    # Draw the vertical slice (as a thin rectangle)
                    pygame.draw.rect(
                        screen, color,
                        (ray_screen_x, HALF_SCREEN_HEIGHT - wall_height // 2, int(slice_width) + 1, wall_height)
                    )
                    break

            # Increment the ray's angle for the next iteration
            ray_angle += DELTA_ANGLE

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
