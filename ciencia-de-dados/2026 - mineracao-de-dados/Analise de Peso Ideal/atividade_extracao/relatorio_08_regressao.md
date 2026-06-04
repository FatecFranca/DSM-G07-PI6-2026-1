# Relatório – Etapa de Extração de Padrões

**Projeto:** PetDex  
**Disciplina:** Mineração de Dados  

---

# 1. Objetivo da etapa

O objetivo desta etapa foi realizar a extração de padrões a partir de uma base de dados contendo informações sobre cães, utilizando algoritmos de Machine Learning para regressão.

A proposta do projeto é prever um peso saudável esperado para o animal com base em características físicas e comportamentais.

Durante o processo, foram realizadas etapas de limpeza, seleção de atributos, treinamento de modelos e comparação de métricas.

---

# 2. Base de dados utilizada

Foi utilizada a base:

**Canine Wellness Dataset – Synthetic 10k Samples**

Disponível no Kaggle.

A base possui aproximadamente 10 mil registros contendo informações sobre cães, incluindo:

- raça;
- porte;
- idade;
- sexo;
- nível de atividade;
- distância caminhada;
- horas de sono;
- tempo de brincadeira;
- visitas ao veterinário;
- peso.

---

# 3. Pré-processamento realizado

Antes do treinamento dos modelos, foi realizado um pré-processamento da base de dados.

As etapas executadas foram:

## 3.1 Filtragem de animais saudáveis

Foram mantidos apenas os registros classificados como animais saudáveis, evitando que o modelo aprendesse padrões relacionados a possíveis problemas de saúde.

## 3.2 Remoção de atributos irrelevantes

Alguns atributos foram removidos por apresentarem pouca relação com o objetivo do problema.

### Atributos removidos

- `Spay/Neuter Status`
- `Other Pets in Household`
- `Seizures`
- `Owner Activity Level`
- `Average Temperature (F)`

A remoção foi feita para reduzir ruído no treinamento.

## 3.3 Tratamento de valores nulos

Os registros com valores ausentes foram tratados para evitar falhas durante o treinamento.

## 3.4 Remoção de outliers

Foi realizada remoção de registros extremos utilizando análise estatística por porte do animal.

Essa etapa buscou reduzir inconsistências na base sintética.

## 3.5 Seleção de atributos

Foram mantidos os atributos considerados mais relevantes para previsão do peso:

- `Breed`
- `Breed Size`
- `Sex`
- `Age`
- `Daily Activity Level`
- `Daily Walk Distance (miles)`
- `Hours of Sleep`
- `Play Time (hrs)`
- `Annual Vet Visits`

---

# 4. Algoritmos utilizados

Foram utilizados três algoritmos de regressão.

## 4.1 Linear Regression

Utilizado como modelo base devido à sua simplicidade e facilidade de interpretação.

Esse algoritmo busca encontrar uma relação linear entre os atributos e o peso do animal.

## 4.2 Random Forest Regressor

Escolhido por sua capacidade de trabalhar com relações não lineares.

O algoritmo utiliza múltiplas árvores de decisão para melhorar a capacidade de generalização.

## 4.3 Gradient Boosting Regressor

Utilizado para tentar melhorar os resultados através de aprendizado incremental.

O modelo corrige gradualmente os erros cometidos durante o treinamento.

---

# 5. Métricas utilizadas

As seguintes métricas foram utilizadas para avaliação:

## MAE (Mean Absolute Error)

Representa o erro médio absoluto entre o valor previsto e o valor real.

Quanto menor o MAE, melhor o modelo.

## RMSE (Root Mean Squared Error)

Mede o erro quadrático médio.

Penaliza erros maiores durante a previsão.

## R² (Coeficiente de Determinação)

Indica o quanto o modelo consegue explicar os padrões da base.

Valores próximos de 1 representam melhor desempenho.

---

# 6. Resultados obtidos

Os modelos apresentaram resultados semelhantes.

O modelo **Linear Regression** apresentou o melhor desempenho entre os três algoritmos testados.

Entretanto, o valor de R² permaneceu baixo.

Isso indica que a base sintética apresenta alta dispersão e inconsistência entre atributos como raça, porte e peso.

Mesmo após limpeza e seleção de atributos, os modelos tiveram dificuldade em encontrar padrões fortes na base.

Essa análise foi considerada importante para demonstrar limitações reais presentes em bases sintéticas.

---

# 7. Conclusão

A etapa de extração de padrões permitiu aplicar técnicas de regressão, seleção de atributos e avaliação de modelos de Machine Learning.

Os resultados mostraram que o pré-processamento e a seleção de atributos ajudam a reduzir ruído e melhorar a interpretação dos dados.

Também foi possível observar limitações presentes na base utilizada, principalmente relacionadas à inconsistência estatística entre peso, raça e porte.

Como continuidade do projeto, pretende-se criar um target mais inteligente baseado em médias por raça, porte e idade, permitindo melhorar a qualidade das previsões realizadas pelo sistema.