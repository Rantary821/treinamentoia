import pygame
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Corrida")
clock = pygame.time.Clock()

# Carregando imagens
pista = pygame.image.load("assets/pista.png")
carro_img = pygame.image.load("assets/carro.png")
carro_img = pygame.transform.scale(carro_img, (50, 100))

# Estado do carro
carro_x = WIDTH // 2 - 25
carro_y = HEIGHT - 120
velocidade = 0
angulo = 0

def desenhar_jogo():
    screen.blit(pista, (0, 0))
    carro_rotacionado = pygame.transform.rotate(carro_img, angulo)
    carro_rect = carro_rotacionado.get_rect(center=(carro_x, carro_y))
    screen.blit(carro_rotacionado, carro_rect.topleft)

    pygame.display.flip()

# Loop principal
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Teclado
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angulo += 3
    if keys[pygame.K_RIGHT]:
        angulo -= 3
    if keys[pygame.K_UP]:
        velocidade = 5
    elif keys[pygame.K_DOWN]:
        velocidade = -3
    else:
        velocidade = 0

    # Movimentação
    rad = -angulo * 3.14 / 180
    carro_x += velocidade * pygame.math.Vector2(1, 0).rotate(-angulo).x
    carro_y += velocidade * pygame.math.Vector2(1, 0).rotate(-angulo).y

    desenhar_jogo()