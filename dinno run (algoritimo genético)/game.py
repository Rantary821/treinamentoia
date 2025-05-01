import pygame
import sys
import random
import json
import os
from ai.RedeNeural import RedeNeural
from ai.Genetic import Agente, nova_geracao
from utils.graficos import desenhar_rede_neural, desenhar_grafico_evolucao

# Inicializar pygame
pygame.init()
melhor_score_da_geracao = 0
WIDTH = 1300
HEIGHT = 680
FPS = 60
font_score = pygame.font.SysFont(None, 60)
font_info = pygame.font.SysFont(None, 25)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
AI_COLOR = (255, 0, 0)
OBSTACLE_COLOR = (100, 100, 100)

# Jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Run Evolution')
clock = pygame.time.Clock()

# Constantes
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_X = 100
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
OBSTACLE_SPEED_START = 5
OBSTACLE_SPEED_MAX = 15
OBSTACLE_SPEED = OBSTACLE_SPEED_START
SPAWN_DELAY_MIN = 40
SPAWN_DELAY_MAX = 120

# População
POPULACAO_TAM = 20

def carregar_melhor_rede():
    if os.path.exists("melhor_rede.json"):
        try:
            with open("melhor_rede.json", "r") as f:
                dados = json.load(f)
                r = RedeNeural()
                r.w_ih = dados["pesos_ih"]
                r.w_ho = dados["pesos_ho"]
                return r
        except:
            pass
    return RedeNeural()

agentes = []
for i in range(POPULACAO_TAM):
    rede = carregar_melhor_rede() if i == 0 else RedeNeural()
    agente = Agente(rede)
    agente.data = {
        "x": PLAYER_X,
        "y": HEIGHT - PLAYER_HEIGHT - 10,
        "vel_y": 0,
        "width": PLAYER_WIDTH,
        "height": PLAYER_HEIGHT,
        "on_ground": True,
        "alive": True,
        "frames_vivo": 0  # ✅ adicionado
    }
    agentes.append(agente)

# Obstáculos
obstacles = []
SPAWN_TIMER = random.randint(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)

# Evolução
geracao = 1
score = 0
scores_por_geracao = []

# Funções

def create_obstacle():
    return pygame.Rect(WIDTH - 300, HEIGHT - OBSTACLE_HEIGHT - 10, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

def apply_gravity(entity):
    gravity = 0.5
    entity["vel_y"] += gravity
    entity["y"] += entity["vel_y"]

    if entity["y"] >= HEIGHT - entity["height"] - 10:
        entity["y"] = HEIGHT - entity["height"] - 10
        entity["vel_y"] = 0
        entity["on_ground"] = True
    else:
        entity["on_ground"] = False

def check_collision(entity):
    rect = pygame.Rect(entity["x"], entity["y"], entity["width"], entity["height"])
    for obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

def draw_score(screen, score):
    surf = font_score.render(str(score), True, BLACK)
    rect = surf.get_rect(center=(WIDTH // 2, 50))
    screen.blit(surf, rect)

# Loop principal
while True:
    melhor_agente = None
    screen.fill(WHITE)
    pygame.draw.line(screen, (200, 200, 200), (1000, 0), (1000, HEIGHT), 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    vivos = [a for a in agentes if a.data["alive"]]
    score += 1
    # Aumentar a velocidade a cada 100 pontos, limitando a 30
    OBSTACLE_SPEED = min(OBSTACLE_SPEED_START + (score // 400), OBSTACLE_SPEED_MAX)
    if score > melhor_score_da_geracao:
        melhor_score_da_geracao = score
    # Obstáculos
    for obs in obstacles:
        obs.x -= OBSTACLE_SPEED
    obstacles = [obs for obs in obstacles if obs.right > 0]

    SPAWN_TIMER -= 1
    if SPAWN_TIMER <= 0:
        if not obstacles or (obstacles[-1].x < WIDTH - 200):
            obstacles.append(create_obstacle())
            SPAWN_TIMER = random.randint(SPAWN_DELAY_MIN, SPAWN_DELAY_MAX)

    # Atualizar agentes IA

    for agente in agentes:
        if not agente.data["alive"]:

            continue

        agente.data["frames_vivo"] += 1
        apply_gravity(agente.data)

        if obstacles:
            obst = obstacles[0]
            dist_x = max(0.0, min(1.0, (obst.x - agente.data["x"]) / 300))
        else:
            dist_x = 1.0

        entradas = [
            agente.data["y"] / HEIGHT,
            agente.data["vel_y"] / 10,
            dist_x,
            1 if agente.data["on_ground"] else 0,
            1
        ]

        saidas, ocultos = agente.rede.forward(entradas)
        agente.entradas = entradas
        agente.ocultos = ocultos
        agente.saidas = saidas

        if saidas[0] > 0.5 and agente.data["on_ground"]:
            agente.data["vel_y"] = -10

        if check_collision(agente.data):
            agente.data["alive"] = False
            agente.fitness = agente.data["frames_vivo"]

        if melhor_agente is None or agente.fitness >= melhor_agente.fitness:
            melhor_agente = agente

    # Quando todos morrerem
    if all(not a.data["alive"] for a in agentes):
        
        scores_por_geracao.append(score)
        with open("dados_geracao.json", "w") as f:
            json.dump({"scores": scores_por_geracao}, f)



        # Salvar melhor rede da geração
        if melhor_agente:
            with open("melhor_rede.json", "w") as f:
                json.dump({
                    "pesos_ih": melhor_agente.rede.w_ih,
                    "pesos_ho": melhor_agente.rede.w_ho
                }, f)


        # Resetar
        score = 0
        melhor_score_da_geracao = 0
        agentes = nova_geracao(agentes, POPULACAO_TAM)
        for agente in agentes:
            agente.data = {
                "x": PLAYER_X,
                "y": HEIGHT - PLAYER_HEIGHT - 10,
                "vel_y": 0,
                "width": PLAYER_WIDTH,
                "height": PLAYER_HEIGHT,
                "on_ground": True,
                "alive": True,
                "frames_vivo": 0  
            }
        geracao += 1

    # Visual
    for agente in agentes:
        if agente.data["alive"]:
            pygame.draw.rect(screen, AI_COLOR, (agente.data["x"], agente.data["y"], agente.data["width"], agente.data["height"]))

    draw_score(screen, score)

    texto_geracao = font_info.render(f"Geração: {geracao}", True, BLACK)
    texto_score = font_info.render(f"Score: {score}", True, BLACK)
    screen.blit(texto_geracao, (1020, 10))
    screen.blit(texto_score, (1020, 35))

    if melhor_agente:
        desenhar_rede_neural(screen, melhor_agente.entradas, melhor_agente.ocultos, melhor_agente.saidas, pos_x=1020, pos_y=90)

    desenhar_grafico_evolucao(screen, scores_por_geracao, pos_x=1020, pos_y=450)
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obs)

    pygame.display.update()
    clock.tick(FPS)
