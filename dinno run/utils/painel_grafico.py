import json
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

CAMINHO_DADOS = "dados_geracao.json"  # gerado pelo game.py

scores = []

def atualizar_grafico():
    global scores

    # Se o arquivo existir, carrega os dados
    if os.path.exists(CAMINHO_DADOS):
        with open(CAMINHO_DADOS, "r") as f:
            try:
                dados = json.load(f)
                scores = dados.get("scores", [])
            except:
                pass  # evita erro de leitura durante escrita

    ax.clear()
    ax.set_title("Evolução por Geração")
    ax.set_xlabel("Geração")
    ax.set_ylabel("Score")
    ax.plot(scores, color="blue", label="Melhor Score")
    ax.legend()
    canvas.draw()

    root.after(1000, atualizar_grafico)  # atualiza a cada 1s

# Janela Tkinter
root = tk.Tk()
root.title("Painel IA - Gráfico de Score")
root.geometry("500x300")

fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

atualizar_grafico()
root.mainloop()
