import pygame
import renderizador as render
import utils
from ia.agente import criar_agente

mostrar_colisao = False

# Simulação de rede neural
rede_simulada = [
    [0.1, 0.2, 0.3],
    [0.4, -0.5, 0.6, 0.1],
    [0.9, -0.7]
]
pesos_simulados = [
    [
        [0.2, -0.1, 0.5],
        [0.3, 0.6, -0.2],
        [-0.4, 0.2, 0.1],
        [0.1, -0.3, 0.7]
    ],
    [
        [0.5, -0.2, 0.1, 0.3],
        [-0.6, 0.4, -0.1, 0.2]
    ]
]

pygame.init()
largura_tela = 1360
altura_tela = 700
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Estacionamento")

carro = criar_agente()

executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_c:
                mostrar_colisao = not mostrar_colisao
                print("Trocou!", mostrar_colisao)
    # --- Controle do carro (manual com setas) ---
    teclas = pygame.key.get_pressed()
    aceleracao = 0
    direcao = 0

    if teclas[pygame.K_UP]:
        aceleracao = 0.2
    elif teclas[pygame.K_DOWN]:
        aceleracao = -0.2
    if teclas[pygame.K_LEFT]:
        direcao = -1
    elif teclas[pygame.K_RIGHT]:
        direcao = 1

    carro.atualizar(aceleracao, direcao)
    carro.atualizar_sensores(render.mapa_colisao)

    # --- Renderização ---
    if mostrar_colisao:
        tela.blit(render.estacionamento_debug_surface, (render.offset_x, render.offset_y))
    else:
        tela.blit(render.estacionamento_escolhido_surface, (render.offset_x, render.offset_y))

    carro.desenhar(tela, render.offset_x, render.offset_y, mostrar_sensores=True)

    utils.desenhar_rede(tela, rede_simulada, pesos_simulados,
                        pos_x=1050, pos_y=20, largura=280, altura=300)

    pygame.display.flip()

pygame.quit()