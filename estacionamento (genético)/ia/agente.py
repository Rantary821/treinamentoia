import pygame
import math

class Sensor:
    def __init__(self, angulo_relativo, max_distancia):
        self.angulo_relativo = angulo_relativo
        self.max_distancia = max_distancia
        self.valor = 0
        self.ponto_final = (0, 0)
        self.origem = (0, 0)

    def calcular(self, x, y, angulo_global, mapa_colisao, escala=1.0):
        self.origem = (x, y)
        rad = math.radians(angulo_global)
        for d in range(self.max_distancia):
            sx = int(x + math.cos(rad) * d * escala)
            sy = int(y + math.sin(rad) * d * escala)
            if sy < 0 or sy >= len(mapa_colisao) or sx < 0 or sx >= len(mapa_colisao[0]):
                self.valor = d / self.max_distancia
                self.ponto_final = (sx, sy)
                return
            if mapa_colisao[sy][sx] == 1:
                self.valor = d / self.max_distancia
                self.ponto_final = (sx, sy)
                return
        self.valor = 1.0
        self.ponto_final = (sx, sy)

class Agente:
    def __init__(self, x, y, imagem_path, escala=1.0):
        self.x = x
        self.y = y
        self.velocidade = 0
        self.angulo = 0
        self.escala = escala

        original = pygame.image.load(imagem_path).convert_alpha()
        self.largura = int(original.get_width() * escala)
        self.altura = int(original.get_height() * escala)
        self.imagem_original = pygame.transform.scale(original, (self.largura, self.altura))
        self.imagem = self.imagem_original
        self.rect = self.imagem.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.imagem_original)

        self.sensores = [
            Sensor(0, 200),     # frente
            Sensor(-48, 200),   # frente esquerda
            Sensor(45, 200),    # frente direita
            Sensor(-90, 200),    # lado esquerdo
            Sensor(90, 200),     # lado direito
        ]

    def get_ponto_rotacionado(self, offset_x, offset_y):
        rad = math.radians(self.angulo)
        rx = offset_x * math.cos(rad) - offset_y * math.sin(rad)
        ry = offset_x * math.sin(rad) + offset_y * math.cos(rad)
        return (self.x + rx, self.y + ry)

    def atualizar_sensores(self, mapa_colisao, escala=1.0):
        w = self.largura / 2
        h = self.altura / 2

        pontos_origem = {
            0: self.get_ponto_rotacionado(3, -h),
            -45: self.get_ponto_rotacionado(-w * 2, -h),
            45: self.get_ponto_rotacionado(w * 2, -h),
            -90: self.get_ponto_rotacionado(-w, 0),
            90: self.get_ponto_rotacionado(w, 0),
        }

        for sensor in self.sensores:
            origem = pontos_origem.get(sensor.angulo_relativo, (self.x, self.y))
            angulo_total = self.angulo + sensor.angulo_relativo
            sensor.calcular(origem[0], origem[1], angulo_total, mapa_colisao, escala)

    def atualizar(self, aceleracao, direcao, escala=1.0):
        aceleracao_max = 0.2
        velocidade_max = 5
        atrito = 0.08
        rotacao_max = 5

        self.velocidade += aceleracao
        self.velocidade = max(-velocidade_max, min(velocidade_max, self.velocidade))

        if self.velocidade > 0:
            self.velocidade = max(0, self.velocidade - atrito)
        elif self.velocidade < 0:
            self.velocidade = min(0, self.velocidade + atrito)

        if abs(self.velocidade) > 0.1:
            self.angulo += direcao * rotacao_max * (self.velocidade / velocidade_max)

        rad = math.radians(self.angulo)
        dx = math.sin(rad) * self.velocidade
        dy = -math.cos(rad) * self.velocidade
        self.x += dx * escala
        self.y += dy * escala

        self.imagem = pygame.transform.rotate(self.imagem_original, -self.angulo)
        self.rect = self.imagem.get_rect(center=(int(self.x), int(self.y)))
        self.mask = pygame.mask.from_surface(self.imagem)

    def desenhar(self, tela, offset_x=0.5, offset_y=0.5, mostrar_sensores=True):
        tela.blit(self.imagem, self.rect.move(offset_x, offset_y))

        if mostrar_sensores:
            for sensor in self.sensores:
                x1 = int(sensor.origem[0] + offset_x)
                y1 = int(sensor.origem[1] + offset_y)
                x2 = int(sensor.ponto_final[0] + offset_x)
                y2 = int(sensor.ponto_final[1] + offset_y)
                pygame.draw.line(tela, (255, 255, 0), (x1, y1), (x2, y2), 1)
                pygame.draw.circle(tela, (255, 0, 0), (x2, y2), 3)

def criar_agente():
    return Agente(x=120, y=450, imagem_path="assets/carro (4).png", escala=0.4)