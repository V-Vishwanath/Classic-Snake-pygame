import pygame
from random import randint


class BodyPart:
    def __init__(self, x, y, direction, image):
        self.x = x
        self.y = y
        self.direction = direction
        self.image = image


class Snake:
    def __init__(self, x, y, width, height, vel, images):
        self.x = x
        self.y = y
        self.vel = vel
        self.direction = ''
        self.width = width
        self.height = height

        self.head_up = images[0]
        self.head_down = images[1]
        self.head_left = images[2]
        self.head_right = images[3]

        self.neck_up_right = images[4]
        self.neck_up_left = images[5]
        self.neck_down_right = images[6]
        self.neck_down_left = images[7]

        self.body_vertical = images[8]
        self.body_horizontal = images[9]

        self.tail_up = images[10]
        self.tail_down = images[11]
        self.tail_left = images[12]
        self.tail_right = images[13]

        self.head = self.head_right
        self.tail = self.tail_right
        self.body = [BodyPart(self.x - 15, self.y, 'right', self.tail), BodyPart(self.x, self.y, 'right', self.head)]
        self.len = 2

    def move(self):
        if self.direction == 'up':
            self.head = self.head_up
            self.y -= self.vel
        elif self.direction == 'down':
            self.head = self.head_down
            self.y += self.vel
        elif self.direction == 'left':
            self.head = self.head_left
            self.x -= self.vel
        elif self.direction == 'right':
            self.head = self.head_right
            self.x += self.vel

        if self.y < 0:
            self.y = self.height - self.vel
        elif self.x < 0:
            self.x = self.width - self.vel
        elif self.y + 15 > self.height:
            self.y = self.vel
        elif self.x + 15 > self.width:
            self.x = self.vel

        if self.direction != '':
            self.body.append(BodyPart(self.x, self.y, self.direction, self.head))
            if len(self.body) - 2 > self.len:
                self.body.pop(0)

                if self.body[0].direction == 'up':
                    self.body[0].image = self.tail_up
                elif self.body[0].direction == 'down':
                    self.body[0].image = self.tail_down
                elif self.body[0].direction == 'left':
                    self.body[0].image = self.tail_down
                elif self.body[0].direction == 'right':
                    self.body[0].image = self.tail_down

                for i in range(1, len(self.body) - 1):
                    if self.body[i].direction == 'up':
                        if self.body[i + 1].direction == 'right':
                            self.body[i].image = self.neck_up_right
                        elif self.body[i + 1].direction == 'left':
                            self.body[i].image = self.neck_up_left
                        else:
                            self.body[i].image = self.body_vertical

                    elif self.body[i].direction == 'down':
                        if self.body[i + 1].direction == 'right':
                            self.body[i].image = self.neck_down_right
                        elif self.body[i + 1].direction == 'left':
                            self.body[i].image = self.neck_down_left
                        else:
                            self.body[i].image = self.body_vertical

                    elif self.body[i].direction == 'left':
                        if self.body[i + 1].direction == 'up':
                            self.body[i].image = self.neck_down_right
                        elif self.body[i + 1].direction == 'down':
                            self.body[i + 1].image = self.neck_up_right
                        else:
                            self.body[i].image = self.body_horizontal

                    else:
                        if self.body[i + 1].direction == 'up':
                            self.body[i].image = self.neck_down_left
                        elif self.body[i + 1].direction == 'down':
                            self.body[i + 1].image = self.neck_up_left
                        else:
                            self.body[i].image = self.body_horizontal

    def eat(self, food):
        food_mask = food.get_mask()
        snake_mask = pygame.mask.from_surface(self.head)
        offset = (self.x - food.x, self.y - food.y)

        if food_mask.overlap(snake_mask, offset):
            return True
        return False

    def collided(self):
        x = self.x + 7
        y = self.y + 7

        for i in range(self.len - 1):
            if (self.body[i].x <= x <= self.body[i].x+15) and (self.body[i].y <= y <= self.body[i].y+15):
                return True
        return False

    def draw(self, win):
        self.move()
        for i in self.body:
            win.blit(i.image, (i.x, i.y))


class Food:
    def __init__(self, width, height, image):
        self.x = None
        self.y = None
        self.image = image
        self.make_food = True

        self.width = width
        self.height = height

    def gen_food(self):
        self.x = randint(16, self.width - 16)
        self.y = randint(16, self.height - 16)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self, win):
        if self.make_food:
            self.gen_food()
            self.make_food = False

        win.blit(self.image, (self.x, self.y))
