import matplotlib.pyplot as plt

class SimpleInterest:
    def __init__(self, pi, tj, t, unidade_tempo, periodo_taxa):
        self.pi = pi
        self.tj = tj / 100
        self.t = t
        self.unidade_tempo = unidade_tempo
        self.periodo_taxa = periodo_taxa


    def calculo(self):
        
        if self.unidade_tempo == 'meses' and self.periodo_taxa == 'mensal':
            return self.pi * (1 + self.tj * self.t)

        elif self.unidade_tempo == "anos" and self.periodo_taxa == 'anual':
            return self.pi * (1 + self.tj * self.t)

        elif self.unidade_tempo == "meses" and self.periodo_taxa == 'anual':
            taxa_mensal = self.tj / 12
            return self.pi * (1 + taxa_mensal * self.t)
        
        elif self.unidade_tempo == "anos" and self.periodo_taxa == 'mensal':
            tempo_meses = self.t * 12
            return self.pi * (1 + self.tj * tempo_meses)
        
        else:
            print("Erro! unidade de tempo invalida.")
        

    def gerarGrafico(self, graph_path="static/ImagemGrafico.png"):

        periodos = list(range(1, int(self.t * 12) + 1))  

        valores = [self.pi * (1 + self.tj * (i / 12)) for i in periodos]  
       
        plt.figure(figsize=(10, 6))
        plt.plot(periodos, valores, label="Valor Total com Juros Simples", color='blue')
        plt.xlabel('Período (meses)')
        plt.ylabel('Valor Acumulado (R$)')
        plt.title('Gráfico de Juros Simples')
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
