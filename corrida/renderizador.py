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

rodando = True

while rodando:
    dt = clock.tick(60) / 1000.0
    screen.fill((30, 30, 30))

    pista = pistas[pista_atual]
    matriz_logica = gerar_matriz_logica(pista)

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
    proximo_x = carro_x + (-carro_vel * math.sin(rad))
    proximo_y = carro_y + (-carro_vel * math.cos(rad))

    if verificar_colisao(matriz_logica, proximo_x, proximo_y):
        carro_vel *= -0.3  # bate e quica
    else:
        carro_x = proximo_x
        carro_y = proximo_y

    # Atualiza câmera para seguir o carro
    camera_offset_x = int(carro_x - WIDTH // 2)
    camera_offset_y = int(carro_y - HEIGHT // 2)

    desenhar_pista(pista, camera_offset_x, camera_offset_y)

    carro_rot = pygame.transform.rotate(carro_img, carro_angle)
    rect = carro_rot.get_rect(center=(carro_x - camera_offset_x, carro_y - camera_offset_y))
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
