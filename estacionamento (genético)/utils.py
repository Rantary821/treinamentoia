import pygame
import pygame.gfxdraw

REDE_X = 1050
REDE_Y = 20
REDE_LARGURA = 280
REDE_ALTURA = 300

def cor_por_valor(valor):
    valor = max(min(valor, 1), -1)
    if valor >= 0:
        return (int(255 * (1 - valor)), 255, int(255 * (1 - valor)))
    else:
        return (255, int(255 * (1 + valor)), int(255 * (1 + valor)))

def desenhar_rede(surface, rede, pesos, pos_x=1050, pos_y=20, largura=280, altura=300):
    raio = 10
    fonte = pygame.font.SysFont("arial", 10)

    num_camadas = len(rede)
    max_neuronios = max(len(c) for c in rede)

    espaco_horizontal = largura // (num_camadas + 1)
    espaco_vertical = altura // (max_neuronios + 1)

    posicoes = []

    # Conexões
    for camada_idx in range(num_camadas - 1):
        posicoes_camada_atual = []
        posicoes_camada_proxima = []

        for i in range(len(rede[camada_idx])):
            x = pos_x + (camada_idx + 1) * espaco_horizontal
            y = pos_y + (i + 1) * espaco_vertical
            posicoes_camada_atual.append((x, y))

        for j in range(len(rede[camada_idx + 1])):
            x = pos_x + (camada_idx + 2) * espaco_horizontal
            y = pos_y + (j + 1) * espaco_vertical
            posicoes_camada_proxima.append((x, y))

        for j, pos_prox in enumerate(posicoes_camada_proxima):
            for i, pos_atual in enumerate(posicoes_camada_atual):
                peso = pesos[camada_idx][j][i]
                cor = (0, 255, 0) if peso >= 0 else (255, 0, 0)
                espessura = max(1, int(abs(peso) * 5))
                pygame.draw.line(surface, cor, pos_atual, pos_prox, espessura)

    # Neurônios
    for camada_idx, camada in enumerate(rede):
        for i, valor in enumerate(camada):
            x = pos_x + (camada_idx + 1) * espaco_horizontal
            y = pos_y + (i + 1) * espaco_vertical
            cor = cor_por_valor(valor)

            pygame.draw.circle(surface, (0, 0, 0), (x, y), raio + 2)
            pygame.draw.circle(surface, cor, (x, y), raio)

            texto = fonte.render(f"{valor:.2f}", True, (255, 255, 255))
            rect = texto.get_rect(center=(x, y))
            surface.blit(texto, rect)

    # Segunda parte: desenhar neurônios com valores
    fonte = pygame.font.SysFont("arial", 12)

    for camada_idx, camada in enumerate(rede):
        num_neuronios = len(camada)
        #offset_y = (surface_height - (num_neuronios * espaco_vertical)) // 2

        for i, valor in enumerate(camada):
            x = pos_x + (camada_idx + 1) * espaco_horizontal
            y = pos_y + (i + 1) * espaco_vertical
            cor = cor_por_valor(valor)

            pygame.draw.circle(surface, (0, 0, 0), (x, y), raio + 2)
            pygame.draw.circle(surface, cor, (x, y), raio)

            texto = fonte.render(f"{valor:.2f}", True, (255, 255, 255))
            rect = texto.get_rect(center=(x, y))
            surface.blit(texto, rect)

            
def gerar_mapa_colisao(imagem_surface, cor_livre=(50, 50, 50), tolerancia=5):
    largura, altura = imagem_surface.get_size()
    mapa = []
    for y in range(altura):
        linha = []
        for x in range(largura):
            cor_pixel = imagem_surface.get_at((x, y))[:3]
            if any(abs(c - l) > tolerancia for c, l in zip(cor_pixel, cor_livre)):
                linha.append(1)  # 1 = colisão
            else:
                linha.append(0)  # 0 = livre
        mapa.append(linha)
    return mapa
