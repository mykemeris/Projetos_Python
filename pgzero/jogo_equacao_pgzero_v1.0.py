# -*- coding: utf-8 -*-
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

# --- NOVAS VARIÁVEIS ---
TIME_LIMIT = 15.0               # segundos por pergunta
question_start = 0.0            # quando a pergunta atual começou
feedback = ""                   # texto: “Acertou!”, “Errou!”
feedback_timer = 0.0            # quanto tempo ainda mostrar o feedback

def nova_pergunta():
    global pergunta, respostas, resposta_certa, botoes
    global question_start

    botoes = []
    x = random.randint(2, 10)
    resultado = x * random.randint(1, 10)
    pergunta = f"{resultado} \u00F7 {x} = ?"
    resposta_certa = resultado // x

    respostas = [resposta_certa]
    while len(respostas) < 4:
        falsa = random.randint(1, 10)
        if falsa not in respostas:
            respostas.append(falsa)
    random.shuffle(respostas)

    # criar botoes na tela
    for i in range(4):
        rect = Rect(300, 200 + i * 80, 200, 50)
        botoes.append(rect)

    # reinicia o cronômetro
    question_start = time.time()

# primeira pergunta
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

    # pontuação
    screen.draw.text(f"Pontua\u00E7\u00E3o: {pontuacao}", (10, 10), fontsize=40)

    # temporizador
    elapsed = time.time() - question_start
    time_left = max(0, int(TIME_LIMIT - elapsed))
    screen.draw.text(f"Tempo: {time_left}s", (WIDTH - 160, 10), fontsize=35)

    # pergunta
    screen.draw.text(pergunta, center=(WIDTH//2, 100), fontsize=50)

    # botões de resposta
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

    # só processa clique se o feedback já tiver expirado
    if feedback_timer > 0:
        return

    for i, rect in enumerate(botoes):
        if rect.collidepoint(pos):
            if respostas[i] == resposta_certa:
                pontuacao += 1
                feedback = "Acertou!"
            else:
                if pontuacao > 0:
                    pontuacao -= 1
                feedback = "Errou!"
            # exibe feedback por 1.5 segundos
            feedback_timer = 1.5
            # gera a próxima pergunta (reinicia timer)
            nova_pergunta()
            break
