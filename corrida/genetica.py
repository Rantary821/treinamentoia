import random
import pickle
from rede_neural import RedeNeural

class Individuo:
    def __init__(self):
        self.rede = RedeNeural()
        self.fitness = 0

    def avaliar(self, sensores):
        saidas, _ = self.rede.forward(sensores)
        return saidas

    def cruzar(self, outro):
        filho = Individuo()
        for i in range(len(self.rede.w_ih)):
            for j in range(len(self.rede.w_ih[i])):
                filho.rede.w_ih[i][j] = random.choice([self.rede.w_ih[i][j], outro.rede.w_ih[i][j]])

        for i in range(len(self.rede.w_ho)):
            for j in range(len(self.rede.w_ho[i])):
                filho.rede.w_ho[i][j] = random.choice([self.rede.w_ho[i][j], outro.rede.w_ho[i][j]])

        return filho

    def mutar(self, taxa=0.1):
        for i in range(len(self.rede.w_ih)):
            for j in range(len(self.rede.w_ih[i])):
                if random.random() < taxa:
                    self.rede.w_ih[i][j] += random.uniform(-1, 1)

        for i in range(len(self.rede.w_ho)):
            for j in range(len(self.rede.w_ho[i])):
                if random.random() < taxa:
                    self.rede.w_ho[i][j] += random.uniform(-1, 1)

class Populacao:
    def __init__(self, tamanho=200):
        self.geracao = 0
        self.tamanho = tamanho

        try:
            with open("melhor_agente.pkl", "rb") as f:
                melhor = pickle.load(f)
                print("🔁 Melhor agente carregado com sucesso.")
                self.individuos = [melhor] + [Individuo() for _ in range(tamanho - 1)]
        except:
            print("🆕 Nenhum agente salvo encontrado, criando população nova.")
            self.individuos = [Individuo() for _ in range(tamanho)]

    def salvar_melhor(self, caminho='melhor_agente.pkl'):
        melhor = max(self.individuos, key=lambda ind: ind.fitness)
        with open(caminho, 'wb') as f:
            pickle.dump(melhor, f)

    def evoluir(self):
        self.individuos.sort(key=lambda ind: ind.fitness, reverse=True)
        self.salvar_melhor()
        sobreviventes = self.individuos[:10]

        novos = []
        while len(novos) < self.tamanho - len(sobreviventes):
            pai = random.choice(sobreviventes)
            mae = random.choice(sobreviventes)
            filho = pai.cruzar(mae)
            filho.mutar()
            novos.append(filho)

        self.individuos = sobreviventes + novos
        self.geracao += 1
