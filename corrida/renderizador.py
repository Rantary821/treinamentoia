import pygame
import math

TILE_SIZE = 100
GRID_WIDTH = 12
GRID_HEIGHT = 8
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE

# Define manualmente duas pistas como matrizes
PISTA_1 = [
    ["direitabaixo.png", "left.png", "left.png", "esquerdabaixo.png", None, None, None, None, None, None, None, None],
    ["up.png", None, None, "up.png", None, None, None, None, None, None, None, None],
    ["up.png", None, None, "up.png", None, None, None, None, None, None, None, None],
    ["up.png", None, None, "up.png", None, None, None, None, None, None, None, None],
    ["cimadireita.png", "esquerdabaixo.png", None, "cimadireita.png", "left.png", "esquerdabaixo.png", None, None, None, None, None, None],
    [None, "up.png", None, None, None, "up.png", None, None, None, None, None, None],
    [None, "up.png", None, None, None, "up.png", None, None, None, None, None, None],
    [None, "cimadireita.png", "left.png", "left.png", "left.png", "cimaesquerda.png", None, None, None, None, None, None],
]

PISTA_2 = [
    ["direitabaixo.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "esquerdabaixo.png"],
    ["up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png"],
    ["cimadireita.png", "left.png", "cimaesquerda.png", "cimadireita.png", "left.png", "cimaesquerda.png", "cimadireita.png", "left.png", "cimaesquerda.png", "cimadireita.png", "left.png", "cimaesquerda.png"],
    ["up.png", "up.png", "direitabaixo.png", "up.png", "up.png", "direitabaixo.png", "up.png", "up.png", "direitabaixo.png", "up.png", "up.png", "up.png"],
    ["up.png", "up.png", "cimadireita.png", "left.png", "left.png", "cimaesquerda.png", "cimadireita.png", "left.png", "left.png", "cimaesquerda.png", "up.png", "up.png"],
    ["up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png"],
    ["up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png", "up.png"],
    ["cimadireita.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "cimaesquerda.png"],
]

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Pistas")
clock = pygame.time.Clock()

# Cache de imagens
tile_images = {}
carro_img_original = pygame.image.load("assets/audi.png")
carro_img = pygame.transform.scale(carro_img_original, (TILE_SIZE, TILE_SIZE))

# Carro com movimento real
carro_x = 100.0
carro_y = 100.0
carro_vel = 0.0
carro_angle = 0.0
aceleracao = 0.3
vel_max = 4.5
vel_giro = 3.0

pistas = [PISTA_1, PISTA_2]
pista_atual = 0

def carregar_tile(nome):
    if nome not in tile_images:
        try:
            tile_images[nome] = pygame.transform.scale(
                pygame.image.load(f"assets/tiles/{nome}"), (TILE_SIZE, TILE_SIZE))
        except:
            erro = pygame.Surface((TILE_SIZE, TILE_SIZE))
            erro.fill((255, 0, 255))
            tile_images[nome] = erro
    return tile_images[nome]

def desenhar_pista(matriz):
    for y, linha in enumerate(matriz):
        for x, nome_tile in enumerate(linha):
            if nome_tile:
                imagem = carregar_tile(nome_tile)
                screen.blit(imagem, (x * TILE_SIZE, y * TILE_SIZE))

rodando = True
while rodando:
    dt = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    pista = pistas[pista_atual]
    desenhar_pista(pista)

    # Movimento do carro
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        carro_angle += vel_giro
    if keys[pygame.K_RIGHT]:
        carro_angle -= vel_giro
    if keys[pygame.K_UP]:
        carro_vel = min(vel_max, carro_vel + aceleracao)
    elif keys[pygame.K_DOWN]:
        carro_vel = max(-vel_max / 2, carro_vel - aceleracao)
    else:
        carro_vel *= 0.95

    rad = math.radians(carro_angle)
    carro_x += -carro_vel * math.sin(rad)
    carro_y += -carro_vel * math.cos(rad)

    carro_rot = pygame.transform.rotate(carro_img, carro_angle)
    rect = carro_rot.get_rect(center=(carro_x, carro_y))
    screen.blit(carro_rot, rect.topleft)

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