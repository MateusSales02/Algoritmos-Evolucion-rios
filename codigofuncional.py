import random

def inicializar_populacao(tamanho_populacao, tamanho_problema):
    return [random.sample(range(100), tamanho_problema) for _ in range(tamanho_populacao)]

def avaliar_populacao(populacao):
    return [fitness(ind) for ind in populacao]

def fitness(individuo):
    return sum(individuo)

def obter_melhor_solucao(populacao):
    avaliacoes = avaliar_populacao(populacao)
    return populacao[avaliacoes.index(max(avaliacoes))]

def condicao_de_parada(geracao, max_geracoes):
    return geracao >= max_geracoes

def selecionar_pais(populacao):
    avaliacoes = avaliar_populacao(populacao)
    total = sum(avaliacoes)
    probabilidades = [aval / total for aval in avaliacoes]
    pais = random.choices(populacao, weights=probabilidades, k=len(populacao) // 2)
    return pais

def cruzamento(pai1, pai2, pcrossover):
    if random.random() < pcrossover:
        ponto = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto] + pai2[ponto:]
        filho2 = pai2[:ponto] + pai1[ponto:]
        return filho1, filho2
    return pai1, pai2
def mutar(individuo, pmutacao):
    for i in range(len(individuo)):
        if random.random() < pmutacao:
            individuo[i] = random.randint(0, 100)
    return individuo

def substituir(populacao, filhos):
    return populacao + filhos

def algoritmo_genetico(tamanho_populacao, tamanho_problema, pcrossover, pmutacao, max_geracoes=100):
    populacao = inicializar_populacao(tamanho_populacao, tamanho_problema)
    melhor_solucao = obter_melhor_solucao(populacao)

    geracao = 0
    while not condicao_de_parada(geracao, max_geracoes):
        pais = selecionar_pais(populacao)
        filhos = []

        for i in range(0, len(pais), 2):
            pai1 = pais[i]
            if i + 1 < len(pais):
                pai2 = pais[i + 1]
                filho1, filho2 = cruzamento(pai1, pai2, pcrossover)
                filhos.append(mutar(filho1, pmutacao))
                filhos.append(mutar(filho2, pmutacao))
            else:
                filhos.append(mutar(pai1, pmutacao))

        populacao = substituir(populacao, filhos)
        melhor_solucao = obter_melhor_solucao(populacao)

        geracao += 1
        print(f"Geração {geracao}: Melhor solução até agora: {melhor_solucao}, Fitness: {fitness(melhor_solucao)}")

    return melhor_solucao

tamanho_populacao = 10
tamanho_problema = 5
pcrossover = 0.7
pmutacao = 0.1

resultado = algoritmo_genetico(tamanho_populacao, tamanho_problema, pcrossover, pmutacao)
print("Melhor solução encontrada:", resultado)
