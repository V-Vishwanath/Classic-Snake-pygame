import pygame
import os
from objects import Snake, Food


def resize(image, width, height):
    return pygame.transform.scale(pygame.image.load(image), (width, height))


SNAKE_IMAGES = [resize(f'images/Snake/{i}', 15, 15) for i in os.listdir('images/Snake')]
FOOD_IMAGE = resize('images/food.png', 15, 15)

snake = Snake(255, 255, 500, 500, 10, SNAKE_IMAGES)
food = Food(500, 500, FOOD_IMAGE)

win = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('comicsans', 25)

i = 0
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.direction = 'up'
            elif event.key == pygame.K_s:
                snake.direction = 'down'
            elif event.key == pygame.K_a:
                snake.direction = 'left'
            elif event.key == pygame.K_d:
                snake.direction = 'right'

    if not game_over:
        win.fill((255, 255, 255))
        snake.draw(win)
        food.draw(win)
        win.blit(font.render(f'Score : {snake.len - 2}', 1, (255, 0, 0)), (0, 0))
        pygame.display.update()

        if snake.eat(food):
            food.make_food = True
            snake.len += 1

        if snake.collided():
            print('COLLIDED')
            game_over = True

    clock.tick(30)
