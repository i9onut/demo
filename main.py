import pygame
import math
import settings as s
from game_objects import Enemy, Tower, WaveManager, Player

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Grid Defense")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 40)

# --- Shop Button Class (UI) ---
class ShopButton:
    def __init__(self, x, y, tower_key):
        self.rect = pygame.Rect(x, y, 80, 80)
        self.tower_key = tower_key
        self.data = s.TOWER_TYPES[tower_key]

    def draw(self, surface, money, selected_key):
        color = self.data['color']
        if money < self.data['cost']: color = s.GRAY
        
        pygame.draw.rect(surface, color, self.rect)
        
        if selected_key == self.tower_key:
             pygame.draw.rect(surface, s.WHITE, self.rect, 4)
        else:
             pygame.draw.rect(surface, s.BLACK, self.rect, 2)

        label = font.render(f"{self.data['name']}", True, s.BLACK)
        cost_label = font.render(f"${self.data['cost']}", True, s.BLACK)
        surface.blit(label, (self.rect.x + 5, self.rect.y + 5))
        surface.blit(cost_label, (self.rect.x + 5, self.rect.y + 55))

# --- Game Globals ---
game_state = "playing" # playing, won, lost
money = s.STARTING_MONEY
lives = s.STARTING_LIVES
selected_tower = None

enemies = []
towers = []
projectiles = []
shop_buttons = []

# Instantiate Managers and Player
wave_manager = WaveManager()
player = Player()

# Setup Shop
btn_x = 20
for key in s.TOWER_TYPES:
    shop_buttons.append(ShopButton(btn_x, s.HEIGHT - 90, key))
    btn_x += 100

def get_grid_pos(mouse_pos):
    col = mouse_pos[0] // s.TILE_SIZE
    row = mouse_pos[1] // s.TILE_SIZE
    return col, row

def can_place_tower(col, row):
    # Check bounds
    if not (0 <= col < s.GRID_COLS and 0 <= row < s.GRID_ROWS):
        return False
        
    # Check if a tower is already here
    # Towers are stored with pixel coordinates (center), we need to check grid alignment
    # Center of a tile (col, row) is col*SIZE + SIZE/2
    target_x = col * s.TILE_SIZE + s.TILE_SIZE // 2
    target_y = row * s.TILE_SIZE + s.TILE_SIZE // 2
    
    for t in towers:
        if t.x == target_x and t.y == target_y:
            return False
            
    # Optional: Don't place on player
    if player.grid_x == col and player.grid_y == row:
        return False
        
    return True

running = True
while running:
    dt = clock.tick(s.FPS)
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            # 1. Click UI
            if mouse_pos[1] > s.MAP_HEIGHT:
                selected_tower = None
                for btn in shop_buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        selected_tower = btn.tower_key
            
            # 2. Click Map (Place Tower)
            elif mouse_pos[1] < s.MAP_HEIGHT and selected_tower:
                col, row = get_grid_pos(mouse_pos)
                
                if can_place_tower(col, row):
                    cost = s.TOWER_TYPES[selected_tower]["cost"]
                    if money >= cost:
                        # Place in center of tile
                        tx = col * s.TILE_SIZE + s.TILE_SIZE // 2
                        ty = row * s.TILE_SIZE + s.TILE_SIZE // 2
                        towers.append(Tower(tx, ty, s.TOWER_TYPES[selected_tower]))
                        money -= cost

    # --- Update ---
    if game_state == "playing":
        wave_manager.update(current_time, enemies)
        if wave_manager.game_won:
            game_state = "won"

        # Update Player
        player.update(dt, enemies)

        # Update Enemies
        enemies_to_remove = []
        for enemy in enemies:
            enemy.update()
            if enemy.finished:
                lives -= 1
                enemies_to_remove.append(enemy)
                if lives <= 0: game_state = "lost"
            elif enemy.health <= 0:
                money += enemy.reward
                enemies_to_remove.append(enemy)
        
        for e in enemies_to_remove:
            if e in enemies: enemies.remove(e)

        # Update Towers and Projectiles
        for tower in towers:
            tower.update(enemies, current_time, projectiles)
        
        projectiles = [p for p in projectiles if p.alive]
        for p in projectiles:
            p.update(enemies)

    # --- Draw ---
    screen.fill(s.BROWN)

    # 1. Draw Grid Lines
    for x in range(0, s.WIDTH, s.TILE_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, s.MAP_HEIGHT), 1)
    for y in range(0, s.MAP_HEIGHT + 1, s.TILE_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (s.WIDTH, y), 1)

    # 2. Draw Path
    if len(s.PATH_POINTS) > 1:
        pygame.draw.lines(screen, s.PATH_COLOR, False, s.PATH_POINTS, 10)
    
    # Base
    pygame.draw.circle(screen, s.BLUE, s.BASE_POS, 20)

    # 3. Entities
    for e in enemies: e.draw(screen)
    for t in towers: t.draw(screen)
    for p in projectiles: p.draw(screen)
    
    # 4. Player
    player.draw(screen)

    # 5. UI Panel
    pygame.draw.rect(screen, s.GRAY, (0, s.MAP_HEIGHT, s.WIDTH, s.UI_HEIGHT))
    pygame.draw.line(screen, s.BLACK, (0, s.MAP_HEIGHT), (s.WIDTH, s.MAP_HEIGHT), 3)
    
    for btn in shop_buttons:
        btn.draw(screen, money, selected_tower)

    # Stats
    stats_text = font.render(f"Money: ${money} | Lives: {lives} | Wave: {wave_manager.wave_index}/{s.WIN_WAVE}", True, s.WHITE)
    screen.blit(stats_text, (10, 10))

    # Controls Hint
    hint_text = font.render("WASD to Move | SPACE to Attack", True, s.WHITE)
    screen.blit(hint_text, (s.WIDTH - 300, 10))

    # Tower Placement Preview
    if selected_tower and mouse_pos[1] < s.MAP_HEIGHT:
         col, row = get_grid_pos(mouse_pos)
         # Snap preview to grid center
         px = col * s.TILE_SIZE + s.TILE_SIZE // 2
         py = row * s.TILE_SIZE + s.TILE_SIZE // 2
         
         range_rad = s.TOWER_TYPES[selected_tower]['range']
         range_surf = pygame.Surface((range_rad*2, range_rad*2), pygame.SRCALPHA)
         pygame.draw.circle(range_surf, (255, 255, 255, 50), (range_rad, range_rad), range_rad)
         screen.blit(range_surf, (px-range_rad, py-range_rad))

    # Game Over Overlay
    if game_state != "playing":
        overlay = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0,0))
        msg = "VICTORY!" if game_state == "won" else "DEFEAT!"
        color = s.GREEN if game_state == "won" else s.RED
        text = big_font.render(msg, True, color)
        screen.blit(text, text.get_rect(center=(s.WIDTH/2, s.HEIGHT/2)))

    pygame.display.flip()

pygame.quit()