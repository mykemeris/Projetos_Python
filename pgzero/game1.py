import os

TITLE = "Game Jornada do Soldado Mediavel"

# posiciona em 0,0 e desativa centralização automática
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
os.environ['SDL_VIDEO_CENTERED']     = '0'

import pgzrun
import math
import random
from pygame import Rect

# --- Configurações do Jogo ---
WIDTH = 800
HEIGHT = 600
GRAVITY = 1
JUMP_POWER = -20
PLAYER_SPEED = 5
ENEMY_SPEED = 2
FPS = 30

# --- Recursos ---
PLAYER_IDLE_RIGHT = ["hero_idle_right_0.png", "hero_idle_right_1.png"]
PLAYER_RUN_RIGHT = ["hero_run_right_0.png", "hero_run_right_1.png"]
PLAYER_IDLE_LEFT = ["hero_idle_left_0.png", "hero_idle_left_1.png"]
PLAYER_RUN_LEFT = ["hero_run_left_0.png", "hero_run_left_1.png"]
ENEMY_SPRITES = ["enemy_idle_0.png", "enemy_idle_1.png"]
PLATFORM_IMAGE = "platform.png"
BACKGROUND_IMAGE = "background.png"
MENU_BACKGROUND_IMAGE = "menu_background.png"
MUSIC = "background_music.mp3"
JUMP_SOUND = "jump.wav"
DEATH_SOUND = "Death.mp3"

# --- Estados do Jogo ---
GAME_STATE = "menu"  # Pode ser "menu", "playing", "game_over"
MUSIC_ENABLED = True

# --- Classes ---

class Entity(Actor):
    """Classe base para entidades com animação."""
    def __init__(self, image, pos, frames, animation_speed=0.1):
        super().__init__(image, pos)
        self.frames = frames
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.animation_timer = 0.0

    def update_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

class Hero(Entity):
    """Classe para o personagem principal."""
    def __init__(self, pos):
        super().__init__(PLAYER_IDLE_RIGHT[0], pos, PLAYER_IDLE_RIGHT)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.facing_right = True

    def update(self, dt, platforms):
        self.vx = 0
        if keyboard.left:
            self.vx = -PLAYER_SPEED
            if self.on_ground:
                self.frames = PLAYER_RUN_LEFT
            else:
                self.image = PLAYER_RUN_LEFT[0] # Manter um frame de corrida no ar
            self.facing_right = False
        elif keyboard.right:
            self.vx = PLAYER_SPEED
            if self.on_ground:
                self.frames = PLAYER_RUN_RIGHT
            else:
                self.image = PLAYER_RUN_RIGHT[0] # Manter um frame de corrida no ar
            self.facing_right = True
        else:
            if self.facing_right:
                self.frames = PLAYER_IDLE_RIGHT
            else:
                self.frames = PLAYER_IDLE_LEFT

        if not self.on_ground:
            self.vy += GRAVITY

        self.x += self.vx
        self.y += self.vy

        self.on_ground = False
        for platform in platforms:
            if self.colliderect(platform):
                if self.vy > 0:
                    self.bottom = platform.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.top = platform.bottom
                    self.vy = 0

        if keyboard.space and self.on_ground:
            self.vy = JUMP_POWER
            if MUSIC_ENABLED:
                sounds.jump.play()

        self.update_animation(dt)
        if self.vx == 0 and self.on_ground:
            self.update_animation(dt) # Animação de idle quando parado no chão

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_POWER
            self.on_ground = False
            if MUSIC_ENABLED:
                sounds.jump.play()

class Enemy(Entity):
    """Classe para os inimigos."""
    def __init__(self, pos, patrol_area):
        super().__init__(ENEMY_SPRITES[0], pos, ENEMY_SPRITES, animation_speed=0.2)
        self.vx = ENEMY_SPEED
        self.patrol_left = patrol_area[0]
        self.patrol_right = patrol_area[1]

    def update(self, dt):
        self.x += self.vx
        if self.x < self.patrol_left:
            self.vx = ENEMY_SPEED
        elif self.x > self.patrol_right:
            self.vx = -ENEMY_SPEED
        self.update_animation(dt)

# --- Objetos do Jogo ---
hero = Hero((50, HEIGHT - 150))
platforms = [
    Actor(PLATFORM_IMAGE, (100, HEIGHT - 20)),
    Actor(PLATFORM_IMAGE, (300, HEIGHT - 100)),
    Actor(PLATFORM_IMAGE, (500, HEIGHT - 50)),
    Actor(PLATFORM_IMAGE, (700, HEIGHT - 150))
]
enemies = [
    Enemy((200, HEIGHT - 40), (150, 250)),
    Enemy((600, HEIGHT - 70), (550, 650))
]
background = Actor(BACKGROUND_IMAGE, (WIDTH // 2, HEIGHT // 2))
menu_background = Actor(MENU_BACKGROUND_IMAGE, (WIDTH // 2, HEIGHT // 2))

# --- Botões do Menu ---
start_button_rect = Rect(WIDTH // 2 - 100, 200, 200, 50)
music_button_rect = Rect(WIDTH // 2 - 100, 270, 200, 50)
exit_button_rect = Rect(WIDTH // 2 - 100, 340, 200, 50)

def draw():
    if GAME_STATE == "menu":
        menu_background.draw()
        screen.draw.text("Game Platformer X", center=(WIDTH // 2, 90), fontsize=48, color="white", ocolor='black')
        screen.draw.rect(start_button_rect, (100, 100, 100))
        screen.draw.text("Comecar Jogo", center=start_button_rect.center, fontsize=24, color="white", ocolor='black')
        screen.draw.rect(music_button_rect, (100, 100, 100))
        music_text = "Musica ON" if MUSIC_ENABLED else "Musica OFF"
        screen.draw.text(music_text, center=music_button_rect.center, fontsize=24, color="white", ocolor='black')
        screen.draw.rect(exit_button_rect, (100, 100, 100))
        screen.draw.text("Sair", center=exit_button_rect.center, fontsize=24, color="white", ocolor='black')
 
    elif GAME_STATE == "playing":
        background.draw()
        for platform in platforms:
            platform.draw()
        hero.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text("Pressione a Tecla ALT pra pular", center=(WIDTH // 2, 100), fontsize=48, color="white", ocolor='black')
    elif GAME_STATE == "game_over":
        screen.fill("black")
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 30), fontsize=48, color="red")
        screen.draw.text("Pressione ESPACO para reiniciar", center=(WIDTH // 2, HEIGHT // 2 + 30), fontsize=24, color="white")

def update(dt):
    global GAME_STATE
    if GAME_STATE == "playing":
        hero.update(dt, platforms)
        for enemy in enemies:
            enemy.update(dt)
            if hero.colliderect(enemy):
                GAME_STATE = "game_over"
                if MUSIC_ENABLED:
                    sounds.death.play()
                    music.stop()

def on_mouse_down(pos):
    global GAME_STATE, MUSIC_ENABLED
    if GAME_STATE == "menu":
        if start_button_rect.collidepoint(pos):
            GAME_STATE = "playing"
            if MUSIC_ENABLED:
                music.play(MUSIC)
        elif music_button_rect.collidepoint(pos):
            MUSIC_ENABLED = not MUSIC_ENABLED
            if MUSIC_ENABLED:
                music.play(MUSIC)
            else:
                music.stop()
        elif exit_button_rect.collidepoint(pos):
            quit()
    elif GAME_STATE == "game_over":
        pass # Adicionar lógica de reinício se pressionar espaço na função update

def on_key_down(key):
    global GAME_STATE, hero, enemies
    if GAME_STATE == "game_over" and key == keys.SPACE:
        GAME_STATE = "playing"
        hero = Hero((100, HEIGHT - 50))
        enemies = [
            Enemy((200, HEIGHT - 40), (150, 250)),
            Enemy((600, HEIGHT - 70), (550, 650))
        ]
        if MUSIC_ENABLED:
            music.play(MUSIC)

pgzrun.go()