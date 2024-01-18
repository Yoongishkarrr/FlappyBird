import pygame
import sys
import random

# Pygame initialization
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird settings
bird_x = 100
bird_y = HEIGHT // 2
bird_speed = 5
gravity = 1
jump_force = 15

# Pipes settings
pipe_width = 50
pipe_height = 300
pipe_distance = 200
pipes = []

# Clock to control the frame rate
clock = pygame.time.Clock()

# Results storage
results = []

def draw_bird(x, y):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 20)

def draw_pipe(x, height):
    pygame.draw.rect(screen, (0, 128, 0), (x, 0, pipe_width, height))
    pygame.draw.rect(screen, (0, 128, 0), (x, height + pipe_distance, pipe_width, HEIGHT - height - pipe_distance))

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Player wants to play again
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

def get_player_name():
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        width = max(200, font.size(text)[0]+10)
        input_box.w = width
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

def show_results():
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    y = 50
    for result in results:
        text = f"{result['name']}: {result['score']} points"
        result_text = font.render(text, True, (0, 0, 0))
        screen.blit(result_text, (WIDTH // 2 - 100, y))
        y += 40
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def draw_menu(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    text_start = font.render("1 - New Game", True, (0, 0, 0))
    text_results = font.render("2 - Results", True, (0, 0, 0))
    text_exit = font.render("3 - Exit", True, (0, 0, 0))
    screen.blit(text_start, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
    screen.blit(text_results, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(text_exit, (WIDTH // 2 - 100, HEIGHT // 2 + 60))
    pygame.display.flip()

def main_menu():
    draw_menu(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # New game
                    player_name = get_player_name()
                    bird_y = HEIGHT // 2
                    bird_speed = 0
                    pipes = []
                    score = 0
                    game_running = True  # Флаг для контроля состояния новой игры
                    while game_running:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                game_running = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    bird_speed = -jump_force
                        bird_speed += gravity
                        bird_y += bird_speed

                        if len(pipes) == 0 or pipes[-1][0] < WIDTH - pipe_distance:
                            pipe_height = random.randint(100, HEIGHT - 200)
                            pipes.append([WIDTH, pipe_height])

                        for pipe in pipes:
                            pipe[0] -= 5

                        for pipe in pipes:
                            if bird_x + 20 > pipe[0] and bird_x - 20 < pipe[0] + pipe_width:
                                if bird_y - 20 < pipe[1] or bird_y + 20 > pipe[1] + pipe_distance:
                                    results.append({'name': player_name, 'score': score})
                                    if game_over():
                                        game_running = False
                                        break

                        pipes = [pipe for pipe in pipes if pipe[0] > 0]

                        screen.fill((255, 255, 255))
                        draw_bird(bird_x, bird_y)
                        for pipe in pipes:
                            draw_pipe(pipe[0], pipe[1])

                        pygame.display.flip()
                        clock.tick(30)
                        score += 1
                elif event.key == pygame.K_2:
                    # Show results
                    show_results()
                elif event.key == pygame.K_3:
                    # Exit
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
