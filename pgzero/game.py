# -*- coding: utf-8 -*-
#"""
#Platformer Game
#Only uses PgZero, math, random, and Rect from pygame.
#Genres: Platformer
#"""
import random
import math
from pygame import Rect

#    PgZero constants
TITLE = "My Platformer Adventure"
WIDTH = 800
HEIGHT = 600

gravity = 1200  # pixels per second squared

# Game states\STATE_MENU = 0
STATE_PLAY = 1
STATE_QUIT = 2

state = STATE_MENU
music_on = True

# Menu buttons container
menu_buttons = []

class Button:
    """Simple clickable button"""
    def __init__(self, rect, text, callback):
        self.rect = rect
        self.text = text
        self.callback = callback

    def draw(self):
        screen.draw.filled_rect(self.rect, 'dodgerblue')
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=40,
            color='white'
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()


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
        music.play('bg_music', loop=True)


def toggle_music():
    """Toggle background music"""
    global music_on
    music_on = not music_on
    btn = menu_buttons[1]
    btn.text = f"Music: {'On' if music_on else 'Off'}"
    if music_on:
        music.play('bg_music', loop=True)
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
        # load sprite frames (assumes images in images/hero/ ...)
        self.idle_frames = [f'hero_idle_{i}' for i in range(2)]
        self.run_frames = [f'hero_run_{i}' for i in range(4)]
        self.frame_index = 0
        self.frame_time = 0.1
        self.time_acc = 0.0

        self.rect = Rect(pos[0], pos[1], 48, 64)
        self.vel = [0, 0]
        self.on_ground = False
        self.facing = 'right'

    def update(self, dt):
        # input
        self.vel[0] = 0
        if keyboard.left:
            self.vel[0] = -200
            self.facing = 'left'
        elif keyboard.right:
            self.vel[0] = 200
            self.facing = 'right'
        if keyboard.up and self.on_ground:
            self.vel[1] = -500

        # apply gravity
        self.vel[1] += gravity * dt

        # move and collide
        self.rect.x += self.vel[0] * dt
        self.check_collision('horizontal')
        self.rect.y += self.vel[1] * dt
        self.check_collision('vertical')

        # animation
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
        self.move_frames = [f'enemy_move_{i}' for i in range(2)]
        self.idle_frames = [f'enemy_idle_{i}' for i in range(2)]
        self.frame_index = 0
        self.frame_time = 0.2
        self.time_acc = 0.0

        self.rect = Rect(x1, y, 48, 48)
        self.bounds = (x1, x2)
        self.speed = 100
        self.dir = 1

    def update(self, dt):
        # patrol
        self.rect.x += self.speed * self.dir * dt
        if self.rect.x < self.bounds[0] or self.rect.x > self.bounds[1]:
            self.dir *= -1

        # animation
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
    """Setup hero, platforms, enemies"""
    global hero, enemies, platforms
    platforms.clear()
    enemies.clear()
    # ground
    platforms.append(Platform(0, HEIGHT - 40, WIDTH, 40))
    # floating platforms
    platforms.append(Platform(150, 450, 200, 20))
    platforms.append(Platform(450, 350, 200, 20))
    # hero
    hero = Hero((100, HEIGHT - 100))
    # enemies on platforms
    enemies.append(Enemy(160, 330, 410))
    enemies.append(Enemy(460, 630, 310))


def update(dt):
    if state == STATE_PLAY:
        hero.update(dt)
        for e in enemies:
            e.update(dt)
        # check collisions hero vs enemy
        for e in enemies:
            if hero.rect.colliderect(e.rect):
                # reset level on collision
                load_level()
                sounds.hit.play()
                break


def draw():
    screen.clear()
    if state == STATE_MENU:
        screen.draw.text("My Platformer Adventure",
                         center=(WIDTH//2, 100), fontsize=60, color='white')
        for btn in menu_buttons:
            btn.draw()
    elif state == STATE_PLAY:
        for plat in platforms:
            plat.draw()
        hero.draw()
        for e in enemies:
            e.draw()

init_menu()
