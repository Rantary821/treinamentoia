import random
import copy

from rede_neural import RedeNeural

class Individuo:
    def __init__(self):
        self.rede = RedeNeural() #Cria uma nova rede neural dentro do indivíduo.
        self.fitness = 0         #fitness mede o quão bem ele se saiu (ex: tempo vivo, distância etc.).

    def avaliar(self, sensores):
        # Recebe os dados dos sensores e usa a rede para gerar a decisão
        saidas, _ = self.rede.forward(sensores) #Recebe os valores dos sensores (ex: distâncias).
        return saidas                           #Roda o forward() da rede e retorna as saídas (ex: acelerar, virar).

    def cruzar(self, outro):  #Cria um novo filho (outra rede neural zerada).
        filho = Individuo()
        # Cruzamento dos pesos entre entrada e camada oculta
        for i in range(len(self.rede.w_ih)):    #Faz isso para cada peso da entrada→oculta (w_ih) e oculta→saída (w_ho).
            for j in range(len(self.rede.w_ih[i])):
                if random.random() < 0.5:
                    filho.rede.w_ih[i][j] = self.rede.w_ih[i][j]
                else:
                    filho.rede.w_ih[i][j] = outro.rede.w_ih[i][j]

        # Cruzamento dos pesos entre camada oculta e saída
        for i in range(len(self.rede.w_ho)):
            for j in range(len(self.rede.w_ho[i])):
                if random.random() < 0.5:
                    filho.rede.w_ho[i][j] = self.rede.w_ho[i][j]
                else:
                    filho.rede.w_ho[i][j] = outro.rede.w_ho[i][j]

        return filho

    def mutar(self, taxa=0.1):  #taxa: chance de cada peso ser alterado (10% por padrão).
        for i in range(len(self.rede.w_ih)):
            for j in range(len(self.rede.w_ih[i])):
                if random.random() < taxa:  #Altera um pouco o valor do peso (positiva ou negativamente). Isso evita que a população fique "presa" sem evolução.
                    self.rede.w_ih[i][j] += random.uniform(-1, 1)

        for i in range(len(self.rede.w_ho)):
            for j in range(len(self.rede.w_ho[i])):
                if random.random() < taxa:
                    self.rede.w_ho[i][j] += random.uniform(-1, 1)

class Populacao:
    def __init__(self, tamanho=50): #criando os individuos
        self.individuos = [Individuo() for _ in range(tamanho)]
        self.geracao = 0    #geracao conta o número de ciclos de evolução.

    def evoluir(self):
        # Ordena por fitness (maior é melhor)
        self.individuos.sort(key=lambda ind: ind.fitness, reverse=True) #Ordena os indivíduos com base no fitness (do melhor para o pior).
        sobreviventes = self.individuos[:10]  # top 10 sobreviventes

        # Gera novos filhos
        novos = []
        while len(novos) < len(self.individuos) - len(sobreviventes):#Gera novos filhos cruzando e mutando os sobreviventes.
            pai = random.choice(sobreviventes)
            mae = random.choice(sobreviventes)
            filho = pai.cruzar(mae)
            filho.mutar()       #Preenche o resto da população com filhos novos.
            novos.append(filho)

        self.individuos = sobreviventes + novos #Atualiza a nova geração e soma +1 na contagem.
        self.geracao += 1
