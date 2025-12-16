import pygame
import math
from settings import *

class Player:
    def __init__(self):
        self.grid_x, self.grid_y = PLAYER_START_POS
        self.move_timer = 0
        self.attack_timer = 0
        self.is_attacking = False
        
        # Pixel position for smooth drawing or collision logic
        self.x = self.grid_x * TILE_SIZE
        self.y = self.grid_y * TILE_SIZE
        
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            
        return dx, dy, keys[pygame.K_SPACE]

    def update(self, dt, enemies):
        current_time = pygame.time.get_ticks()
        dx, dy, attack_key = self.handle_input()

        # --- Movement ---
        if (dx != 0 or dy != 0) and (current_time - self.move_timer > PLAYER_MOVE_DELAY):
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            # Bounds Check (Stay within Map Area)
            if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:
                self.grid_x = new_x
                self.grid_y = new_y
                self.move_timer = current_time

        # Update pixel position (snapped to grid)
        self.x = self.grid_x * TILE_SIZE
        self.y = self.grid_y * TILE_SIZE
        self.rect.topleft = (self.x, self.y)

        # --- Attack ---
        self.is_attacking = False
        if attack_key and (current_time - self.attack_timer > PLAYER_ATTACK_COOLDOWN):
            self.attack(enemies)
            self.attack_timer = current_time
            self.is_attacking = True

    def attack(self, enemies):
        # Center of player
        px = self.x + TILE_SIZE // 2
        py = self.y + TILE_SIZE // 2
        
        for enemy in enemies:
            # Distance check
            dist = math.sqrt((enemy.x - px)**2 + (enemy.y - py)**2)
            if dist <= PLAYER_ATTACK_RANGE:
                enemy.health -= PLAYER_DAMAGE
                if enemy.health < 0:
                    enemy.health = 0

    def draw(self, surface):
        # Draw Player
        color = RED if self.is_attacking else PLAYER_COLOR
        
        # Slightly smaller than tile to see grid
        draw_rect = pygame.Rect(
            self.x + 4, self.y + 4, 
            TILE_SIZE - 8, TILE_SIZE - 8
        )
        pygame.draw.rect(surface, color, draw_rect)
        pygame.draw.rect(surface, BLACK, draw_rect, 2)
        
        # Attack Visual
        if self.is_attacking:
            cx = self.x + TILE_SIZE // 2
            cy = self.y + TILE_SIZE // 2
            pygame.draw.circle(surface, (255, 200, 50), (cx, cy), PLAYER_ATTACK_RANGE, 2)