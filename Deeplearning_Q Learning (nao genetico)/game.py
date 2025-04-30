import pygame
import numpy as np
import random
import sys
from redeNeural import RedeNeural
import time

# Inicializar o pygame
pygame.init()

# Inicializando a rede neural
rede_neural = RedeNeural(input_size=5, output_size=4, tamanho_mapa=10)

# Configurações

GRAFICO_HEIGHT = 200  
SIZE = 10
CELL_SIZE = 50
JOGO_WIDTH = SIZE * CELL_SIZE  
PAINEL_WIDTH = 500
WINDOW_WIDTH = JOGO_WIDTH + PAINEL_WIDTH
WINDOW_HEIGHT = JOGO_WIDTH + GRAFICO_HEIGHT 
score = 0
font = pygame.font.SysFont(None, 40)
font_rede = pygame.font.SysFont(None, 25)     # Fonte da rede neural (inputs e outputs)
memory =[]
recompensas_medias = []


NUM_AGENTES = 100  #Define quantidade de agentes(IA)
#definindo lista de array automaticamente com o NUM_AGENTES
agents = []
for _ in range(NUM_AGENTES):
    agent_info = {
        "pos": [random.randint(0, SIZE-1), random.randint(0, SIZE-1)],
        "target": [random.randint(0, SIZE-1), random.randint(0, SIZE-1)],
        "movimentos_sem_pegar_alvo": 0
    }
    agents.append(agent_info)
NUM_AGENTES_VISIVEIS = 1  # Quantidade de plot de agente na tela.


# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
AGENT_COLORS = [
    (0, 0, 255),    # Azul
    (0, 255, 0),    # Verde
    (255, 0, 0),    # Vermelho
    (255, 255, 0),  # Amarelo
    (255, 0, 255),  # Rosa
    (0, 255, 255),  # Ciano
    (255, 165, 0),  # Laranja
    (128, 0, 128),  # Roxo
    (0, 128, 0),    # Verde escuro
    (128, 128, 0),  # Mostarda
]
# Criar janela
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Catch the Dot - Rede Neural')

# Funções para desenhar a rede neural
input_names = ["Agente X", "Agente Y", "Distância", "Alvo X", "Alvo Y"]
def draw_label(screen, text, position, color=(0,0,0)):
    label = font_rede.render(text, True, color)
    screen.blit(label, (position[0], position[1]))

def draw_connections(screen, connections):
    for start, end in connections:
        pygame.draw.line(screen, GRAY, start, end, 2)

def draw_input_nodes(screen, input_positions, input_values):
    input_names = ["Agente X", "Agente Y", "Distância", "Alvo X", "Alvo Y"]
    for idx, pos in enumerate(input_positions):
        pygame.draw.rect(screen, (0, 0, 255), (pos[0]-10, pos[1]-10, 20, 20))
        texto = f"{input_names[idx]}: {input_values[idx]:.2f}"
        draw_label(screen, texto, (pos[0] - 30, pos[1] + 25))

def draw_weight_nodes(screen, weight_positions):
    for pos in weight_positions:
        pygame.draw.polygon(screen, (255, 165, 0), [
            (pos[0], pos[1]-10),
            (pos[0]+10, pos[1]),
            (pos[0], pos[1]+10),
            (pos[0]-10, pos[1])
        ])

def draw_output_nodes(screen, output_positions, chosen_action):
    output_names = ["Cima", "Baixo", "Esquerda", "Direita"]
    for idx, pos in enumerate(output_positions):
        if idx == chosen_action:
            color = (0, 255, 0)  
        else:
            color = (255, 0, 0)  
        pygame.draw.circle(screen, color, pos, 15)
        draw_label(screen, output_names[idx], (pos[0] - 30, pos[1] + 25))

# Posições dos inputs
input_positions = [
    (550, 80),
    (550, 160),
    (550, 240),
    (550, 320),
    (550, 400),
]

# Posições dos outputs
output_positions = [
    (850, 120),
    (850, 220),
    (850, 320),
    (850, 420),
]

# Posições dos pesos e conexões
weight_positions = []
connections = []

for inp in input_positions:
    for out in output_positions:
        mid_x = (inp[0] + out[0]) // 2
        mid_y = (inp[1] + out[1]) // 2
        weight_positions.append((mid_x, mid_y))
        connections.append((inp, (mid_x, mid_y)))
        connections.append(((mid_x, mid_y), out))

# Inicializar agente e alvo
agent_pos = [0, 0]
target_pos = [random.randint(0, SIZE-1), random.randint(0, SIZE-1)]

# Funções auxiliares do jogo
def draw_grid():
    for x in range(0, JOGO_WIDTH, CELL_SIZE):
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)

def draw_score():
    text = font.render(f"score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_agent(agent_pos, color):
    rect = pygame.Rect(agent_pos[1]*CELL_SIZE, agent_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def draw_target(target_pos, color):
    rect = pygame.Rect(target_pos[1]*CELL_SIZE, target_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

def draw_time(elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_text = font.render(f"Tempo de execução: {minutes:02d}:{seconds:02d}", True, BLACK)
    screen.blit(timer_text,(JOGO_WIDTH + 20, 20))

def draw_learning_curve(recompensas_medias):
    if len(recompensas_medias) < 2:
        return  

    max_height = GRAFICO_HEIGHT - 40 
    largura = 400
    start_x = JOGO_WIDTH + 50  
    start_y = JOGO_WIDTH + GRAFICO_HEIGHT - 30 

    # Normalizar recompensas
    max_recompensa = max(max(recompensas_medias), 1)
    normalized = [r / max_recompensa for r in recompensas_medias[-largura:]]
    pygame.draw.rect(screen, (230, 230, 230), (JOGO_WIDTH, JOGO_WIDTH, PAINEL_WIDTH, GRAFICO_HEIGHT))
    for i in range(len(normalized) - 1):
        x1 = start_x + i
        y1 = start_y - normalized[i] * max_height
        x2 = start_x + i + 1
        y2 = start_y - normalized[i+1] * max_height
        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)







start_time = time.time()
contador_frames = 0
FREQUENCIA_TREINO = 1  
# Loop principal
clock = pygame.time.Clock()
movimentos_sem_pegar_alvo = 0  
MAX_PASSOS = 25  

# NOVO: inicializar a quantidade de agentes
#NUM_AGENTES = 5  # Controla quantos agentes serão treinados
agents = []
for _ in range(NUM_AGENTES):
    agent_info = {
        "pos": [0, 0],
        "target": [random.randint(0, SIZE-1), random.randint(0, SIZE-1)],
        "movimentos_sem_pegar_alvo": 0
    }
    agents.append(agent_info)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    contador_frames += 1
    elapsed_time = time.time() - start_time
    # inicializando os agentes da lista de array
    for agent in agents:
        linha_agente, coluna_agente = agent["pos"]
        linha_target, coluna_target = agent["target"]

        # Atualizar contador de movimentos é feito depois, após mover


        epsilon = 0.1  
        if random.random() < epsilon:
            action = random.randint(0, 3)  
        else:
            action = rede_neural.predict(linha_agente, coluna_agente, linha_target, coluna_target)

        # CALCULAR distância antes de agir
        distancia_antes = abs(linha_agente - linha_target) + abs(coluna_agente - coluna_target)

        input_values = [
            linha_agente / SIZE,
            coluna_agente / SIZE,
            (abs(linha_agente - linha_target) + abs(coluna_agente - coluna_target)) / (SIZE*2),
            linha_target / SIZE,
            coluna_target / SIZE
        ]
        estado_atual = input_values.copy()

        #print(f"Ação escolhida pela IA: {action}")
        # Atualizar lista de recompensas médias
        if len(memory) > 0:
            recompensas = [exp[2] for exp in memory[-200:]]  # últimas 200 experiências
            media_recompensa = sum(recompensas) / len(recompensas)
            recompensas_medias.append(media_recompensa)

        # Executar movimento
        if action == 0 and linha_agente > 0:
            linha_agente -= 1
        elif action == 1 and linha_agente < SIZE-1:
            linha_agente += 1
        elif action == 2 and coluna_agente > 0:
            coluna_agente -= 1
        elif action == 3 and coluna_agente < SIZE-1:
            coluna_agente += 1

        # Atualizar a posição do agente após agir
        agent["pos"] = [linha_agente, coluna_agente]

        # CALCULAR distância depois de agir
        distancia_depois = abs(linha_agente - linha_target) + abs(coluna_agente - coluna_target)

               # Atualizar contador de movimentos
        if distancia_depois < distancia_antes:
            agent["movimentos_sem_pegar_alvo"] = 0  
            agent["movimentos_sem_pegar_alvo"] += 1  

        # NOVO SISTEMA DE RECOMPENSA
        if agent["pos"] == agent["target"]:
            recompensa = 100  
        elif distancia_depois < distancia_antes:
            recompensa = 10   
        elif distancia_depois > distancia_antes:
            recompensa = -2   
        elif distancia_depois == distancia_antes:
            recompensa = -5  

        # PUNIÇÃO extra por muitos movimentos sem pegar o alvo
        if agent["movimentos_sem_pegar_alvo"] > MAX_PASSOS:
            recompensa -= 50  # Punição
            #print("🔄 Resetando agente: travou muito!")
            agent["pos"] = [0, 0]
            agent["target"] = [random.randint(0, SIZE-1), random.randint(0, SIZE-1)]
            agent["movimentos_sem_pegar_alvo"] = 0


        # Salvar na memoria as experiencias do agente
        novo_estado = [
            linha_agente / SIZE,
            coluna_agente / SIZE,
            (abs(linha_agente - linha_target) + abs(coluna_agente - coluna_target)) / (SIZE*2),
            linha_target / SIZE,
            linha_target / SIZE
        ]
        experience = (estado_atual, action, recompensa, novo_estado)
        memory.append(experience)

        # Limitador da memória
        if len(memory) > 20000:
            memory.pop(0)

    # Treinando a rede
    rede_neural.train(memory)

    # Mostrar no terminal só pra meio de debug, e saber oq se passa no sistema de recompensa
    #print(f"Ação: {action} | Recompensa: {recompensa}")

    # Atualizar tela
    screen.fill(WHITE)
    draw_grid()
    # Desenha TODOS os agentes
    for idx, agent in enumerate(agents[:NUM_AGENTES_VISIVEIS]):
        cor_agente = AGENT_COLORS[idx % len(AGENT_COLORS)]
        draw_agent(agent["pos"], cor_agente)
        draw_target(agent["target"], cor_agente)



    draw_agent(agents[0]["pos"], AGENT_COLORS[0])
    draw_target(agents[0]["target"], AGENT_COLORS[0])
    draw_score()

    # Painel da rede neural
    draw_connections(screen, connections)
    draw_input_nodes(screen, input_positions, input_values)  # <-- agora passando os valores
    draw_weight_nodes(screen, weight_positions)
    draw_output_nodes(screen, output_positions, action)
    draw_time(elapsed_time)
    draw_learning_curve(recompensas_medias)

    pygame.display.update()

    # Verificar se pegou o alvo (primeiro agente no visual)
    if agents[0]["pos"] == agents[0]["target"]:
        score += 1
        print("🏆 Pegou o alvo!")
        agents[0]["movimentos_sem_pegar_alvo"] = 0
        pygame.time.wait(1000)
        agents[0]["pos"] = [0, 0]
        agents[0]["target"] = [random.randint(0, SIZE-1), random.randint(0, SIZE-1)]

    clock.tick(15) 
