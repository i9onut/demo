import pygame
from settings import WAVES, WIN_WAVE
from .enemy import Enemy

class WaveManager:
    def __init__(self):
        self.wave_index = 0
        self.enemies_to_spawn = 0
        self.spawn_timer = 0
        self.in_progress = False
        self.cooldown_timer = 0
        self.time_between_waves = 3000 # ms
        self.game_won = False

    def update(self, current_time, enemies_list):
    
        if not self.in_progress:
            if current_time > self.cooldown_timer:
                if self.wave_index < len(WAVES):
                    self.start_wave()
                elif self.wave_index == WIN_WAVE and len(enemies_list) == 0:
                    self.game_won = True
            return

        
        if self.enemies_to_spawn > 0:
            wave_data = WAVES[self.wave_index - 1]
            if current_time - self.spawn_timer > wave_data["delay"]:
                new_enemy = Enemy(wave_data["hp"], wave_data["spd"], wave_data["rew"], wave_data["grade"])
                enemies_list.append(new_enemy)
                self.enemies_to_spawn -= 1
                self.spawn_timer = current_time
        
        
        elif len(enemies_list) == 0:
            self.in_progress = False
            self.cooldown_timer = current_time + self.time_between_waves

    def start_wave(self):
        self.enemies_to_spawn = WAVES[self.wave_index]["count"]
        self.in_progress = True
        self.wave_index += 1