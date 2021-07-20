#desenvolvido por lucas e rebecca

from random import randint

def solucao_inicial(tam):
	sol = [str(randint(0,1)) for i in range(tam)]
	return ''.join(sol)

def avaliacao(sol):
	return sol.count('1')

def gerar_vizinhos(sol):
	vizinhos = []
	for i in range(len(sol)):
		lista_bits = list(sol) #trabnsformas a solução em uma lista
		lista_bits[i] = '1' if sol[i] == '0' else '0' #troca os bits
		vizinho = ''.join(lista_bits)
		vizinhos.append(vizinho)
	return vizinhos

def movimento_tabu(sol, vizinho):
	for i in range(len(sol)):
		if sol[i] != vizinho[i]: 
			return i #movimento proibido

def obter_melhor_vizinho(vizinhos, lista_tabu, melhor_sol, sol):
	vizinhos.sort(key=avaliacao, reverse=True)#ordena a lista em ordem decrescente
	for vizinho in vizinhos:
		if movimento_tabu(sol, vizinho) in lista_tabu: #se tiver na lista tabui
			if avaliacao(vizinho) > avaliacao(melhor_sol): #testa o criterio de aspiração
				return vizinho
		else:
			return vizinho

	# se chegar aqui é porque nenhum vizinho foi selecionado
	print('erro: nenhum vizinho foi selecionado')
 
def teste (teste):
  print(teste)
  
def busca_tabu(bits=4, BTmax=2, T=1):
	lista_tabu = []
	Iter, melhor_iter = 0, 0
	sol = solucao_inicial(bits)
	melhor_sol = sol[:]
	print('Solução inicial: ', sol)
	print('Avaliação da solução inicial: ', avaliacao(sol))

	while (Iter - melhor_iter) <= BTmax:
		avaliacao_sol = avaliacao(sol)
		vizinhos = gerar_vizinhos(sol)
		melhor_vizinho = obter_melhor_vizinho(vizinhos, lista_tabu, melhor_sol, sol)
		sol = melhor_vizinho[:]
		pos_tabu = movimento_tabu(sol, melhor_vizinho)

		if len(lista_tabu) < T: #se o tamanho da lista for menor que o tamanho da lista tabu
			lista_tabu.append(pos_tabu)
		else:#a lista esta cheia
			lista_tabu.pop(0)
			lista_tabu.append(pos_tabu)

		if avaliacao(melhor_vizinho) > avaliacao(melhor_sol):#atualiza melhor solução e melhor iter
			melhor_sol = melhor_vizinho[:]
			melhor_iter += 1

		Iter += 1

	return melhor_sol, Iter, melhor_iter

if __name__ == '__main__':
	melhor_solucao, Iter, MelhorIter = busca_tabu(bits=100, BTmax=2, T=2)
	print('\nMelhor solução: ', melhor_solucao, '\nIter.', Iter, '\nMelhor Iter.', MelhorIter)
	print('Avaliação da melhor solução: ', avaliacao(melhor_solucao))