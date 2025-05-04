#[inicio codigo]

#-*- coding: utf-8 -*-
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

pontuacao = 0
pergunta = ""
respostas = []
resposta_certa = 0
botoes = []

def nova_pergunta():
    global pergunta, respostas, resposta_certa, botoes
    botoes = []
    x = random.randint(2, 10)
    resultado = x * random.randint(1, 10)
    #pergunta = f"{resultado} ÷ {x} = ?"
    pergunta = f"{resultado} \u00F7 {x} = ?"
    #
    #Isso evita totalmente depender do encoding do arquivo, porque \u00E7 (ç), \u00E3 (ã) e \u00F7 (÷) sempre mapearão para o caractere correto.
    resposta_certa = resultado // x
    respostas = [resposta_certa]

    while len(respostas) < 4:
        falsa = random.randint(1, 10)
        if falsa not in respostas:
            respostas.append(falsa)

    random.shuffle(respostas)

    for i in range(4):
        rect = Rect(300, 200 + i * 80, 200, 50)
        botoes.append(rect)

nova_pergunta()

def draw():
    screen.clear()
    #screen.draw.text(f"Pontuação: {pontuacao}", (10, 10), fontsize=40)
      # usando escapes unicode em vez de "ç", "ã", "÷"
    screen.draw.text(f"Pontua\u00E7\u00E3o: {pontuacao}", (10, 10), fontsize=40)
    screen.draw.text(pergunta, center=(WIDTH//2, 100), fontsize=50)
    

    for i in range(4):
        screen.draw.filled_rect(botoes[i], "orange")
        screen.draw.text(str(respostas[i]), center=botoes[i].center, fontsize=40, color="black")

def on_mouse_down(pos):
    global pontuacao
    for i in range(4):
        if botoes[i].collidepoint(pos):
            if respostas[i] == resposta_certa:
                pontuacao += 1
            else:
                pontuacao -= 1 if pontuacao > 0 else 0
            nova_pergunta()
#[fim codigo]