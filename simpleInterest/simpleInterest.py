import os
import matplotlib.pyplot as plt

class SimpleInterest:
    def __init__(self, pi, tj, t):
        self.pi = pi
        self.tj = tj / 100
        self.t = t 

    def calculo(self):
        value = self.pi * (1 + self.tj * self.t)
        return value
    
    def gerarGrafico(self, graph_path="static/ImagemGrafico.png"):

         # Gerando os períodos mensais (1 até t * 12 meses)
        periodos = list(range(1, int(self.t * 12) + 1))  # Períodos de 1 até t * 12 meses

        # Calculando o valor acumulado para cada mês
        valores = [self.pi * (1 + self.tj * (i / 12)) for i in periodos]  # Usando o i/12 para representar o mês a mês

        # Gerando o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(periodos, valores, label="Valor Total com Juros Simples", color='blue')
        plt.xlabel('Período (meses)')
        plt.ylabel('Valor Acumulado (R$)')
        plt.title('Gráfico de Juros Simples')
        plt.grid(True)
        plt.legend()

        # Salvando o gráfico no caminho especificado
        plt.savefig(graph_path)
        plt.close()