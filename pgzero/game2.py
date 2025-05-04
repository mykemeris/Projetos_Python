# -*- coding: utf-8 -*-
"""
Projeto Educacional: Jogo de Plataforma com PgZero

Este é um projeto de exemplo para fins educacionais, voltado para iniciantes na programação em Python.
O objetivo é ensinar conceitos fundamentais de desenvolvimento de jogos 2D utilizando a biblioteca PgZero,
que é baseada no Pygame, mas com uma abordagem mais simples e acessível para quem está começando.

Funcionalidades implementadas:
- Menu inicial com botões interativos
- Protagonista com movimentação, salto e animações
- Plataformas estáticas e inimigos com movimentação automática
- Detecção de colisões e reinício do nível ao colidir com inimigos
- Alternância de estados do jogo: menu e jogando
- Controle de música de fundo

Bibliotecas permitidas:
- PgZero
- math
- random
- pygame.Rect

Este projeto pode ser utilizado como base para aulas de introdução à programação, lógica computacional
e desenvolvimento de jogos.

Pastas do projeto:
- images: contém os sprites dos personagens, plataformas e cenários
- sounds: contém os efeitos sonoros
- music: contém as trilhas sonoras

Próximos passos sugeridos:
- Adicionar múltiplas fases
- Criar uma tela de Game Over
- Implementar coleta de itens e pontuação
- Criar diferentes tipos de inimigos
- Usar variáveis para controlar vidas ou tempo

"""
import os

# posiciona em 0,0 e desativa centralização automática
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
os.environ['SDL_VIDEO_CENTERED']     = '0'

import random
import math
from pygame import Rect

# PgZero constants
TITLE = "My Platformer Adventure"
WIDTH = 800
HEIGHT = 600

gravity = 1200  # pixels per second squared

# --- Recursos ---
PLAYER_IDLE_RIGHT = ["hero_idle_right_0.png", "hero_idle_right_1.png"]
PLAYER_RUN_RIGHT = ["hero_run_right_0.png", "hero_run_right_1.png"]
PLAYER_IDLE_LEFT = ["hero_idle_left_0.png", "hero_idle_left_1.png"]
PLAYER_RUN_LEFT = ["hero_run_left_0.png", "hero_run_left_1.png"]
ENEMY_SPRITES = ["enemy_idle_0.png", "enemy_idle_1.png"]
PLATFORM_IMAGE = "platform.png"
BACKGROUND_IMAGE = "background.png"
MENU_BACKGROUND_IMAGE = "menu_background.png"
MUSIC = "background_music"
JUMP_SOUND = "jump.wav"
DEATH_SOUND = "Death.mp3"

# --- Estados do Jogo ---
GAME_STATE = "menu"  # Pode ser "menu", "playing", "game_over"
MUSIC_ENABLED = True

# Game states
STATE_MENU = 0
STATE_PLAY = 1
STATE_QUIT = 2

state = STATE_MENU
music_on = True

# Menu buttons container
menu_buttons = []
# Mouse position tracker
mouse_pos = (0, 0)

class Button:
    """Simple clickable button"""
    def __init__(self, rect, text, callback):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.hover = False

    def draw(self):
        color = 'lightskyblue' if self.hover else 'dodgerblue'
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=40,
            color='white',
            owidth=1.5,
            ocolor='black'
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)


def init_menu():
    """Create menu buttons"""
    menu_buttons.clear()
    btn_w, btn_h = 300, 60
    x = (WIDTH - btn_w) // 2
    y0 = 200
    spacing = 80
    # Start Game
    menu_buttons.append(Button(
        Rect(x, y0, btn_w, btn_h),
        'Start Game',
        start_game
    ))
    # Toggle Music
    menu_buttons.append(Button(
        Rect(x, y0 + spacing, btn_w, btn_h),
        'Music: On',
        toggle_music
    ))
    # Quit Game
    menu_buttons.append(Button(
        Rect(x, y0 + 2 * spacing, btn_w, btn_h),
        'Quit',
        quit_game
    ))


def start_game():
    """Switch to play state and initialize level"""
    global state
    state = STATE_PLAY
    load_level()
    if music_on:
        music.play(MUSIC)


def toggle_music():
    """Toggle background music"""
    global music_on
    music_on = not music_on
    btn = menu_buttons[1]
    btn.text = f"Music: {'On' if music_on else 'Off'}"
    if music_on:
        music.play(MUSIC)
    else:
        music.stop()


def quit_game():
    """Exit application"""
    exit()

# Entities and world
enemies = []
platforms = []
hero = None

class Hero:
    def __init__(self, pos):
        self.idle_frames = PLAYER_IDLE_RIGHT
        self.run_frames = PLAYER_RUN_RIGHT
        self.frame_index = 0
        self.frame_time = 0.1
        self.time_acc = 0.0

        self.rect = Rect(pos[0], pos[1], 48, 64)
        self.vel = [0, 0]
        self.on_ground = False
        self.facing = 'right'

    def update(self, dt):
        self.vel[0] = 0
        if keyboard.left:
            self.vel[0] = -200
            self.facing = 'left'
        elif keyboard.right:
            self.vel[0] = 200
            self.facing = 'right'
        if keyboard.up and self.on_ground:
            self.vel[1] = -500

        self.vel[1] += gravity * dt

        self.rect.x += self.vel[0] * dt
        self.check_collision('horizontal')
        self.rect.y += self.vel[1] * dt
        self.check_collision('vertical')

        frames = self.run_frames if self.vel[0] != 0 else self.idle_frames
        self.time_acc += dt
        if self.time_acc >= self.frame_time:
            self.time_acc -= self.frame_time
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.current_image = frames[self.frame_index]

    def check_collision(self, direction):
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if direction == 'horizontal':
                    if self.vel[0] > 0:
                        self.rect.right = plat.rect.left
                    elif self.vel[0] < 0:
                        self.rect.left = plat.rect.right
                else:
                    if self.vel[1] > 0:
                        self.rect.bottom = plat.rect.top
                        self.vel[1] = 0
                        self.on_ground = True
                    elif self.vel[1] < 0:
                        self.rect.top = plat.rect.bottom
                        self.vel[1] = 0
        if direction == 'vertical' and self.vel[1] != 0:
            self.on_ground = False

    def draw(self):
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

class Enemy:
    def __init__(self, x1, x2, y):
        self.move_frames = ENEMY_SPRITES
        self.idle_frames = ENEMY_SPRITES
        self.frame_index = 0
        self.frame_time = 0.2
        self.time_acc = 0.0

        self.rect = Rect(x1, y, 48, 48)
        self.bounds = (x1, x2)
        self.base_speed = random.randint(80, 120)
        self.speed = self.base_speed
        self.dir = 1
        self.pause_time = 0
        self.pause_duration = 0

    def update(self, dt):
        if self.pause_time > 0:
            self.pause_time -= dt
            return

        self.rect.x += self.speed * self.dir * dt
        if self.rect.x < self.bounds[0] or self.rect.x > self.bounds[1]:
            self.dir *= -1
            self.speed = random.randint(80, 150)
            self.pause_duration = random.uniform(0.2, 1.0)
            self.pause_time = self.pause_duration

        frames = self.move_frames if self.dir != 0 else self.idle_frames
        self.time_acc += dt
        if self.time_acc >= self.frame_time:
            self.time_acc -= self.frame_time
            self.frame_index = (self.frame_index + 1) % len(frames)
        self.current_image = frames[self.frame_index]

    def draw(self):
        screen.blit(self.current_image, (self.rect.x, self.rect.y))

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = Rect(x, y, w, h)

    def draw(self):
        screen.draw.filled_rect(self.rect, 'sienna')


def load_level():
    global hero, enemies, platforms
    platforms.clear()
    enemies.clear()
    platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))
    platforms.append(Platform(150, 450, 200, 20))
    platforms.append(Platform(450, 350, 200, 20))
    hero = Hero((100, HEIGHT - 100))
    enemies.append(Enemy(160, 330, 410))
    enemies.append(Enemy(460, 630, 310))


def update(dt):
    if state == STATE_PLAY:
        hero.update(dt)
        for e in enemies:
            e.update(dt)
        for e in enemies:
            if hero.rect.colliderect(e.rect):
                load_level()
                break
    elif state == STATE_MENU:
        for btn in menu_buttons:
            btn.check_hover(mouse_pos)


def draw():
    screen.clear()
    if state == STATE_MENU:
        screen.draw.text("My Platformer Adventure",
                         center=(WIDTH//2, 100), fontsize=60, color='white', owidth=2.0, ocolor='black')
        for btn in menu_buttons:
            btn.draw()
    elif state == STATE_PLAY:
        for plat in platforms:
            plat.draw()
        hero.draw()
        for e in enemies:
            e.draw()


def on_mouse_down(pos):
    if state == STATE_MENU:
        for btn in menu_buttons:
            btn.check_click(pos)

def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

init_menu()
