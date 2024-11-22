import pygame
import sys
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Inicializa o jogo usando Pygame
pygame.init()

# Configurações da tela (1200x600)
largura, altura = 1200, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Calculadora de Função Quadrática")

# Cores usadas (Preto e Branco)
preto = (0, 0, 0)
branco = (255, 255, 255)

# Efeitos de flocos de neve / Snowfall
flocos = [{'x': random.randint(0, largura), 'y': random.randint(0, altura), 'alpha': random.randint(50, 150), 'velocidade': random.uniform(0.1, 0.3)} for _ in range(50)]

# Função para desenhar os flocos de neve
def desenhar_flocos():
    for floco in flocos:
        floco['y'] += floco['velocidade']
        if floco['y'] > altura:
            floco['y'] = 0
            floco['x'] = random.randint(0, largura)
        superficie_floco = pygame.Surface((6, 6), pygame.SRCALPHA)
        pygame.draw.circle(superficie_floco, (255, 255, 255, floco['alpha']), (3, 3), 3)
        tela.blit(superficie_floco, (floco['x'], floco['y']))

# Função para calcular as raízes da equação quadrática usando formula de bhaskara
def calcular_raizes(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return None, None
    elif delta == 0:
        x1 = x2 = -b / (2 * a)
        return x1, x2
    else:
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        return x1, x2

# Função para desenhar a tela de entrada usada pelo jogo
def tela_entrada(mensagem_extra=""):
    tela.fill(preto)
    desenhar_flocos()
    fonte = pygame.font.Font(None, 36)
    mensagem = "Heya, por favorzinho digite os coeficientes A, B e C da função quadrática:"
    mensagem_texto = fonte.render(mensagem, True, branco)
    tela.blit(mensagem_texto, (50, 50))
    if mensagem_extra:
        entrada_texto = fonte.render(mensagem_extra, True, branco)
        tela.blit(entrada_texto, (50, 150))
    pygame.display.flip()

# Função para desenhar a tela de resultado usado pelo jogo
def tela_resultado(a, b, c, x1, x2):
    tela.fill(preto)
    desenhar_flocos()
    fonte = pygame.font.Font(None, 36)
    if x1 is None or x2 is None:
        resultado = f'A função quadrática {a}x² + {b}x + {c} não tem raízes reais.'
    else:
        resultado = f'As raízes da função {a}x² + {b}x + {c} são:\n x1 = {x1:.2f} e x2 = {x2:.2f}.'
    resultado_texto = [fonte.render(linha, True, branco) for linha in resultado.split('\n')]
    for i, linha in enumerate(resultado_texto):
        tela.blit(linha, (50, 150 + i * 40))
    instrucoes_texto = fonte.render("Pressione Espaço para fechar o programa", True, branco)
    tela.blit(instrucoes_texto, (50, 50))
    pygame.display.flip()

    # Desenhar o gráfico da função quadrática usando a, b, c, x1, x2
    desenhar_grafico(a, b, c, x1, x2)
    
    # Esperar que o usuário pressione a barra de espaço para fechar o programa
    esperar_ate_espaco()

# Função para desenhar o gráfico da função quadrática utilizando fig, plot, axhline
def desenhar_grafico(a, b, c, x1, x2):
    fig, ax = plt.subplots()
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    ax.plot(x, y, label=f'{a}x² + {b}x + {c}')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.legend()
    
    # Adicionar as raízes ao gráfico caso exista, utilizando as funções do Canva (NÃO É O APLICATIVO) 
    if x1 is not None and x2 is not None:
        ax.plot(x1, 0, 'ro')
        ax.plot(x2, 0, 'ro')
        ax.text(x1, 0, f'x1={x1:.2f}', color='red', fontsize=12, ha='left')
        ax.text(x2, 0, f'x2={x2:.2f}', color='red', fontsize=12, ha='left')

    canvas = FigureCanvas(fig)
    canvas.draw()
    raw_data = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    raw_data = raw_data.reshape(canvas.get_width_height()[::-1] + (3,))

    # Atualizador de gráfico da tela do Pygame
    surf = pygame.surfarray.make_surface(raw_data) 
    surf = pygame.transform.scale(surf, (400, 400)) # Ajustar tamanho do gráfico 
    surf = pygame.transform.rotate(surf, 90)
    surf = pygame.transform.flip(surf, False, True) # Inverter horizontalmente 
    tela.blit(surf, (650, 200)) # Ajustar a posição do gráfico na tela 
    pygame.display.flip()

    plt.close(fig)  # Fecha as figuras para liberar memória

# Função para esperar que o usuário pressione Espaço para sair do jogo
def esperar_ate_espaco():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pygame.quit()
                    sys.exit()

# Def main principal do jogo
def main():
    coeficientes = {'a': None, 'b': None, 'c': None}
    entrada = ""
    coef_atual = 'a'
    while coef_atual:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    try:
                        if coef_atual == 'a':
                            coeficientes['a'] = int(entrada)
                            coef_atual = 'b'
                        elif coef_atual == 'b':
                            coeficientes['b'] = int(entrada)
                            coef_atual = 'c'
                        elif coef_atual == 'c':
                            coeficientes['c'] = int(entrada)
                            coef_atual = None
                        entrada = ""
                    except ValueError:
                        entrada = ""
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                else:
                    entrada += evento.unicode

        tela_entrada(f'Digite o coeficiente {coef_atual}: {entrada}')

    a, b, c = coeficientes['a'], coeficientes['b'], coeficientes['c']
    x1, x2 = calcular_raizes(a, b, c)
    tela_resultado(a, b, c, x1, x2)

if __name__ == "__main__":
    main()