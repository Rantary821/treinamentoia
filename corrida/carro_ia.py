from carro import Carro
import math
import pygame

# Checkpoints baseados na PISTA_1 (em ordem, no formato COLUNA, LINHA)
CHECKPOINTS_GRID = [
   # (0, 0),  # início
    (3, 0),  # fim da reta
    (3, 4),  # fim da descida
    (5, 4),  # curva à direita
    (5, 7),  # fundo
    (1, 7),  # retorno
]

TILE_SIZE = 100

def gerar_checkpoints_pixel():
    return [(col * TILE_SIZE + TILE_SIZE // 2, lin * TILE_SIZE + TILE_SIZE // 2) for col, lin in CHECKPOINTS_GRID]

CHECKPOINTS = gerar_checkpoints_pixel()

class CarroIA(Carro):
    def __init__(self, x, y, individuo):
        super().__init__(x, y)
        self.individuo = individuo
        self.vivo = True
        self.tempo_vivo = 0
        self.distancia_percorrida = 0
        self.ultimo_x = x
        self.ultimo_y = y
        self.sem_movimento_frames = 0
        self.checkpoint_index = 0
        self.checkpoints_atingidos = 0
        self.frames_desde_ultimo_checkpoint = 0
        self.morreu_por_colisao = False

    def atualizar_com_ia(self, matriz_logica):
        if not self.vivo:
            return
        self.frames_desde_ultimo_checkpoint += 1

        # Penaliza se passar muito tempo sem alcançar checkpoint
        if self.frames_desde_ultimo_checkpoint > 300:  # por exemplo: 5 segundos sem progresso
            self.vivo = False
            self.atualizar_fitness()
            return

        sensores = self.calcular_sensores(matriz_logica)

        entradas = []
        for origem, destino in sensores:
            distancia = math.hypot(destino[0] - origem[0], destino[1] - origem[1])
            entradas.append(distancia / 200)

        saida = self.individuo.avaliar(entradas)

        if saida[0] > 0.5:
            self.angle += 3
        if saida[1] > 0.5:
            self.angle -= 3
        if saida[2] > 0.5:
            self.velocidade = min(6.5, self.velocidade + 0.4)
        if saida[3] > 0.5:
            self.velocidade = max(-3.0, self.velocidade - 0.4)

        self.velocidade *= 0.95
        rad = math.radians(self.angle)
        dx = -self.velocidade * math.sin(rad)
        dy = -self.velocidade * math.cos(rad)

        self.x += dx
        self.y += dy
        self.distancia_percorrida += math.hypot(dx, dy)
        self.tempo_vivo += 1

        self.verificar_checkpoint()

        # Penaliza movimento mínimo (ex: girar no mesmo lugar)
        movimento = math.hypot(self.x - self.ultimo_x, self.y - self.ultimo_y)
        if movimento < 1:
            self.sem_movimento_frames += 1
        else:
            self.sem_movimento_frames = 0


        self.ultimo_x = self.x
        self.ultimo_y = self.y

        if self.sem_movimento_frames > 120:
            self.vivo = False
            self.atualizar_fitness()

    def verificar_checkpoint(self):
        if self.checkpoint_index >= len(CHECKPOINTS):
            return

        cx, cy = CHECKPOINTS[self.checkpoint_index]
        dist = math.hypot(self.x - cx, self.y - cy)

        if dist < 50:
            self.checkpoints_atingidos += 1
            self.checkpoint_index += 1
            self.frames_desde_ultimo_checkpoint = 0  # resetar o contador

    def verificar_estado(self, matriz_logica):
        if self.verificar_colisao(matriz_logica):
            self.vivo = False
            self.morreu_por_colisao = True
            self.atualizar_fitness()

    def atualizar_fitness(self):
        self.individuo.fitness = (
            self.checkpoints_atingidos * 2000 +
            self.distancia_percorrida +
            self.tempo_vivo * 0.2
        )
        if self.morreu_por_colisao:
            self.individuo.fitness *= 0.1  # penaliza fortemente (ou até 0)
