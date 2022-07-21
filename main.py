import random
import sys

import pygame

pygame.init()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BULLET_RADIUS = 6
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
FRAMES_PER_SECOND = 30


class Player(pygame.sprite.Sprite):

    def __init__(self, name, x=0, y=0):
        super().__init__()

        self.name = name
        if name == "player":
            self.color = (150, 0, 0)
            self.direction_moving = None
            self.hit_points = 20
            self.speed = 10
            location_x = SCREEN_WIDTH / 2 - PLAYER_WIDTH / 2
            location_y = SCREEN_HEIGHT - (PLAYER_HEIGHT * 2)
        elif name == "enemy":
            self.color = (0, 150, 0)
            self.direction_moving = pygame.K_RIGHT
            self.hit_points = 6
            self.speed = 5
            location_x = x
            location_y = y
        elif name == "enemy2":
            self.color = (0, 0, 150)
            self.direction_moving = pygame.K_RIGHT
            self.hit_points = 6
            self.speed = 5
            location_x = x
            location_y = y

        self.bullets = []
        self.rect = pygame.rect.Rect(location_x, location_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.time_since_last_bullet = 0
        self.time_since_last_move = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def fire(self):

        if len(self.bullets) <= 3 and pygame.time.get_ticks() - self.time_since_last_bullet > 100:
            self.bullets.append(Bullet("player", self.rect.x, self.rect.y))
            self.time_since_last_bullet = pygame.time.get_ticks()

    def move(self, direction=pygame.K_RIGHT):

        move_x = 0
        move_y = 0

        if self.name == "player":
            if direction == pygame.K_LEFT and self.rect.left > 0:
                move_x = -1 * self.speed
            elif direction == pygame.K_RIGHT and self.rect.right < SCREEN_WIDTH:
                move_x = 1 * self.speed
        else:
            if self.direction_moving == pygame.K_LEFT:
                # bounce it
                if self.rect.left <= 0:
                    self.direction_moving = pygame.K_RIGHT
                    move_y += PLAYER_HEIGHT + int(PLAYER_HEIGHT / 4)
                else:
                    move_x += self.speed * -1
            elif self.direction_moving == pygame.K_RIGHT:
                # bounce it
                if self.rect.right > SCREEN_WIDTH - PLAYER_WIDTH:
                    self.direction_moving = pygame.K_LEFT
                    move_y += PLAYER_HEIGHT + int(PLAYER_HEIGHT / 4)
                else:
                    move_x -= self.speed * -1

        self.rect.x += move_x
        self.rect.y += move_y

    def takeDamage(self, damage_points):
        self.hit_points -= damage_points
        return self.hit_points <= 0


class Bullet(pygame.sprite.Sprite):

    def __init__(self, name, x, y):
        super().__init__()
        self.name = name

        if name == "player":
            self.color = (210, 210, 210)
            self.damage_points = 4
            self.speed = 30
        elif name == "enemy":
            self.color = (0, 150, 0)
            self.damage_points = 2
            self.speed = 15
        elif name == "enemy2":
            self.color = (0, 0, 150)
            self.damage_points = 2
            self.speed = 15

        self.rect = pygame.Rect(x + PLAYER_WIDTH / 2, y, BULLET_RADIUS, BULLET_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.rect.x, self.rect.y), BULLET_RADIUS)

    def move(self):

        delta_y = self.rect.y
        if self.name == "player":
            delta_y += self.speed * -1
        else:
            delta_y += self.speed * 1

        self.rect.y = delta_y


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.time = pygame.time.Clock()
        self.player = Player("player")
        self.enemies = pygame.sprite.Group()

        for start_x in range(int(PLAYER_WIDTH / 2), int(SCREEN_WIDTH - PLAYER_WIDTH / 2), int(PLAYER_WIDTH + (int(PLAYER_WIDTH / 4)))):
            self.enemies.add(Player("enemy", start_x, 64))

    def checkCollisions(self):

        for bullet in self.player.bullets:

            if bullet.rect.y < 0:
                self.player.bullets.remove(bullet)
                bullet.kill()

            enemy_hit_by_bullet = pygame.sprite.spritecollideany(bullet, self.enemies)
            if enemy_hit_by_bullet is not None:

                # Kill the bullet
                self.player.bullets.remove(bullet)
                bullet.kill()

                # Are they dead?
                if enemy_hit_by_bullet.takeDamage(bullet.damage_points):
                    enemy_hit_by_bullet.kill()

    def handleInput(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(pygame.K_LEFT)
        elif keys[pygame.K_RIGHT]:
            self.player.move(pygame.K_RIGHT)

        if keys[pygame.K_SPACE]:
            self.player.fire()

    def updateScreen(self):

        self.screen.fill((0, 0, 0))

        for enemy in self.enemies:
            enemy.move()
            enemy.draw(self.screen)

        for bullet in self.player.bullets:
            bullet.move()
            bullet.draw(self.screen)

        self.player.draw(self.screen)

        pygame.display.update()
        self.time.tick(FRAMES_PER_SECOND)

    def loop(self):

        while True:
            self.checkCollisions()
            self.handleInput()
            self.updateScreen()


if "__main__":
    game = Game()
    game.loop()