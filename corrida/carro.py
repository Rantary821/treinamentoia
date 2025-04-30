import pygame
import math
import renderizador as r

class Carro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0.0
        self.velocidade = 0.0
        self.img = pygame.transform.scale(r.carro_img_original, (r.TILE_SIZE // 2, r.TILE_SIZE // 2))

    def atualizar(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += r.vel_giro
        if keys[pygame.K_RIGHT]:
            self.angle -= r.vel_giro
        if keys[pygame.K_UP]:
            self.velocidade = min(r.vel_max, self.velocidade + r.aceleracao)
        elif keys[pygame.K_DOWN]:
            self.velocidade = max(-r.vel_max / 2, self.velocidade - r.aceleracao)
        else:
            self.velocidade *= 0.95

        rad = math.radians(self.angle)
        dx = -self.velocidade * math.sin(rad)
        dy = -self.velocidade * math.cos(rad)
        self.x += dx
        self.y += dy

    def verificar_colisao(self, matriz_logica):
        col = int(self.x // r.TILE_SIZE)
        lin = int(self.y // r.TILE_SIZE)
        if 0 <= lin < len(matriz_logica) and 0 <= col < len(matriz_logica[0]):
            return matriz_logica[lin][col] == 0
        return True

    def desenhar(self, screen, offset_x, offset_y):
        rot = pygame.transform.rotate(self.img, self.angle)
        rect = rot.get_rect(center=(self.x - offset_x, self.y - offset_y))
        screen.blit(rot, rect.topleft)
