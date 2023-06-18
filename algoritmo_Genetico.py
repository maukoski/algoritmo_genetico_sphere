import random
import matplotlib.pyplot as plt


class Individuo():
    def __init__(self,tamanho_cromossomo, geracao = 0):
        self.cromossomo = self.inicializar_cromossomo(tamanho_cromossomo)
        self.fitness = self.avaliacao()
        self.geracao = geracao

        
    def inicializar_cromossomo(self, tamanho_cromosso):
        retorno = ''
        for i in range(tamanho_cromosso):
            if random.random() > 0.5:
                retorno += '1'
            else:
                retorno += '0'
        return retorno
        
    def avaliacao(self):
        return int(self.cromossomo,2)
            
        
    def imprimir_individuo(self):
        print("Cromossomo: %s Fitness: %s Geração: %s" % (self.cromossomo,
                                              self.fitness,
                                              self.geracao))

    def crossover(self, individuo2):
        pai = self
        mae = individuo2
        
        ponto_de_corte = round(random.random() * len(self.cromossomo))
        
        filho1 = pai.cromossomo[0:ponto_de_corte] + mae.cromossomo[ponto_de_corte::]
        filho2 = mae.cromossomo[0:ponto_de_corte] + pai.cromossomo[ponto_de_corte::]
        
        filhos = [Individuo(len(filho1), pai.geracao + 1),
                  Individuo(len(filho2), mae.geracao + 1)]
        
        filhos[0].cromossomo = filho1
        filhos[0].fitness = filhos[0].avaliacao()
        
        filhos[1].cromossomo = filho2
        filhos[1].fitness = filhos[1].avaliacao()
        
        return filhos

    def mutacao(self, taxa_mutacao):
        cromossomo_list = list(self.cromossomo)
        for i in range(len(cromossomo_list)):
            if random.random() < taxa_mutacao:
                if cromossomo_list[i] == '1':
                    cromossomo_list[i] = '0' 
                else:
                    cromossomo_list[i] = '1'
        self.cromossomo = ''.join(cromossomo_list)
        return self
                

class Algoritmo_Genetico():
    def __init__(self, tamanho_populacao, numero_geracoes, tamanho_cromossomo,taxa_mutacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.lista_melhores_solucoes = []
        self.melhor_resposta = Individuo(tamanho_cromossomo)
        #self.melhor_resposta.cromossomo = '11111111'
        self.melhor_resposta.fitness = self.melhor_resposta.avaliacao()
        self.gearacoes = numero_geracoes
        self.taxa_mutacao = taxa_mutacao
        
        self.inicializar_populacao(tamanho_populacao, tamanho_cromossomo)
        self.ordenar_populacao()
        self.encontrar_melhor_solucao()
        self.resolver_problema(numero_de_geracoes)
    
    
    def inicializar_populacao(self, tamanho_populacao, tamanho_cromossomo):
        for i in range(tamanho_populacao):
            self.populacao.append(Individuo(tamanho_cromossomo))

    def ordenar_populacao(self):
        self.populacao = sorted(self.populacao,
                                key = lambda populacao: populacao.fitness,
                                reverse = False)
    
    def encontrar_melhor_solucao(self):
        if self.populacao[0].fitness < self.melhor_resposta.fitness:
            self.melhor_resposta = self.populacao[0]
        
    def printar_populacao(self):
        for i in range(len(self.populacao)):
            print("Individuo %s" % (i))
            self.populacao[i].imprimir_individuo()
    
    def somar_fitness(self):
        soma = 0
        for i in range(len(self.populacao)):
            soma += self.populacao[i].fitness
        return soma
        
    
    def selecionar_pais(self, somatorio_fitness):
        pai = 0
        valor_sorteado = random.random() * somatorio_fitness
        soma = somatorio_fitness
        i = len(self.populacao) -1
        
        while i > 0 and soma > valor_sorteado:
            soma -= self.populacao[i].fitness
            pai += 1
            i -= 1 
        return pai
    

    def resolver_problema(self, numero_de_geracoes):
        for geracoes in range(numero_de_geracoes):
            somatorio_fitness = self.somar_fitness()
            
            nova_populacao = []
            
            for individuo in range(0, self.tamanho_populacao, 2):
                pai = self.selecionar_pais(somatorio_fitness)
                mae = self.selecionar_pais(somatorio_fitness)
                
                filhos = self.populacao[pai].crossover(self.populacao[mae])
                
                nova_populacao.append(filhos[0].mutacao(self.taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(self.taxa_mutacao))

            self.populacao = list(nova_populacao)
                
            self.ordenar_populacao()
            self.encontrar_melhor_solucao()
                
            self.populacao[0].imprimir_individuo()
            self.lista_melhores_solucoes.append(self.populacao[0].fitness)
        
        print("Melhor solucção:")
        self.melhor_resposta.imprimir_individuo()

            
if __name__ == '__main__':
    tamanho_populacao = 20
    numero_de_geracoes = 100
    tamanho_cromossomo = 16
    taxa_mutacao = 0.01
    ag = Algoritmo_Genetico(tamanho_populacao, numero_de_geracoes, tamanho_cromossomo, taxa_mutacao)
    
    plt.plot(ag.lista_melhores_solucoes)
    plt.title("Melhores Soluções")
    plt.show()
 