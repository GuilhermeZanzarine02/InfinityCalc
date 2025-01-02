import matplotlib.pyplot as plt
from simpleInterest.simpleInterest import SimpleInterest

class CompoundInterest(SimpleInterest):
    def __init__(self, pi, tj, t, unidade_tempo):
        super().__init__(pi, tj, t, unidade_tempo)


    def calculo(self):
        if self.unidade_tempo == "meses":
            return self.pi* (1+ self.tj) ** self.t
        
        elif self.unidade_tempo == "anos":
            t_meses = self.t * 12
            return self.pi * (1 + self.tj) ** t_meses
        
        else:
            print("Erro! unidade de tempo invalida.")
       

    def gerarGrafico(self, graph_path="static/ImagemGrafico2.png"):

        periodos = list(range(1, int(self.t * 12) + 1))  

        valores = [self.pi * (1 + self.tj * (i / 12)) for i in periodos]  

        plt.figure(figsize=(10, 6))
        plt.plot(periodos, valores, label="Valor Total com Juros Simples", color='blue')
        plt.xlabel('Período (meses)')
        plt.ylabel('Valor Acumulado (R$)')
        plt.title('Gráfico de Juros Compostos')
        plt.grid(True)
        plt.legend()
        plt.savefig(graph_path)
        plt.close()

    def gerarGraficoPizza(self, graph_path="static/ImagemPizza2.png"):
        
         valor_total = self.pi * (1 + self.tj * self.t)

         juros_acumulados = valor_total - self.pi
         principal = self.pi

         labels = ['Principal (PI)', 'Juros Acumulados']
         valores = [principal, juros_acumulados]
         colors = ['#3498db', '#e74c3c']
        
         plt.figure(figsize=(8, 8))
         plt.pie(valores, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
         plt.title('Distribuição do Valor Total')
         plt.axis('equal')
         plt.savefig(graph_path)
         plt.close()
         


