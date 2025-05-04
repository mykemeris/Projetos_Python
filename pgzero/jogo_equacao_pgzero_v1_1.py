
# -*- coding: utf-8 -*-
#✅ O que esse código já faz:
#   Mostra uma equação do tipo: resultado ÷ x = ?

#   Gera 4 respostas (1 correta, 3 falsas)
#   Mostra a pontuação
#   Mostra uma mensagem de "acertou" ou "errou"
#   Detecta cliques nas opções e atualiza a pontuação
#   para rodar o projeto > pgzrun jogo_equacao_pgzero_v1_1.py
TITLE = "Jogo de matematica"
import os

# posiciona em 0,0 e desativa centralização automática
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
os.environ['SDL_VIDEO_CENTERED']     = '0'

import random
import time
from pygame import Rect




WIDTH = 800
HEIGHT = 600

pontuacao = 0
pergunta = ""
respostas = []
resposta_certa = 0
botoes = []

# --- NOVAS VARIAVEIS ---
TIME_LIMIT = 30.0               # segundos por pergunta
question_start = 0.0            # quando a pergunta atual comecou
feedback = ""                   # texto: "Acertou!", "Errou!"
feedback_timer = 0.0            # quanto tempo ainda mostrar o feedback

def nova_pergunta():
    global pergunta, respostas, resposta_certa, botoes
    global question_start

    botoes = []
    x = random.randint(2, 10)
    resultado = x * random.randint(1, 10)
    # usando escape unicode \u00F7 para o simbolo de divisao
    pergunta = f"{resultado} \u00F7 {x} = ?"
    resposta_certa = resultado // x

    respostas = [resposta_certa]
    # gera respostas falsas aleatorias
    while len(respostas) < 4:
        falsa = random.randint(1, 10)
        if falsa not in respostas:
            respostas.append(falsa)
    random.shuffle(respostas)

    # posiciona os botoes
    for i in range(4):
        rect = Rect(300, 200 + i * 80, 200, 50)
        botoes.append(rect)

    # reinicia o cronometro
    question_start = time.time()

nova_pergunta()

def update(dt):
    global feedback, feedback_timer

    # atualiza o timer do feedback
    if feedback_timer > 0:
        feedback_timer -= dt
        if feedback_timer <= 0:
            feedback = ""

    # verifica se o tempo acabou
    elapsed = time.time() - question_start
    if elapsed >= TIME_LIMIT:
        nova_pergunta()

def draw():
    screen.clear()

    # pontuacao usando escapes unicode
    screen.draw.text(f"Pontua\u00E7\u00E3o: {pontuacao}", (10, 10), fontsize=40)

    # temporizador
    elapsed = time.time() - question_start
    time_left = max(0, int(TIME_LIMIT - elapsed))
    screen.draw.text(f"Tempo: {time_left}s", (WIDTH - 160, 10), fontsize=35)

    # pergunta
    screen.draw.text(pergunta, center=(WIDTH//2, 100), fontsize=50)

    # botoes de resposta
    for i, rect in enumerate(botoes):
        screen.draw.filled_rect(rect, "orange")
        screen.draw.text(str(respostas[i]),
                         center=rect.center,
                         fontsize=40, color="black")

    # feedback
    if feedback:
        screen.draw.text(feedback,
                         center=(WIDTH//2, HEIGHT//2 + 200),
                         fontsize=60, color="yellow")

def on_mouse_down(pos):
    global pontuacao, feedback, feedback_timer

    if feedback_timer > 0:
        return
    #verifica se o botão clicado confere com a resposta certa
    for i, rect in enumerate(botoes):
        if rect.collidepoint(pos):
            if respostas[i] == resposta_certa:
                pontuacao += 1
                feedback = "Acertou!"
            else:
                if pontuacao > 0:
                    pontuacao -= 1
                feedback = "Errou!"
            feedback_timer = 1.5
            nova_pergunta()
            break
