import pygame
import math

TILE_SIZE = 100
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
    ["direitabaixo.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "left.png", "esquerdabaixo.png"] * 3
] * 20

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador de Pistas")
clock = pygame.time.Clock()

# Cache de imagens
tile_images = {}
carro_img_original = pygame.image.load("assets/audi.png")
carro_img = pygame.transform.scale(carro_img_original, (TILE_SIZE // 2, TILE_SIZE // 2))

# Carro com movimento real
carro_x = 100.0
carro_y = 100.0
carro_vel = 0.0
carro_angle = 0.0
aceleracao = 0.4
vel_max = 6.5
vel_giro = 3.0

camera_offset_x = 0
camera_offset_y = 0

pistas = [PISTA_1, PISTA_2]
pista_atual = 0

# Gera matriz lógica da pista (1 = pista, 0 = fora)
def gerar_matriz_logica(pista):
    return [[1 if cell else 0 for cell in row] for row in pista]

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

def desenhar_pista(matriz, offset_x, offset_y):
    for y, linha in enumerate(matriz):
        for x, nome_tile in enumerate(linha):
            if nome_tile:
                imagem = carregar_tile(nome_tile)
                screen.blit(imagem, (x * TILE_SIZE - offset_x, y * TILE_SIZE - offset_y))

def verificar_colisao(matriz_logica, carro_x, carro_y):
    col = int(carro_x // TILE_SIZE)
    lin = int(carro_y // TILE_SIZE)
    if 0 <= lin < len(matriz_logica) and 0 <= col < len(matriz_logica[0]):
        return matriz_logica[lin][col] == 0
    return True  # fora da pista = colisão

# Checkpoints definidos manualmente na ordem certa (col, lin)
CHECKPOINTS_GRID = [
    #(1, 0),  # início da reta
    (3, 0),  # fim da reta horizontal
    (4, 4),  # meio da descida
    (5, 6),  # fim da descida
    (4, 7),  # curva para a direita
    (2, 7),  # fim da reta à direita
    (1, 5),  # fim da reta à direita
    (0, 2),  # fim da reta à direita
]

# Converte posições de grid para coordenadas absolutas (centro do tile)
def gerar_checkpoints_pixel():
    return [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) for x, y in CHECKPOINTS_GRID]