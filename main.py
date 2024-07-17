import pygame
import sys
import random

def init_pygame():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("HackerHunt")
    return screen, width, height

def draw_player(screen, color, position, size):
    pygame.draw.rect(screen, color, (*position, size, size))

def draw_nodes(screen, color, nodes, size):
    for node_pos in nodes:
        pygame.draw.circle(screen, color, node_pos, size)

def detect_collision(player_pos, node_pos, player_size, node_size):
    p_x, p_y = player_pos
    n_x, n_y = node_pos
    distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
    if distance < player_size / 2 + node_size:
        return True
    return False

def move_player(player_pos, keys, speed):
    if keys[pygame.K_LEFT]:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += speed
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += speed

def main():
    screen, width, height = init_pygame()
    clock = pygame.time.Clock()

    # Define colors
    BLACK = (0, 0, 0)
    BLUE = (0, 128, 255)
    GREEN = (0, 255, 0)

    # Define player properties
    player_size = 30
    player_color = BLUE
    player_pos = [width // 2, height // 2]
    player_speed = 5

    # Define node properties
    node_size = 50
    node_color = GREEN
    nodes = [[random.randint(50, width-50), random.randint(50, height-50)] for _ in range(5)]

    # Define problems
    problems = ["P1", "P2", "P3", "P4", "P5"]
    node_problems = {tuple(node): random.choice(problems) for node in nodes}

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        move_player(player_pos, keys, player_speed)

        screen.fill(BLACK)
        draw_player(screen, player_color, player_pos, player_size)
        draw_nodes(screen, node_color, nodes, node_size)

        for node_pos in nodes[:]:
            if detect_collision(player_pos, node_pos, player_size, node_size):
                print(f"Problem solved at node: {node_problems[tuple(node_pos)]}")
                nodes.remove(node_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
