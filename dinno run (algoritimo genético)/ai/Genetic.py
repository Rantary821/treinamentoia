# genetic.py
import random
import copy

class Agente:
    def __init__(self, rede, fitness=0):
        self.rede = rede
        self.fitness = fitness


def selecao_roleta(populacao):
    soma = sum(a.fitness for a in populacao)
    if soma == 0:
        return random.choice(populacao)
    pick = random.uniform(0, soma)
    atual = 0
    for agente in populacao:
        atual += agente.fitness
        if atual > pick:
            return agente
    return populacao[-1]


def crossover(pai1, pai2):
    filho = copy.deepcopy(pai1)
    for i in range(len(filho.rede.w_ih)):
        for j in range(len(filho.rede.w_ih[i])):
            if random.random() < 0.5:
                filho.rede.w_ih[i][j] = pai2.rede.w_ih[i][j]
    for i in range(len(filho.rede.w_ho)):
        for j in range(len(filho.rede.w_ho[i])):
            if random.random() < 0.5:
                filho.rede.w_ho[i][j] = pai2.rede.w_ho[i][j]
    return filho


def mutacao(rede, taxa=0.1, intensidade=0.5):
    for i in range(len(rede.w_ih)):
        for j in range(len(rede.w_ih[i])):
            if random.random() < taxa:
                rede.w_ih[i][j] += random.uniform(-intensidade, intensidade)
    for i in range(len(rede.w_ho)):
        for j in range(len(rede.w_ho[i])):
            if random.random() < taxa:
                rede.w_ho[i][j] += random.uniform(-intensidade, intensidade)


def nova_geracao(populacao, tamanho):
    nova = []
    populacao.sort(key=lambda a: a.fitness, reverse=True)
    elite = populacao[0]
    nova.append(Agente(copy.deepcopy(elite.rede)))  # elitismo

    while len(nova) < tamanho:
        pai1 = selecao_roleta(populacao)
        pai2 = selecao_roleta(populacao)
        filho = crossover(pai1, pai2)
        mutacao(filho.rede)
        nova.append(filho)

    return nova
