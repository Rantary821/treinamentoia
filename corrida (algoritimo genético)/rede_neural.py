import random
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class RedeNeural:
    def __init__(self, n_input = 20, n_hidden = 50, n_output = 4):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output

        #pesos de entrada (normalização  [1,0,-1])
        self.w_ih = [[random.uniform(-1, 1) for _ in range(n_input)] for _ in range(n_hidden)]
        #pesos saida(normalização  [1,0,-1])
        self.w_ho = [[random.uniform(-1, 1) for _ in range(n_hidden)] for _ in range(n_output)]

    def forward(self, inputs):
            # Camada oculta
            hidden = []
            for h_weights in self.w_ih:
                sum_h = sum(w * i for w, i in zip(h_weights, inputs))
                hidden.append(sigmoid(sum_h))

            # Camada de saída
            output = []
            for o_weights in self.w_ho:
               sum_o = sum(w * h for w, h in zip(o_weights, hidden))
               output.append(sigmoid(sum_o))


            return output, hidden
    