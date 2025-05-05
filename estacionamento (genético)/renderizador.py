import pygame
import random
import os
import utils

pasta_assets = "assets/"

# Sorteia a imagem do estacionamento já renderizada com carros
pistas = [
    os.path.join(pasta_assets, arquivo)
    for arquivo in os.listdir(pasta_assets)
    if arquivo.startswith("estacionamento") and arquivo.endswith(".png")
]
estacionamento_escolhido = random.choice(pistas)

# Carrega a imagem
estacionamento_original = pygame.image.load(estacionamento_escolhido)

# Tamanho da tela
largura_tela = 1366
altura_tela = 700

# Tamanho da imagem original
largura_img, altura_img = estacionamento_original.get_size()

# Calcula escala proporcional
escala = min(largura_tela / largura_img, altura_tela / altura_img)
nova_largura = int(largura_img * escala)
nova_altura = int(altura_img * escala)

# Redimensiona imagem
estacionamento_escolhido_surface = pygame.transform.scale(estacionamento_original, (nova_largura, nova_altura))

# Offset para centralizar na tela
offset_x = 0
offset_y = (altura_tela - nova_altura) // 2

mapa_colisao = utils.gerar_mapa_colisao(estacionamento_escolhido_surface)

# Gera imagem visual com colisões marcadas
def gerar_debug_colisao(imagem, mapa, cor=(255, 0, 0)):
    debug_surface = imagem.copy()
    for y, linha in enumerate(mapa):
        for x, val in enumerate(linha):
            if val == 1:
                debug_surface.set_at((x, y), cor)
    return debug_surface

# No renderizador.py, depois de gerar o mapa_colisao:
estacionamento_debug_surface = gerar_debug_colisao(estacionamento_escolhido_surface, mapa_colisao)