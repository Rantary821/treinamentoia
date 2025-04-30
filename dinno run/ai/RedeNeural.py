import random
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class RedeNeural:
    def __init__(self, n_input=5, n_hidden=6, n_output=2):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output

        # Pesos entrada → oculta
        self.w_ih = [[random.uniform(-1, 1) for _ in range(n_input)] for _ in range(n_hidden)]
        # Pesos oculta → saída
        self.w_ho = [[random.uniform(-1, 1) for _ in range(n_hidden)] for _ in range(n_output)]

    def forward(self, inputs):
        # Camada oculta
        hidden = []
        for h in self.w_ih:
            sum_h = sum(w * i for w, i in zip(h, inputs))
            hidden.append(sigmoid(sum_h))

        # Camada de saída
        output = []
        for o in self.w_ho:
            sum_o = sum(w * h for w, h in zip(o, hidden))
            output.append(sigmoid(sum_o))

        return output, hidden
