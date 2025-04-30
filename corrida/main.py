import pygame
import math
import renderizador as r
from carro import Carro
from carro_ia import CarroIA, CHECKPOINTS
from genetica import Populacao
from renderizador import CHECKPOINTS_GRID, TILE_SIZE

import time
font = pygame.font.SysFont("Arial", 24)
tempo_inicio = time.time()

# Inicializações
pygame.init()
screen = pygame.display.set_mode((r.WIDTH, r.HEIGHT))
clock = pygame.time.Clock()

# Estado do jogo
pista_atual = 0
pop = Populacao(tamanho=30)
carros = [CarroIA(100, 100, ind) for ind in pop.individuos]
carro_manual = Carro(100, 100)
usar_carro_manual = False

font = pygame.font.SysFont(None, 30)
def desenhar_botao():
    cor = (50, 200, 50) if not usar_carro_manual else (200, 50, 50)
    texto = "JOGAR MANUAL" if not usar_carro_manual else "SIMULAÇÃO IA"
    rect = pygame.Rect(10, 10, 160, 40)
    pygame.draw.rect(screen, cor, rect)
    pygame.draw.rect(screen, (255,255,255), rect, 2)
    txt = font.render(texto, True, (255,255,255))
    screen.blit(txt, (20, 20))
    return rect

rodando = True
while rodando:
    dt = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    pista = r.pistas[pista_atual]
    matriz_logica = r.gerar_matriz_logica(pista)

    if usar_carro_manual:
        keys = pygame.key.get_pressed()
        carro_manual.atualizar(keys)
        if carro_manual.verificar_colisao(matriz_logica):
            carro_manual.velocidade *= -0.3

        camera_offset_x = int(carro_manual.x - r.WIDTH // 2)
        camera_offset_y = int(carro_manual.y - r.HEIGHT // 2)

        r.desenhar_pista(pista, camera_offset_x, camera_offset_y)
        carro_manual.desenhar(screen, camera_offset_x, camera_offset_y)

        for origem, destino in carro_manual.calcular_sensores(matriz_logica):
            origem_tela = (origem[0] - camera_offset_x, origem[1] - camera_offset_y)
            destino_tela = (destino[0] - camera_offset_x, destino[1] - camera_offset_y)
            distancia = math.hypot(destino[0] - origem[0], destino[1] - origem[1])
            cor = (255, 0, 0) if distancia < 180 else (0, 255, 0)
            pygame.draw.line(screen, cor, origem_tela, destino_tela, 2)
            pygame.draw.circle(screen, (255, 255, 0), destino_tela, 4)

    else:
        vivos = 0
        if carros:
            camera_offset_x = int(carros[0].x - r.WIDTH // 2)
            camera_offset_y = int(carros[0].y - r.HEIGHT // 2)
        else:
            camera_offset_x = 0
            camera_offset_y = 0

        r.desenhar_pista(pista, camera_offset_x, camera_offset_y)

        for carro in carros:
            if carro.vivo:
                carro.atualizar_com_ia(matriz_logica)
                carro.verificar_estado(matriz_logica)
                vivos += 1

            carro.desenhar(screen, camera_offset_x, camera_offset_y)

            for origem, destino in carro.calcular_sensores(matriz_logica):
                origem_tela = (origem[0] - camera_offset_x, origem[1] - camera_offset_y)
                destino_tela = (destino[0] - camera_offset_x, destino[1] - camera_offset_y)
                pygame.draw.line(screen, (255, 0, 0), origem_tela, destino_tela, 1)
                pygame.draw.circle(screen, (255, 255, 0), destino_tela, 2)

        if vivos == 0:
            pop.evoluir()
            carros = [CarroIA(100, 100, ind) for ind in pop.individuos]

    botao_rect = desenhar_botao()
      # Desenha checkpoints (modo IA)
    if not usar_carro_manual:
        for col, lin in CHECKPOINTS_GRID:
            cx = col * TILE_SIZE + TILE_SIZE // 2
            cy = lin * TILE_SIZE + TILE_SIZE // 2
            pygame.draw.circle(screen, (0, 200, 255), (cx - camera_offset_x, cy - camera_offset_y), 10)
            pygame.draw.circle(screen, (0, 255, 0), (cx - camera_offset_x, cy - camera_offset_y), 50, 1)
            # Tempo decorrido
            tempo_segundos = int(time.time() - tempo_inicio)

            # Desenha HUD com geração e tempo
            texto1 = font.render(f"Geração: {pop.geracao}", True, (255, 255, 255))
            texto2 = font.render(f"Tempo: {tempo_segundos}s", True, (255, 255, 0))
            screen.blit(texto1, (20, 70))
            screen.blit(texto2, (20, 100))
            total = len(pop.individuos)
            vivos = sum(1 for i in pop.individuos if hasattr(i, 'vivo') and i.vivo)
            
            texto3 = font.render(f"População: {total}", True, (0, 200, 255))
            texto4 = font.render(f"Vivos: {vivos}", True, (0, 255, 0))
            
            screen.blit(texto3, (20, 130))
            screen.blit(texto4, (20, 160))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if botao_rect.collidepoint(event.pos):
                usar_carro_manual = not usar_carro_manual
                carro_manual = Carro(100, 100)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                pista_atual = 0
            elif event.key == pygame.K_2:
                pista_atual = 1

pygame.quit()
