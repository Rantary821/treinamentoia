import pygame
import math
import renderizador as r
from carro import Carro
from carro_ia import CarroIA, CHECKPOINTS
from genetica import Populacao
from renderizador import CHECKPOINTS_GRID, TILE_SIZE
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

import time
font = pygame.font.SysFont("Arial", 24)
tempo_inicio = time.time()

# Inicializações
pygame.init()
screen = pygame.display.set_mode((r.WIDTH, r.HEIGHT))
clock = pygame.time.Clock()

# Estado do jogo
pista_atual = 0
surface_colisao = r.gerar_surface_mapa(r.pistas[pista_atual])
pop = Populacao(tamanho=50)
carros = [CarroIA(50, 50, ind) for ind in pop.individuos]
for carro in carros:
    carro.angle = -90  # apontando para a direita, por exemplo
carro_manual = Carro(50, 50)
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
def desenhar_botao_reiniciar():
    largura = 160
    altura = 40
    margem = 20
    rect = pygame.Rect(r.WIDTH - largura - margem, margem, largura, altura)
    pygame.draw.rect(screen, (200, 50, 50), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    txt = font.render("REINICIAR", True, (255, 255, 255))
    screen.blit(txt, (rect.x + 20, rect.y + 10))
    return rect

historico_melhor = []
historico_media = []
rodando = True
while rodando:
    dt = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    pista = r.pistas[pista_atual]
    surface_colisao = r.gerar_surface_mapa(pista)
    #matriz_logica = r.gerar_matriz_logica(pista)

    if usar_carro_manual:
        keys = pygame.key.get_pressed()
        carro_manual.atualizar(keys)
        if carro_manual.verificar_colisao(surface_colisao):
            carro_manual.velocidade *= -0.3

        camera_offset_x = int(carro_manual.x - r.WIDTH // 2)
        camera_offset_y = int(carro_manual.y - r.HEIGHT // 2)

        screen.blit(r.get_colisao_surface(), (-camera_offset_x, -camera_offset_y))
        carro_manual.desenhar(screen, camera_offset_x, camera_offset_y)



        for origem, destino in carro_manual.calcular_sensores(surface_colisao):
            origem_tela = (origem[0] - camera_offset_x, origem[1] - camera_offset_y)
            destino_tela = (destino[0] - camera_offset_x, destino[1] - camera_offset_y)
            distancia = math.hypot(destino[0] - origem[0], destino[1] - origem[1])
            cor = (255, 0, 0) if distancia < 180 else (0, 255, 0)
            pygame.draw.line(screen, cor, origem_tela, destino_tela, 2)
            pygame.draw.circle(screen, (255, 255, 0), destino_tela, 4)

    else:
        vivos = 0
        if carros:
            map_width = len(r.pistas[r.pista_atual][0]) * r.TILE_SIZE
            map_height = len(r.pistas[r.pista_atual]) * r.TILE_SIZE
            camera_offset_x = map_width // 2 - r.WIDTH // 2
            camera_offset_y = map_height // 2 - r.HEIGHT // 2
        else:
            camera_offset_x = 0
            camera_offset_y = 0

        screen.blit(r.get_colisao_surface(), (-camera_offset_x, -camera_offset_y))

        for carro in carros:
            if carro.vivo:
                carro.atualizar_com_ia(surface_colisao)
                carro.verificar_estado(surface_colisao)
                vivos += 1

            carro.desenhar(screen, camera_offset_x, camera_offset_y)

            for origem, destino in carro.calcular_sensores(surface_colisao):
                origem_tela = (origem[0] - camera_offset_x, origem[1] - camera_offset_y)
                destino_tela = (destino[0] - camera_offset_x, destino[1] - camera_offset_y)
                pygame.draw.line(screen, (255, 0, 0), origem_tela, destino_tela, 1)
                pygame.draw.circle(screen, (255, 255, 0), destino_tela, 2)

        if vivos == 0:
            pop.evoluir()
            carros = [CarroIA(50, 50, ind) for ind in pop.individuos]
            for carro in carros:
                carro.angle = -90  # apontando para a direita, por exemplo
            melhor_fitness = max(ind.fitness for ind in pop.individuos)
            media_fitness = sum(ind.fitness for ind in pop.individuos) / len(pop.individuos)
            historico_melhor.append(melhor_fitness)
            historico_media.append(media_fitness)


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
            minutos = tempo_segundos // 60
            segundos = tempo_segundos % 60
            tempo_formatado = f"{minutos:02d}:{segundos:02d}"  # ex: 03:47
            texto2 = font.render(f"Tempo: {tempo_formatado}", True, (255, 255, 0))
            screen.blit(texto1, (20, 70))
            screen.blit(texto2, (20, 100))
            total = len(pop.individuos)
            vivos = sum(1 for i in pop.individuos if hasattr(i, 'vivo') and i.vivo)
            vivos = sum(1 for c in carros if c.vivo)
            texto3 = font.render(f"População: {total}", True, (0, 200, 255))
            texto4 = font.render(f"Vivos: {vivos}", True, (0, 255, 0))

            screen.blit(texto3, (20, 130))
            screen.blit(texto4, (20, 160))
    botao_rect = desenhar_botao()
    botao_reiniciar_rect = desenhar_botao_reiniciar()
    pygame.display.flip()

    
    #fig, ax = plt.subplots()
    #linha_melhor, = ax.plot([], [], label="Melhor")
    #linha_media, = ax.plot([], [], label="Média")
    #ax.set_title("Desempenho por Geração")
    #ax.set_xlabel("Geração")
    #ax.set_ylabel("Fitness")
    #ax.legend()

    #def atualizar_grafico(frame):
    #    linha_melhor.set_data(range(len(historico_melhor)), historico_melhor)
    #    linha_media.set_data(range(len(historico_media)), historico_media)
    #    ax.relim()
    #    ax.autoscale_view()
    #    return linha_melhor, linha_media
    #

    #ani = animation.FuncAnimation(fig, atualizar_grafico, interval=1000)
    #plt.show(block=False)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
             pista_atual = 0
             r.surface_colisao = r.gerar_surface_mapa(r.pistas[pista_atual])
             r.matriz_logica = r.gerar_matriz_logica(r.pistas[pista_atual])
             r.atualizar_surface_colisao(pista_atual)  # <== GARANTIR ISSO
            elif event.key == pygame.K_2:
                pista_atual = 1
                r.surface_colisao = r.gerar_surface_mapa(r.pistas[pista_atual])
                r.matriz_logica = r.gerar_matriz_logica(r.pistas[pista_atual])
                r.atualizar_surface_colisao(pista_atual)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if botao_rect.collidepoint(event.pos):
                usar_carro_manual = not usar_carro_manual
                carro_manual = Carro(50, 50)
            elif botao_reiniciar_rect.collidepoint(event.pos):
                pop.evoluir()
                carros = [CarroIA(50, 50, ind) for ind in pop.individuos]
                for carro in carros:
                    carro.angle = -90  # ou qualquer direção inicial desejada

pygame.quit()
