# Example file showing a basic pygame "game loop"
try:
    import sys
    import pygame
except ImportError as err:
    print(f"modules missing: {err}")
    sys.exit(2)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
bg_color = (0, 50, 50)
grid_color = pygame.Color("#000000")
cell_size = 10
cell_thickness = 1
cell_color = pygame.Color("#b0e5d7")

x_iterator = range(0, pygame.display.get_window_size()[0], cell_size)
y_iterator = range(0, pygame.display.get_window_size()[1], cell_size)
grid_data = [[False for y in y_iterator] for x in x_iterator]
simulating = False


def draw_grid():
    for x_location in x_iterator:
        for y_location in y_iterator:
            pygame.draw.rect(
                screen,
                grid_color,
                pygame.Rect(x_location, y_location, cell_size, cell_size),
                cell_thickness,
            )


def draw_cell(x, y):
    pygame.draw.rect(
        screen,
        cell_color,
        pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size),
    )


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                simulating = not simulating

            elif not simulating and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                grid_data[mouse_pos[0] // cell_size][
                    mouse_pos[1] // cell_size
                ] = not grid_data[mouse_pos[0] // cell_size][mouse_pos[1] // cell_size]

    if simulating:
        next_grid_data = [i.copy() for i in grid_data]
        for x in range(len(grid_data)):
            for y in range(len(grid_data[0])):
                neighbor_count = 0
                if grid_data[x][y]:
                    for n_x in range(-1, 2):
                        for n_y in range(-1, 2):
                            if n_x != 0 or n_y != 0:
                                neighbor_count = (
                                    neighbor_count + 1
                                    if grid_data[(x + n_x) % len(grid_data)][
                                        (y + n_y) % len(grid_data[0])
                                    ]
                                    else neighbor_count
                                )
                    if neighbor_count < 2 or neighbor_count > 3:
                        next_grid_data[x][y] = False
                else:
                    for n_x in range(-1, 2):
                        for n_y in range(-1, 2):
                            if n_x != 0 or n_y != 0:
                                neighbor_count = (
                                    neighbor_count + 1
                                    if grid_data[(x + n_x) % len(grid_data)][
                                        (y + n_y) % len(grid_data[0])
                                    ]
                                    else neighbor_count
                                )
                    if neighbor_count == 3:
                        next_grid_data[x][y] = True
        next_grid_data, grid_data = grid_data, next_grid_data

    # fill the screen with a color to wipe away anything from last frame
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    screen.fill(bg_color)
    draw_grid()
    for x in x_iterator:
        for y in y_iterator:
            x_item = x // cell_size
            y_item = y // cell_size
            if grid_data[x_item][y_item]:
                draw_cell(x_item, y_item)
    pygame.display.flip()

    clock.tick(15)  # limits FPS to 60

pygame.quit()
