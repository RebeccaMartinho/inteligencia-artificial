from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators
import numpy as np
import os

def generate_(random, args): #geração da pop inicial
    size = args.get('num_inputs', 12)
    return [random.randint(0, 16000) for i in range(size)] #max 16000 central
#avaliação da solução
def evaluate_(candidates, args):
    fitness = []
    for cs in candidates: #para cada candidato, gera o fitness, armazena na lista e retorna ela
        fit = perform_fitness(cs[0], cs[1], cs[2], cs[3], cs[4], cs[5], cs[6], cs[7], cs[8], cs[9], cs[10], cs[11])
        fitness.append(fit)
    return fitness
#calcular o fitness para cad individuo
def perform_fitness(carga1_D, carga1_C, carga1_T, carga2_D, carga2_C, carga2_T, carga3_D, carga3_C, carga3_T, carga4_D, carga4_C, carga4_T):
  carga1_D = np.round(carga1_D) #arredondando
  carga1_C = np.round(carga1_C)
  carga1_T = np.round(carga1_T)

  carga2_D = np.round(carga2_D)
  carga2_C = np.round(carga2_C)
  carga2_T = np.round(carga2_T)

  carga3_D = np.round(carga3_D)
  carga3_C = np.round(carga3_C)
  carga3_T = np.round(carga3_T)

  carga4_D = np.round(carga4_D)
  carga4_C = np.round(carga4_C)
  carga4_T = np.round(carga4_T)
#estimativa grosseira
  lucro_total_maximo = 22750
#fitness
  fit = float(((0.31 * carga1_D + 0.31 * carga1_C + 0.31 * carga1_T) +
                (0.38 * carga2_D + 0.38 * carga2_C + 0.38 * carga2_T) + 
                (0.35 * carga3_D + 0.35 * carga3_C + 0.35 * carga3_T) + 
                (0.285 * carga4_D + 0.285 * carga4_C + 0.285 * carga4_T)) / lucro_total_maximo)
#restrição de peso dos compartimentos
  h1 = np.maximum(0, float((carga1_D + carga2_D + carga3_D + carga4_D) - 10000)) / float(10000 / 13)  #normalizando, div pela capacidade max dividida pelo fator R
  h2 = np.maximum(0, float((carga1_C + carga2_C + carga3_C + carga4_C) - 16000)) / float(16000 / 13)
  h3 = np.maximum(0, float((carga1_T + carga2_T + carga3_T + carga4_T) - 8000)) / float(8000 / 13)
#restrição  de espaço nos compartimentos
  h4 = np.maximum(0, float((0.48 * carga1_D + 0.65 * carga2_D + 0.58 * carga3_D + 0.39 * carga4_D) - 6800)) / float(6800 / 13)
  h5 = np.maximum(0, float((0.48 * carga1_C + 0.65 * carga2_C + 0.58 * carga3_C + 0.39 * carga4_C) - 8700)) / float(8700 / 13)
  h6 = np.maximum(0, float((0.48 * carga1_T + 0.65 * carga2_T + 0.58 * carga3_T + 0.39 * carga4_T) - 5300)) / float(5300 / 13)

  cargas_total = 34000
  prop_dianteira = float(10000 / cargas_total)
  prop_central = float(16000 / cargas_total)
  prop_traseira = float(8000 / cargas_total)

  carga_dianteira = float(carga1_D + carga2_D + carga3_D + carga4_D)
  carga_central = float(carga1_C + carga2_C + carga3_C + carga4_C)
  carga_traseira = float(carga1_T + carga2_T + carga3_T + carga4_T)
  soma_cargas = float(carga_dianteira + carga_central + carga_traseira)

#proporção
  h7 = np.maximum(0, float(((carga_dianteira / soma_cargas) - prop_dianteira))) / float(prop_dianteira / 13)
  h8 = np.maximum(0, float(((carga_central / soma_cargas) - prop_central))) / float(prop_central / 13)
  h9 = np.maximum(0, float(((carga_traseira / soma_cargas) - prop_traseira))) / float(prop_traseira / 13) 

#restrição do peso max das cargas
  h10 = np.maximum(0, float((carga1_D + carga1_C + carga1_T) - 18000)) / float(18000 / 13)
  h11 = np.maximum(0, float((carga2_D + carga2_C + carga2_T) - 15000)) / float(15000 / 13)
  h12 = np.maximum(0, float((carga3_D + carga3_C + carga3_T) - 23000)) / float(23000 / 13)
  h13 = np.maximum(0, float((carga4_D + carga4_C + carga4_T) - 12000)) / float(12000 / 13)
#fitness obtivo pela solução - penalizações
  fit = fit - (h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + h10 + h11 + h12 + h13)

  return fit


def solution_evaluation(carga1_D, carga1_C, carga1_T, carga2_D, carga2_C, carga2_T, carga3_D, carga3_C, carga3_T, carga4_D, carga4_C, carga4_T):
  carga1_D = np.round(carga1_D)
  carga1_C = np.round(carga1_C)
  carga1_T = np.round(carga1_T)

  carga2_D = np.round(carga2_D)
  carga2_C = np.round(carga2_C)
  carga2_T = np.round(carga2_T)

  carga3_D = np.round(carga3_D)
  carga3_C = np.round(carga3_C)
  carga3_T = np.round(carga3_T)

  carga4_D = np.round(carga4_D)
  carga4_C = np.round(carga4_C)
  carga4_T = np.round(carga4_T)

  print("\n --- Peso por compartimento --- \n")
  print("Carga 1 - dianteira:", carga1_D)
  print("Carga 1 - central:", carga1_C)
  print("Carga 1 - traseira:", carga1_T)
  carga1_total = float(carga1_D + carga1_C + carga1_T)
  print("Carga 1 - Total:", (carga1_total))

  print("\nCarga 2 - dianteira:", carga2_D)
  print("Carga 2 - central:", carga2_C)
  print("Carga 2 - traseira:", carga2_T)
  carga2_total = float(carga2_D + carga2_C + carga2_T)
  print("Carga 2 - Total:", (carga2_total))

  print("\nCarga 3 - dianteira:", carga3_D)
  print("Carga 3 - central:", carga3_C)
  print("Carga 3 - traseira:", carga3_T)
  carga3_total = float(carga3_D + carga3_C + carga3_T)
  print("Carga 3 - Total:", (carga3_total))

  print("\nCarga 4 - dianteira:", carga4_D)
  print("Carga 4 - central:", carga4_C)
  print("Carga 4 - traseira:", carga4_T)
  carga4_total = float(carga4_D + carga4_C + carga4_T)
  print("Carga 4 - Total:", (carga4_total))

  cargas_total = float(carga1_total + carga2_total + carga3_total + carga4_total)

  print("\n Total do peso do carregamento : ", cargas_total)

  print("\nCarga dianteira total:", carga1_D + carga2_D + carga3_D + carga4_D)
  print("Carga central total:", carga1_C + carga2_C + carga3_C + carga4_C)
  print("Carga traseira total:", carga1_T + carga2_T + carga3_T + carga4_T)

  lucro_c1 = float(0.31 * carga1_D + 0.31 * carga1_C + 0.31 * carga1_T)
  lucro_c2 = float(0.38 * carga2_D + 0.38 * carga2_C + 0.38 * carga2_T)
  lucro_c3 = float(0.35 * carga3_D + 0.35 * carga3_C + 0.35 * carga3_T)
  lucro_c4 = float(0.285 * carga4_D + 0.285 * carga4_C + 0.285 * carga4_T)
  
  print("\n --- Lucro por carga --- \n")
  print("Lucro carga 1:", lucro_c1)
  print("Lucro carga 2:", lucro_c2)
  print("Lucro carga 3:", lucro_c3)
  print("Lucro carga 4:", lucro_c4)
  print("Lucro Total :", lucro_c1 + lucro_c2 + lucro_c3 + lucro_c4)

  volume_dianteiro = float((carga1_D * 0.48)+(carga2_D * 0.65) + (carga3_D * 0.58) + (carga4_D * 0.39)) #peso da carga * o volume 
  volume_central = float((carga1_C * 0.48) + (carga2_C * 0.65) + (carga3_C * 0.58) + (carga4_C * 0.39))
  volume_traseiro = float((carga1_T * 0.48)+(carga2_T * 0.65) + (carga3_T * 0.58) + (carga4_T * 0.39))

  print("\n --- Volume por compartimento --- ")
  print("Total de volume dianteiro : ", volume_dianteiro)
  print("Total de volume central : ", volume_central)
  print("Total de volume traseiro : ", volume_traseiro)

  print("\n --- Proporção --- ")
  print("Proporção de Carga Dianteira: ", round(((carga1_D + carga2_D + carga3_D + carga4_D) / cargas_total),4 ))
  print("Proporção de Carga Central: ", round(((carga1_C + carga2_C + carga3_C + carga4_C) / cargas_total),4))
  print("Proporção de Carga Traseira: ", round(((carga1_T + carga2_T + carga3_T + carga4_T) / cargas_total),4))

def main():
  rand = Random()
  rand.seed(int(time())) #inicar semente aleatoria

  ea = ec.GA(rand)
  ea.selector = ec.selectors.tournament_selection #metodo de seleção: torneio
  ea.variator = [ec.variators.uniform_crossover, #op genético crossover uniforme
                  ec.variators.gaussian_mutation] #op genético mutação gaussian_mutation

  ea.replacer = ec.replacers.steady_state_replacement #determina os sobreviventes da prox geração

  ea.terminator = terminators.generation_termination #critério de parada: atingir o máx de geraçoes

  ea.observer = [ec.observers.stats_observer, ec.observers.file_observer] #geração de estatísticas da evolução

  final_pop = ea.evolve(generator=generate_, #gera pop
                        evaluator=evaluate_, #avalia soluções
                        pop_size=10000,
                        maximize=True,
                        bounder=ec.Bounder(0, 16000), #Limites minimos e maximos dos genes
                        max_generations=5000,
                        num_imputs=12,
                        crossover_rate=1.0,
                        num_crossover_points=1,
                        mutation_rate=0.15, #aplicado a cada individuo após crossover
                        num_elites=1, #qts individuos passarão para a prox pop.
                        num_selected=12, #num selecionados do torneio
                        tournament_size=12,
                        statistics_file=open("aviao_stats.csv", "w"),
                        individuals_file=open("aviao_individuais.csv", "w"))

  final_pop.sort(reverse=True) #melhor candidato
  print(final_pop[0])

  perform_fitness(final_pop[0].candidate[0], final_pop[0].candidate[1],final_pop[0].candidate[2],final_pop[0].candidate[3],final_pop[0].candidate[4],final_pop[0].candidate[5],final_pop[0].candidate[6],final_pop[0].candidate[7],final_pop[0].candidate[8],final_pop[0].candidate[9],final_pop[0].candidate[10],final_pop[0].candidate[11])
  solution_evaluation(final_pop[0].candidate[0], final_pop[0].candidate[1], final_pop[0].candidate[2], final_pop[0].candidate[3], final_pop[0].candidate[4], final_pop[0].candidate[5], final_pop[0].candidate[6], final_pop[0].candidate[7], final_pop[0].candidate[8], final_pop[0].candidate[9], final_pop[0].candidate[10], final_pop[0].candidate[11])


main()