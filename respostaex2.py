# -*- coding: utf-8 -*-
"""respostaEx2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wKst-jEkqx31J8uvxk7-sDpF44wQ4gMl
"""

import random
import math

def calcular_distancia(ponto1, ponto2):
    return math.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)

def avaliar_rota(rota, pontos_entrega):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += calcular_distancia(pontos_entrega[rota[i]], pontos_entrega[rota[i + 1]])
    distancia_total += calcular_distancia(pontos_entrega[rota[-1]], pontos_entrega[rota[0]])
    return distancia_total

def inicializar_populacao(tamanho_populacao, tamanho_problema):
    populacao = []
    for _ in range(tamanho_populacao):
        rota = list(range(tamanho_problema))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao

def selecionar_pais(populacao, avaliacoes):
    aptidoes_inversas = [1 / aval for aval in avaliacoes]
    total_aptidao = sum(aptidoes_inversas)
    probabilidades = [apt / total_aptidao for apt in aptidoes_inversas]
    pais = random.choices(populacao, weights=probabilidades, k=len(populacao))
    return pais

def cruzamento(pai1, pai2, pcrossover):
    if random.random() < pcrossover:
        ponto1, ponto2 = sorted(random.sample(range(len(pai1)), 2))

        filho1 = pai1[:ponto1] + pai2[ponto1:ponto2] + pai1[ponto2:]
        filho2 = pai2[:ponto1] + pai1[ponto1:ponto2] + pai2[ponto2:]

        filho1 = reparar_filho(filho1, pai1)
        filho2 = reparar_filho(filho2, pai2)

        return filho1, filho2
    return pai1, pai2

def reparar_filho(filho, pai_original):
    falta = set(pai_original) - set(filho)
    for i in range(len(filho)):
        if filho.count(filho[i]) > 1:
            filho[i] = falta.pop()
    return filho

def mutar(rota, pmutacao):
    if random.random() < pmutacao:
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]
    return rota

def algoritmo_genetico(tamanho_populacao, tamanho_problema, pontos_entrega, pcrossover, pmutacao, max_geracoes=100):
    populacao = inicializar_populacao(tamanho_populacao, tamanho_problema)
    melhor_solucao = None
    melhor_distancia = float('inf')
    melhor_geracao = 0

    for geracao in range(max_geracoes):
        avaliacoes = [avaliar_rota(rota, pontos_entrega) for rota in populacao]

        if not avaliacoes:
            print(f"Erro: Avaliações estão vazias na geração {geracao}")
            continue

        menor_distancia = min(avaliacoes)
        if menor_distancia < melhor_distancia:
            melhor_distancia = menor_distancia
            melhor_solucao = populacao[avaliacoes.index(menor_distancia)]
            melhor_geracao = geracao

        pais = selecionar_pais(populacao, avaliacoes)
        nova_populacao = []

        for i in range(0, len(pais), 2):
            pai1 = pais[i]
            if i + 1 < len(pais):
                pai2 = pais[i + 1]
                filho1, filho2 = cruzamento(pai1, pai2, pcrossover)
                nova_populacao.append(mutar(filho1, pmutacao))
                nova_populacao.append(mutar(filho2, pmutacao))
            else:
                nova_populacao.append(mutar(pai1, pmutacao))

        populacao = nova_populacao

    print(f"A melhor geração foi a {melhor_geracao}, com a solução {melhor_solucao} e distância {melhor_distancia}")
    return melhor_solucao


pontos_entrega = [(0, 0), (1, 5), (5, 1), (3, 3), (4, 4), (6, 1), (7, 7), (8, 5)]
tamanho_populacao = 10
tamanho_problema = len(pontos_entrega)
pcrossover = 0.7
pmutacao = 0.1

resultado = algoritmo_genetico(tamanho_populacao, tamanho_problema, pontos_entrega, pcrossover, pmutacao)
print("Melhor solução encontrada:", resultado)