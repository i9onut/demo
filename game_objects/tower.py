import pygame
import math
from settings import BLACK

class Projectile:
    def __init__(self, x, y, target, damage, color):
        self.x, self.y = x, y
        self.target = target
        self.damage = damage
        self.speed = 10
        self.color = color
        self.alive = True

    def update(self, enemies):
        if self.target not in enemies: 
            self.alive = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.speed:
            self.target.health -= self.damage
            self.alive = False
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)

class Tower:
    def __init__(self, x, y, data):
        self.x, self.y = x, y
        self.range = data['range']
        self.damage = data['damage']
        self.cooldown_time = data['cooldown']
        self.color = data['color']
        self.last_shot_time = 0
        
    def update(self, enemies, current_time, projectiles_list):
        if current_time - self.last_shot_time < self.cooldown_time:
            return

        closest_enemy = None
        min_dist = self.range + 1

        for enemy in enemies:
            dist = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if dist < self.range and dist < min_dist:
                min_dist = dist
                closest_enemy = enemy
        
        if closest_enemy:
            projectiles_list.append(Projectile(self.x, self.y, closest_enemy, self.damage, self.color))
            self.last_shot_time = current_time

    def draw(self, surface):
        rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)