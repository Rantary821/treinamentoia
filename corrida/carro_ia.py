from carro import Carro
import math
import pygame

class CarroIA(Carro):
    def __init__(self, x, y, individuo):
        super().__init__(x, y)
        self.individuo = individuo
        self.vivo = True
        self.tempo_vivo = 0
        self.distancia_percorrida = 0

    def atualizar_com_ia(self, matriz_logica):
        if not self.vivo:
            return

        sensores = self.calcular_sensores(matriz_logica)

        # Converte sensores em distância normalizada
        entradas = []
        for origem, destino in sensores:
            distancia = math.hypot(destino[0] - origem[0], destino[1] - origem[1])
            entradas.append(distancia / 200)  # normaliza

        saida = self.individuo.avaliar(entradas)

        # Converte ações em movimentos
        if saida[0] > 0.5:  # girar esquerda
            self.angle += 3
        if saida[1] > 0.5:  # girar direita
            self.angle -= 3
        if saida[2] > 0.5:  # acelerar
            self.velocidade = min(6.5, self.velocidade + 0.4)
        if saida[3] > 0.5:  # frear
            self.velocidade = max(-3.0, self.velocidade - 0.4)

        self.velocidade *= 0.95
        rad = math.radians(self.angle)
        dx = -self.velocidade * math.sin(rad)
        dy = -self.velocidade * math.cos(rad)

        self.x += dx
        self.y += dy
        self.distancia_percorrida += math.hypot(dx, dy)
        self.tempo_vivo += 1

    def verificar_estado(self, matriz_logica):
        if self.verificar_colisao(matriz_logica):
            self.vivo = False
            self.individuo.fitness = self.distancia_percorrida + self.tempo_vivo * 0.5
