import pygame
import math
import renderizador as r


from carro import Carro

carro = Carro(100, 100)
pista_atual = 0  # ✅ Adiciona esta linha aqui

# Inicializações específicas do main
pygame.init()
screen = pygame.display.set_mode((r.WIDTH, r.HEIGHT))
clock = pygame.time.Clock()


rodando = True
while rodando:
    dt = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    pista = r.pistas[pista_atual]
    matriz_logica = r.gerar_matriz_logica(pista)

    # Movimento do carro
    keys = pygame.key.get_pressed()
    carro.atualizar(keys)
    if carro.verificar_colisao(matriz_logica):
        carro.velocidade *= -0.3

    camera_offset_x = int(carro.x - r.WIDTH // 2)
    camera_offset_y = int(carro.y - r.HEIGHT // 2)

    r.desenhar_pista(pista, camera_offset_x, camera_offset_y)

    carro.desenhar(screen, camera_offset_x, camera_offset_y)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                pista_atual = 0
            elif event.key == pygame.K_2:
                pista_atual = 1

pygame.quit()
