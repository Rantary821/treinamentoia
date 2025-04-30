import pygame
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def desenhar_rede_neural(screen, entradas, ocultos, saidas, pesos_ih=None, pesos_ho=None, pos_x=1020, pos_y=80):
    raio = 10
    espaco_y = 50
    offset_x = 80

    font = pygame.font.SysFont("Arial", 18)

    pos_entrada = [(pos_x, pos_y + i * espaco_y) for i in range(len(entradas))]
    pos_oculta  = [(pos_x + offset_x, pos_y + i * espaco_y) for i in range(len(ocultos))]
    pos_saida   = [(pos_x + offset_x * 2, pos_y + i * espaco_y * 2) for i in range(len(saidas))]

    # Linhas entrada -> oculta
    for i, (x1, y1) in enumerate(pos_entrada):
        for j, (x2, y2) in enumerate(pos_oculta):
            peso = pesos_ih[j][i] if pesos_ih else 0
            cor = (0, 200, 0) if peso >= 0 else (200, 0, 0)
            largura = max(1, int(abs(peso) * 3)) if pesos_ih else 1
            pygame.draw.line(screen, cor, (x1 + 20, y1 + 10), (x2, y2 + 10), largura)

    # Linhas oculta -> saída
    for i, (x1, y1) in enumerate(pos_oculta):
        for j, (x2, y2) in enumerate(pos_saida):
            peso = pesos_ho[j][i] if pesos_ho else 0
            cor = (0, 200, 0) if peso >= 0 else (200, 0, 0)
            largura = max(1, int(abs(peso) * 3)) if pesos_ho else 1
            pygame.draw.line(screen, cor, (x1 + 20, y1 + 10), (x2, y2 + 10), largura)

    # Entrada
    # Labels das entradas (ajuste conforme seus inputs)
    labels_entrada = [
        "Posição Y",
        "Vel. Y",
        "Dist. obst.",
        "Está no chão",
        "Bias"
    ]
    
    for i, val in enumerate(entradas):
        x, y = pos_entrada[i]
        pygame.draw.rect(screen, (0, 0, 255), (x, y, 20, 20))
    
        txt_val = font.render(f"{val:.2f}", True, (0, 0, 0))
        txt_label = font.render(labels_entrada[i], True, (0, 0, 0))
    
        screen.blit(txt_val, (x - 40, y))
        screen.blit(txt_label, (x - 130, y))

    # Oculta
    for i in range(len(ocultos)):
        x, y = pos_oculta[i]
        pygame.draw.polygon(screen, (255, 165, 0), [
            (x, y + 10), (x + 10, y), (x + 20, y + 10), (x + 10, y + 20)
        ])

    # Saída
    labels = ['Pular', 'Nada']
    for i, (val, label) in enumerate(zip(saidas, labels)):
        x, y = pos_saida[i]
        cor = (0, 255, 0) if val > 0.5 else (255, 0, 0)
        pygame.draw.circle(screen, cor, (x + 10, y + 10), raio)
        txt = font.render(f"{label}: {val:.2f}", True, (0, 0, 0))
        screen.blit(txt, (x + 25, y))

def desenhar_cabecalho(screen, geracao, score, tempo_str, pos_x=1020):
    font = pygame.font.SysFont("Arial", 22)
    txt1 = font.render(f"Geração: {geracao}", True, (0, 0, 0))
    txt2 = font.render(f"Score: {score}", True, (0, 0, 0))
    txt3 = font.render(f"Tempo: {tempo_str}", True, (0, 0, 0))
    screen.blit(txt1, (pos_x, 10))
    screen.blit(txt2, (pos_x, 35))
    screen.blit(txt3, (pos_x, 60))

def desenhar_grafico_evolucao(screen, lista_scores, pos_x=1020, pos_y=380, largura=260, altura=80):
    if len(lista_scores) < 2:
        return

    max_score = max(lista_scores)
    escala = altura / (max_score + 1)

    for i in range(1, len(lista_scores)):
        x1 = pos_x + int((i - 1) * (largura / len(lista_scores)))
        y1 = pos_y + altura - int(lista_scores[i - 1] * escala)
        x2 = pos_x + int(i * (largura / len(lista_scores)))
        y2 = pos_y + altura - int(lista_scores[i] * escala)
        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

    pygame.draw.rect(screen, (0, 0, 0), (pos_x, pos_y, largura, altura), 1)
