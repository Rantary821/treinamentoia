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
        #Definindo sensores
        self.angulos_sensores = [i for i in range(0, 360, 360 // 16)]  # 16 sensores circulares

    def atualizar(self, keys):
        # Atualiza aceleração
        if keys[pygame.K_UP]:
            self.velocidade = min(r.vel_max, self.velocidade + r.aceleracao)
        elif keys[pygame.K_DOWN]:
            self.velocidade = max(-r.vel_max / 2, self.velocidade - r.aceleracao)
        else:
            self.velocidade *= 0.95
    
        # Somente gira se estiver em movimento
        if abs(self.velocidade) > 0.5:
            if keys[pygame.K_LEFT]:
                self.angle += r.vel_giro
            if keys[pygame.K_RIGHT]:
                self.angle -= r.vel_giro
    
        # Aplica movimento
        rad = math.radians(self.angle)
        dx = -self.velocidade * math.sin(rad)
        dy = -self.velocidade * math.cos(rad)
        self.x += dx
        self.y += dy

    def verificar_colisao(self, surface_colisao):
        x_int = int(self.x)
        y_int = int(self.y)

        if 0 <= x_int < surface_colisao.get_width() and 0 <= y_int < surface_colisao.get_height():
            cor = surface_colisao.get_at((x_int, y_int))[:3]  # Pega RGB
            return cor == (0, 0, 0)  # Colide se for preto
        return True  # Fora dos limites = colisão

    def desenhar(self, screen, offset_x, offset_y):
        rot = pygame.transform.rotate(self.img, self.angle)
        rect = rot.get_rect(center=(self.x - offset_x, self.y - offset_y))
        screen.blit(rot, rect.topleft)

    def calcular_sensores(self, surface_colisao, range_max=800, step=5):
        sensores = []
        for ang in self.angulos_sensores:
            total_angle = math.radians(self.angle + ang)
            for dist in range(0, range_max, step):
                sx = self.x + dist * math.cos(total_angle)
                sy = self.y - dist * math.sin(total_angle)
    
                x_int = int(sx)
                y_int = int(sy)
    
                if (0 <= x_int < surface_colisao.get_width()) and (0 <= y_int < surface_colisao.get_height()):
                    cor = surface_colisao.get_at((x_int, y_int))[:3]  # ignora alfa
                    if cor == (0, 0, 0):  # colidiu com preto (borda da pista)
                        sensores.append(((self.x, self.y), (sx, sy)))
                        break
                else:
                    sensores.append(((self.x, self.y), (sx, sy)))
                    break
            else:
                sensores.append(((self.x, self.y), (sx, sy)))
        return sensores