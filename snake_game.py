import pygame
import random
import os

# Constants
display_width = 640
display_height = 480
grid_size = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
font = pygame.font.SysFont('arial', 24)
clock = pygame.time.Clock()

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Geli\u015fmi\u015f Y\u0131lan Oyunu')

highscore_file = 'highscore.txt'


def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, 'r') as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0


def save_highscore(score):
    with open(highscore_file, 'w') as f:
        f.write(str(score))


def draw_text(surface, text, color, x, y):
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.topleft = (x, y)
    surface.blit(img, rect)


class Snake:
    def __init__(self):
        self.positions = [(display_width // 2, display_height // 2)]
        self.direction = random.choice([(grid_size, 0), (-grid_size, 0), (0, grid_size), (0, -grid_size)])
        self.grow = False

    def move(self):
        cur = self.positions[0]
        x, y = cur
        dx, dy = self.direction
        new_pos = ((x + dx) % display_width, (y + dy) % display_height)
        if new_pos in self.positions or new_pos in obstacles:
            return False
        self.positions = [new_pos] + self.positions
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def change_direction(self, dir):
        opposite = (-self.direction[0], -self.direction[1])
        if dir != opposite:
            self.direction = dir

    def eat(self):
        self.grow = True

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], grid_size, grid_size)
            pygame.draw.rect(surface, GREEN, rect)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        while True:
            x = random.randrange(0, display_width, grid_size)
            y = random.randrange(0, display_height, grid_size)
            if (x, y) not in snake.positions and (x, y) not in obstacles:
                self.position = (x, y)
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], grid_size, grid_size)
        pygame.draw.rect(surface, RED, rect)


def create_obstacles(num):
    obs = []
    for _ in range(num):
        while True:
            x = random.randrange(0, display_width, grid_size)
            y = random.randrange(0, display_height, grid_size)
            if (x, y) not in snake.positions and (x, y) not in obs:
                obs.append((x, y))
                break
    return obs


def draw_obstacles(surface):
    for pos in obstacles:
        rect = pygame.Rect(pos[0], pos[1], grid_size, grid_size)
        pygame.draw.rect(surface, BLUE, rect)


def main():
    global snake, food, obstacles
    snake = Snake()
    food = Food()
    obstacles = create_obstacles(10)
    score = 0
    highscore = load_highscore()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -grid_size))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, grid_size))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-grid_size, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((grid_size, 0))
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_r and not running:
                    main()
                    return

        if not paused:
            if not snake.move():
                running = False

            if snake.positions[0] == food.position:
                snake.eat()
                food.randomize_position()
                score += 1
                if score > highscore:
                    highscore = score
                if score % 5 == 0:
                    obstacles += create_obstacles(3)

        display.fill(BLACK)
        draw_obstacles(display)
        snake.draw(display)
        food.draw(display)
        draw_text(display, f'Score: {score}  High Score: {highscore}', WHITE, 10, 10)
        if paused:
            draw_text(display, 'Pause', WHITE, display_width // 2 - 40, display_height // 2)
        pygame.display.update()
        clock.tick(10 + score // 5)

    save_highscore(highscore)
    game_over(highscore)


def game_over(highscore):
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                elif event.key == pygame.K_q:
                    over = False
        display.fill(BLACK)
        draw_text(display, 'Oyun Bitti - R: Yeniden, Q: Cik', WHITE, display_width // 2 - 140, display_height // 2)
        draw_text(display, f'En Yüksek Skor: {highscore}', WHITE, display_width // 2 - 100, display_height // 2 + 40)
        pygame.display.update()
        clock.tick(5)
    pygame.quit()


if __name__ == '__main__':
    main()
