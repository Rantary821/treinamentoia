from carro import Carro
import math
import pygame

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
        #if self.frames_desde_ultimo_checkpoint > 300:  # por exemplo: 5 segundos sem progresso
         #   self.vivo = False
          #  self.atualizar_fitness()
           # return

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

        # Verificação se está tentando voltar para checkpoint anterior
        if self.checkpoint_index > 1:
            cx_ant, cy_ant = CHECKPOINTS[self.checkpoint_index - 2]
            dist_volta = math.hypot(self.x - cx_ant, self.y - cy_ant)
            if dist_volta < 50:
                self.vivo = False
                self.individuo.fitness *= 0  # penalidade se ele voltar o checkpoint
                return
        cx, cy = CHECKPOINTS[self.checkpoint_index]
        dist = math.hypot(self.x - cx, self.y - cy)

        # Verifica se está perto de qualquer checkpoint "futuro" sem ter feito os anteriores
        if self.checkpoint_index == 0:
            # Só verifica se ele está tentando ir direto para o último checkpoint
            cx_ultimo, cy_ultimo = CHECKPOINTS[-1]
            dist_ultimo = math.hypot(self.x - cx_ultimo, self.y - cy_ultimo)
            if dist_ultimo < 50:
                self.vivo = False
                self.individuo.fitness = 0
                return

        if dist < 50:
            self.checkpoints_atingidos += 1
            self.checkpoint_index += 1
            self.frames_desde_ultimo_checkpoint = 0  # resetar o contador

    def verificar_estado(self, surface_colisao):
        if self.verificar_colisao(surface_colisao):
            self.vivo = False
            self.morreu_por_colisao = True
            self.atualizar_fitness()

    def atualizar_fitness(self):
        bonus_checkpoints = sum((i + 1) * 1000 for i in range(self.checkpoints_atingidos))

        self.individuo.fitness = (
            bonus_checkpoints +
            self.distancia_percorrida +
            self.tempo_vivo * 0.2
        )
        if self.morreu_por_colisao:
            self.individuo.fitness *= 0.9  # penaliza fortemente (ou até 0)
