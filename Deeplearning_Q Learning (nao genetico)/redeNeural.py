import random
import numpy as np

input_size = 5
output_size = 4


class RedeNeural:
    def __init__(self, input_size, output_size, tamanho_mapa):
        self.input_size = input_size
        self.output_size = output_size
        self.tamanho_mapa = tamanho_mapa
        self.weights = np.random.randn(input_size, output_size)
        self.bias = np.random.randn(output_size)

    #Calcula os pesos, e o output.
    def predict(self, linha_agente, coluna_agente, linha_alvo, coluna_alvo):
        input_data = self.montar_input(linha_agente, coluna_agente, linha_alvo, coluna_alvo)
        output = np.dot(input_data,self.weights)+self.bias
        action = np.argmax(output)
        return action
    
    def montar_input(self, linha_agente, coluna_agente, linha_alvo, coluna_alvo):
        dist_alvo = abs(linha_agente - linha_alvo) + abs(coluna_agente - coluna_alvo)
        input_data = [
            linha_agente / self.tamanho_mapa,
            coluna_agente / self.tamanho_mapa,
            dist_alvo / (self.tamanho_mapa*2),
            linha_alvo / self.tamanho_mapa,
            coluna_alvo / self.tamanho_mapa
        ]
        return input_data
    
    #Aqui inicia o treinamento da rede, com aprendizado por reforço utilizando deep learning
    def train(self, memory, batch_size=256):
        if len(memory) < batch_size:
            return  

        batch = random.sample(memory, batch_size)

        inputs = []
        targets = []

        for estado_atual, action, recompensa, novo_estado in batch:
            previsao = np.dot(estado_atual, self.weights) + self.bias
            Q_novo_estado = np.dot(novo_estado, self.weights) + self.bias
            max_Q_novo = np.max(Q_novo_estado)
            gamma = 0.9
            target = previsao.copy()  # Copiamos a previsão atual
            target[action] = recompensa + gamma * max_Q_novo

            inputs.append(estado_atual)
            targets.append(target)
        
        inputs = np.array(inputs)
        targets = np.array(targets)
    
        previsao_atual = np.dot(inputs, self.weights) + self.bias
        erro = targets - previsao_atual
    
        # Atualizar pesos e bias
        taxa_aprendizado = 0.15  
        self.weights += taxa_aprendizado * np.dot(inputs.T, erro) / batch_size
        self.bias += taxa_aprendizado * np.mean(erro, axis=0)
