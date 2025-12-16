import pygame
import math
import settings as s
# Import from our new package
from game_objects import Enemy, Tower, WaveManager

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Medieval Tower Defense")
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


wave_manager = WaveManager()
btn_x = 20
for key in s.TOWER_TYPES:
    shop_buttons.append(ShopButton(btn_x, s.HEIGHT - 90, key))
    btn_x += 100

def can_place_tower(pos):
    for t in towers:
        dist = math.sqrt((t.x - pos[0])**2 + (t.y - pos[1])**2)
        if dist < 35: return False
    return True


running = True
while running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            
            if mouse_pos[1] > s.MAP_HEIGHT:
                selected_tower = None
                for btn in shop_buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        selected_tower = btn.tower_key
            
            
            elif mouse_pos[1] < s.MAP_HEIGHT and selected_tower:
                cost = s.TOWER_TYPES[selected_tower]["cost"]
                if money >= cost and can_place_tower(mouse_pos):
                    towers.append(Tower(mouse_pos[0], mouse_pos[1], s.TOWER_TYPES[selected_tower]))
                    money -= cost

    
    if game_state == "playing":
      
        wave_manager.update(current_time, enemies)
        if wave_manager.game_won:
            game_state = "won"

        
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

        
        for tower in towers:
            tower.update(enemies, current_time, projectiles)
        
        projectiles = [p for p in projectiles if p.alive]
        for p in projectiles:
            p.update(enemies)

    
    screen.fill(s.BROWN)

    if len(s.PATH_POINTS) > 1:
        pygame.draw.lines(screen, s.PATH_COLOR, False, s.PATH_POINTS, 30)
    
    pygame.draw.circle(screen, s.BLUE, s.BASE_POS, 30)
    pygame.draw.circle(screen, s.GREEN, (s.BASE_POS[0]-10, s.BASE_POS[1]-5), 10)

    for e in enemies: e.draw(screen)
    for t in towers: t.draw(screen)
    for p in projectiles: p.draw(screen)

    
    pygame.draw.rect(screen, s.GRAY, (0, s.MAP_HEIGHT, s.WIDTH, s.UI_HEIGHT))
    pygame.draw.line(screen, s.BLACK, (0, s.MAP_HEIGHT), (s.WIDTH, s.MAP_HEIGHT), 3)
    
    for btn in shop_buttons:
        btn.draw(screen, money, selected_tower)

    stats_text = font.render(f"Money: ${money} | Lives: {lives} | Wave: {wave_manager.wave_index}/{s.WIN_WAVE}", True, s.WHITE)
    screen.blit(stats_text, (10, 10))

    if selected_tower and mouse_pos[1] < s.MAP_HEIGHT:
         range_rad = s.TOWER_TYPES[selected_tower]['range']
         range_surf = pygame.Surface((range_rad*2, range_rad*2), pygame.SRCALPHA)
         pygame.draw.circle(range_surf, (255, 255, 255, 50), (range_rad, range_rad), range_rad)
         screen.blit(range_surf, (mouse_pos[0]-range_rad, mouse_pos[1]-range_rad))

    if game_state != "playing":
        overlay = pygame.Surface((s.WIDTH, s.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0,0))
        msg = "VICTORY!" if game_state == "won" else "DEFEAT!"
        color = s.GREEN if game_state == "won" else s.RED
        text = big_font.render(msg, True, color)
        screen.blit(text, text.get_rect(center=(s.WIDTH/2, s.HEIGHT/2)))

    pygame.display.flip()
    clock.tick(s.FPS)

pygame.quit()