import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
SKY_COLOR = (135, 206, 235)
GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 69, 19)
STONE_COLOR = (128, 128, 128)
PLAYER_COLOR = (255, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Minecraft Clone")
clock = pygame.time.Clock()

# World Generation (Simple 2D grid)
# 0 = Sky, 1 = Grass, 2 = Dirt, 3 = Stone
world = []
for y in range(GRID_HEIGHT):
    row = []
    for x in range(GRID_WIDTH):
        if y < GRID_HEIGHT // 2:
            row.append(0)  # Sky
        elif y == GRID_HEIGHT // 2:
            row.append(1)  # Grass
        elif y < GRID_HEIGHT - 5:
            row.append(2)  # Dirt
        else:
            row.append(3)  # Stone
    world.append(row)

# Player Setup
player_x = SCREEN_WIDTH // 2
player_y = (GRID_HEIGHT // 2 - 1) * BLOCK_SIZE
player_width = 30
player_height = 40
player_speed = 5
is_jumping = False
jump_count = 10

# Selected Block
selected_block = 2  # Default: Dirt

# Main Loop
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            # Block switching
            if event.key == pygame.K_1:
                selected_block = 1  # Grass
            elif event.key == pygame.K_2:
                selected_block = 2  # Dirt
            elif event.key == pygame.K_3:
                selected_block = 3  # Stone
                
            # Jump
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            grid_x = pos[0] // BLOCK_SIZE
            grid_y = pos[1] // BLOCK_SIZE
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                # Left-click to break block
                if event.button == 1:
                    world[grid_y][grid_x] = 0
                # Right-click to place block
                elif event.button == 3:
                    world[grid_y][grid_x] = selected_block

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Simple Jump Logic
    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Drawing and rendering
    screen.fill(SKY_COLOR)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            block_type = world[y][x]
            color = None
            
            if block_type == 1:
                color = GRASS_COLOR
            elif block_type == 2:
                color = DIRT_COLOR
            elif block_type == 3:
                color = STONE_COLOR
                
            if color:
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    # Draw Player
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
