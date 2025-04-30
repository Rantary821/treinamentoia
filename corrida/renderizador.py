import pygame
import math

TILE_SIZE = 80
WIDTH, HEIGHT = 1280, 720

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
    ["up.png", None, None, None, None, None, "direitabaixo.png", "esquerdabaixo.png", None, None, None, "up.png"],
    ["up.png", None, "direitabaixo.png", "esquerdabaixo.png", None, None, "up.png", "cimadireita.png", "left.png", "left.png", "left.png", "cimaesquerda.png"],
    ["cimadireita.png", "esquerdabaixo.png", "up.png", "up.png", None, None, "up.png", None, "direitabaixo.png", "left.png", "left.png", "esquerdabaixo.png"],
    [None, "cimadireita.png", "cimaesquerda.png", "up.png", None, None, "up.png", None, "up.png", None, None, "up.png"],
    ["direitabaixo.png", "left.png.", "left.png", "cimaesquerda.png", None, None, "up.png", None, "up.png", None, None, "up.png"],
    ["up.png", None, None, None, None, None, "cimadireita.png", "left.png", "cimaesquerda.png", None, None, "up.png"],
    ["cimadireita.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "cimaesquerda.png"],
]

pistas = [PISTA_1, PISTA_2]
pista_atual = 0

# Inicializações
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Pistas")
clock = pygame.time.Clock()

# Parâmetros do carro
aceleracao = 0.4
vel_max = 10.5
vel_giro = 2.0

# Imagens e cache
tile_images = {}
carro_img_original = pygame.image.load("assets/audi.png")
carro_img = pygame.transform.scale(carro_img_original, (TILE_SIZE // 2, TILE_SIZE // 2))

# Surface usada para colisão
colisao_surface = None

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

def gerar_surface_mapa(pista):
    largura = len(pista[0]) * TILE_SIZE
    altura = len(pista) * TILE_SIZE
    mapa = pygame.Surface((largura, altura))
    mapa.fill((0, 0, 0))
    for y, linha in enumerate(pista):
        for x, tile in enumerate(linha):
            if tile:
                imagem = carregar_tile(tile)
                mapa.blit(imagem, (x * TILE_SIZE, y * TILE_SIZE))
    return mapa

def desenhar_pista(pista, offset_x, offset_y):
    global colisao_surface
    if colisao_surface:
        screen.blit(colisao_surface, (-offset_x, -offset_y))

def atualizar_surface_colisao(indice_pista):
    global pista_atual, colisao_surface
    pista_atual = indice_pista
    colisao_surface = gerar_surface_mapa(pistas[pista_atual])

def get_colisao_surface():
    return colisao_surface

# Checkpoints (opcional)
CHECKPOINTS_GRID = [
    (3, 0), (4, 4), (5, 6), (4, 7), (2, 7), (1, 5), (0, 2)
]

def gerar_checkpoints_pixel():
    return [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) for x, y in CHECKPOINTS_GRID]

# Inicializa a surface de colisão na primeira execução
atualizar_surface_colisao(pista_atual)

def gerar_matriz_logica(pista):
    return [[1 if cell else 0 for cell in row] for row in pista]
