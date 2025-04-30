import matplotlib.pyplot as plt

plt.ion()  # modo interativo

fig, ax = plt.subplots()
linha_max, = ax.plot([], [], label="Fitness Máximo")
linha_med, = ax.plot([], [], label="Fitness Médio")
ax.set_title("Evolução da IA")
ax.set_xlabel("Geração")
ax.set_ylabel("Fitness")
ax.legend()
ax.grid(True)

def atualizar(pop):
    linha_max.set_data(range(len(pop.historico_fitness_max)), pop.historico_fitness_max)
    linha_med.set_data(range(len(pop.historico_fitness_medio)), pop.historico_fitness_medio)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.001)
