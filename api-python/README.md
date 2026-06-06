<p align="center">
  <img src="../docs/img/capa-python.svg" alt="Capa do Projeto" width="100%" />
</p>

# 🧮 API em Python — O Cérebro Analítico da PetDex

Bem-vindo à API de Análise de Dados da PetDex! Desenvolvida com **Python** e **FastAPI**, esta API é o coração analítico do nosso ecossistema. Ela é responsável por **transformar os dados brutos coletados pela coleira em insights acionáveis** e executar o **modelo de Inteligência Artificial** que identifica a espécie do animal, capacitando os donos a cuidarem melhor da saúde de seus pets.


## ⚙️ Tecnologias Utilizadas

* **Python 3.11**
* **FastAPI** (Framework web moderno e assíncrono)
* **Pandas** (Análise e manipulação de dados)
* **NumPy** (Cálculos numéricos e estatísticos)
* **SciPy** (Cálculos científicos, como a distribuição normal)
* **Scikit-learn** (Modelos de Machine Learning)
* **PyPMML** (Carregamento e execução de modelos PMML)
* **httpx** (Cliente HTTP assíncrono para comunicação com a API Java)
* **Uvicorn** (Servidor ASGI)
* **Google Cloud** (Plataforma de hospedagem da API)

---

# 📡 Hospedagem da API

A API está hospedada em um servidor **Google Cloud** e pode ser acessada através do link:

🔗 **API Base:** [http://34.24.9.134:8083](http://34.24.9.134:8083)

📘 **Documentação Interativa (Swagger):** [http://34.24.9.134:8083/docs](http://34.24.9.134:8083/docs)

### 🔐 Autenticação JWT

Todos os endpoints (exceto `/health`) requerem autenticação via **JWT (JSON Web Tokens)**.

**Fluxo de Autenticação:**

1. O aplicativo mobile faz login na **API Java** (endpoint `POST /auth/login`)
2. A API Java retorna um **token JWT**
3. O aplicativo envia esse token no header `Authorization: Bearer <token>` para a **API Python**
4. A API Python valida o token usando a mesma chave secreta (`JWT_SECRET`) configurada na API Java

### **🔑 Credenciais de Teste**

Para testar a API, utilize as seguintes credenciais na API Java:

```json
{
  "email": "henriquealmeidaflorentino@gmail.com",
  "senha": "senha123"
}
```

## 🧠 Objetivo da API

Esta API **não coleta dados diretamente da coleira**. Seu papel estratégico é **consumir os dados já armazenados na API principal (Java)** e aplicar uma camada de inteligência sobre eles. Ela executa desde cálculos estatísticos avançados até a **classificação de espécies com Inteligência Artificial**, fornecendo as análises que tornam o aplicativo PetDex uma ferramenta poderosa para o monitoramento da saúde animal.

---

## 🤖 Inteligência Artificial: Modelo de Análise de Peso e Recomendação Nutricional

A API Python é o coração analítico da PetDex, responsável por carregar e executar o **modelo de análise de peso ideal e recomendação nutricional** que avalia o perfil do animal e sugere a ração ideal para a sua saúde e controle de peso.

### **Base de Dados: Canine Wellness Dataset**

O treinamento do modelo foi fundamentado na base de dados **[Canine Wellness Dataset (Synthetic 10k Samples)](https://www.kaggle.com/datasets/aaronisomaisom3/canine-wellness-dataset-synthetic-10k-samples)**, disponível publicamente no Kaggle.
Com **10.000 amostras simuladas** de cães, a base oferece um conjunto rico de variáveis que englobam idade, peso, nível de atividade e necessidades calóricas. Isso permitiu o desenvolvimento de uma inteligência focada no perfil fisiológico de cada animal.

### **O Modelo Escolhido: K-Nearest Neighbors (KNN)**

Após uma bateria de testes e validações envolvendo diversos algoritmos clássicos de machine learning (como SVM, Random Forest e Árvores de Decisão), o modelo **K-Nearest Neighbors (KNN)** apresentou a melhor relação entre acurácia e capacidade de generalização para classificar o perfil nutricional do cão e predizer a melhor categoria/marca de ração.

### **Como a Recomendação Funciona?**

A inteligência da PetDex atua em duas frentes combinadas:

1. **Predição com KNN (Machine Learning):**
   - A API recebe as métricas do animal (Idade, Peso Ideal, Distância de Caminhada Diária e Necessidade Calórica de Repouso - RER).
   - Esses dados são normalizados (utilizando o `scaler_knn_brand.pkl`) e submetidos ao algoritmo preditivo KNN (`modelo_knn_racao.pkl`), que avalia as características mais próximas ("vizinhos") na base de treinamento para identificar a ração mais apropriada.

2. **Avaliação Fisiológica (Lógica Especialista):**
   - Paralelamente à predição, a API compara o **peso atual** do animal com o **peso ideal** da raça.
   - O pet é classificado em três estágios corporais possíveis: **Sobrepeso**, **Peso Ideal** ou **Abaixo do Peso**.

### **Integração com o Catálogo de Rações**

O cruzamento entre a categoria de ração predita pelo modelo KNN e o diagnóstico de peso do animal alimenta um motor de busca num **Catálogo Nutricional** (`db-food.json`) validado para o sistema.
- Se o animal possui **Sobrepeso**, o sistema filtra rações voltadas para o controle de calorias (Weight Management).
- O resultado prático é entregue via API para o Aplicativo e Dashboard Web, oferecendo ao tutor sugestões reais de ração e a fundamentação do porquê aquela dieta é recomendada (ex: ganho, perda ou manutenção de peso).

### **Formatos e Persistência**

Diferente de iterações passadas (que utilizavam o padrão PMML para modelos em Java), a arquitetura atual é 100% nativa em Python.
- Os modelos e ferramentas de normalização foram exportados utilizando a biblioteca **`joblib`** (`.pkl`), garantindo máxima compatibilidade, velocidade de inferência e integração perfeita com o ecossistema `scikit-learn` / `pandas` da nossa API.

### **Documentação Completa**

Para mais detalhes sobre o processo de desenvolvimento, análise de dados e treinamento da IA, consulte os notebooks e arquivos na pasta principal:
📄 **[Aprendizagem de Maquina](../Aprendizagem%20de%20Maquina)**

---

## 🏛️ Arquitetura do Projeto (DDD)

A API Python foi estruturada seguindo os princípios do **Domain-Driven Design (DDD)** e da Arquitetura Limpa (Clean Architecture). Essa abordagem organiza o código em camadas, separando as responsabilidades e garantindo que as regras de negócio fiquem isoladas de tecnologias externas.

A estrutura do diretório `app/` está dividida nas seguintes camadas principais:

- 📁 **`domain/` (Domínio):** O núcleo da aplicação. Contém as entidades, objetos de valor e as regras de negócio puras do sistema. Não possui dependências com frameworks externos.
- 📁 **`application/` (Aplicação):** Contém os casos de uso (Use Cases) e serviços da aplicação. Coordena o fluxo de dados entre o domínio e a infraestrutura, orquestrando as operações de análise e IA.
- 📁 **`infraestructure/` (Infraestrutura):** Lida com os detalhes técnicos e integrações externas. Inclui a comunicação com a API Java via HTTP, configuração do modelo de IA (PMML) e outras dependências de baixo nível.
- 📁 **`view/` (Apresentação/Rotas):** É a porta de entrada da API. Contém os endpoints (routers) do FastAPI, responsáveis por receber as requisições HTTP, encaminhá-las para a camada de aplicação e retornar as respostas adequadas.

Essa separação arquitetural traz inúmeros benefícios, como **alta testabilidade**, facilidade de **manutenção** e uma melhor **escalabilidade** para o crescimento do projeto.

---

## 🔬 Conectando a Ciência de Dados à Saúde do Seu Pet

O verdadeiro poder desta API está em como suas funcionalidades se traduzem em recursos visuais e práticos para o usuário. Cada cálculo tem um propósito: dar ao dono do pet a tranquilidade e as informações necessárias para tomar decisões importantes.

### **Dashboard de Saúde: Análises Estatísticas Completas**

A API fornece análises estatísticas detalhadas dos batimentos cardíacos do pet, incluindo média, moda, mediana e desvio padrão. Esses dados são apresentados de forma visual e intuitiva no aplicativo.

<p align="center">
  <img src="../docs/img/tela2.gif" alt="Dashboard de Saúde no App" width="250px" />
</p>
<p align="center">
  <em><b>Tela de Saúde:</b> Exibe a média de batimentos diários, gráficos por data e análises estatísticas completas referentes ao último batimento registrado.</em>
</p>

### **Análise de Probabilidade: Cuidado Proativo e Inteligente**

Uma das ferramentas mais importantes da API é a **análise de probabilidade do último batimento cardíaco coletado**. Utilizando a distribuição normal dos dados históricos do pet, a API calcula se o batimento atual está dentro do esperado ou se é um valor estatisticamente atípico.

**Como funciona:**

- 📊 A API analisa o **último batimento cardíaco** registrado pela coleira
- 🧮 Compara com o **histórico completo** de batimentos do animal
- 📈 Calcula a **probabilidade** desse valor ocorrer usando distribuição normal
- ⚠️ Informa ao tutor se o batimento está **dentro do esperado** ou se é **atípico**

Ao identificar um batimento com baixa probabilidade de ocorrência, o tutor é alertado, o que pode **antecipar uma visita ao veterinário e, em casos extremos, salvar a vida do animal**.

<p align="center">
  <img src="../docs/img/tela1.gif" alt="Tela Inicial com Análise de Batimento" width="250px" />
</p>
<p align="center">
  <em><b>Tela Inicial:</b> Mostra a última localização e o batimento cardíaco mais recente do pet, além de um gráfico com as médias das últimas horas registradas.</em>
</p>

### **Controle de Peso e Recomendação de Ração: Dieta Sob Medida**

Para auxiliar no bem-estar do animal, a API analisa o peso e as necessidades calóricas do pet, fornecendo recomendações de ração para o controle do peso.

<p align="center">
  <img src="../docs/img/tela5.jpeg" alt="Tela de Análise de Peso e Recomendação no App" width="250px" />
</p>
<p align="center">
  <em><b>Tela de Análise de Peso e Recomendação:</b> Exibe a análise de peso e sugere opções e a quantidade de ração adequada para manter a saúde do animal.</em>
</p>

---


### **📋 Rotas Disponíveis**

Cada endpoint abaixo tem um propósito claro, alimentando uma parte específica da interface do usuário no aplicativo mobile:

| Rota | Método | Descrição | Autenticação |
|:-----|:-------|:----------|:-------------|
| `/health` | GET | Verifica se a API está online e funcionando | ❌ Não requer |
| `/batimentos` | GET | Retorna todos os batimentos cardíacos coletados do animal | ✅ Requer JWT |
| `/batimentos/estatisticas` | GET | Fornece estatísticas completas (média, moda, mediana, desvio padrão, probabilidade do último batimento) | ✅ Requer JWT |
| `/batimentos/media-por-data` | GET | Calcula a média de batimentos em um intervalo de datas específico | ✅ Requer JWT |
| `/batimentos/media-ultimos-5-dias` | GET | Retorna a média diária dos últimos 5 dias (alimenta o gráfico da tela de saúde) | ✅ Requer JWT |
| `/batimentos/media-ultimas-5-horas-registradas` | GET | Retorna a média das últimas 5 horas de coleta (alimenta o gráfico da tela inicial) | ✅ Requer JWT |

### **🎯 Principais Funcionalidades por Endpoint**

**`/batimentos/estatisticas`** - Dashboard de Saúde

Este é o endpoint mais completo da API, fornecendo:

- 📊 **Média** de batimentos cardíacos
- 📈 **Moda** (valor mais frequente)
- 📉 **Mediana** (valor central)
- 📐 **Desvio Padrão** (variabilidade dos dados)
- ⚠️ **Probabilidade do último batimento** (indica se está dentro do esperado)

Alimenta diretamente a tela de saúde do aplicativo:

<p align="center">
  <img src="../docs/img/tela2.gif" alt="Dashboard de Saúde" width="250px" />
</p>

**`/batimentos/media-ultimos-5-dias`** - Gráfico de Tendências

Retorna a média diária dos últimos 5 dias, permitindo visualizar tendências de saúde ao longo do tempo.

**`/batimentos/media-ultimas-5-horas-registradas`** - Monitoramento em Tempo Real

Retorna a média das últimas 5 horas de coleta, exibida na tela inicial para acompanhamento rápido:

<p align="center">
  <img src="../docs/img/tela1.gif" alt="Tela Inicial" width="250px" />
</p>

---

## 🔗 Comunicação entre APIs

A **API Python se conecta diretamente à API Java** usando o cliente HTTP assíncrono `httpx`. Ela faz requisições paginadas para obter todos os dados de **batimentos cardíacos** (`GET /batimentos/animal/{id}`) armazenados no banco de dados MongoDB.

**Fluxo de Dados:**

1. 📡 **Coleira IoT** → Envia dados em tempo real via WebSocket
2. ☕ **API Java** → Recebe e armazena os dados no MongoDB
3. 🐍 **API Python** → Consulta os dados armazenados e aplica análises estatísticas e IA
4. 📱 **Aplicativo Mobile** → Exibe os insights de forma visual e intuitiva

Esses dados são transformados em `DataFrames` do Pandas, onde são limpos, processados, agrupados e analisados para gerar as estatísticas e insights apresentados ao usuário.

---

## 🔐 Configuração de Autenticação JWT

A API Python implementa autenticação baseada em **JWT (JSON Web Tokens)** e se comunica com a API Java para validar tokens e obter dados.

### **Configuração do JWT_SECRET**

⚠️ **IMPORTANTE:** A chave secreta JWT (`JWT_SECRET`) é essencial para validar os tokens de autenticação.

**Como configurar:**

1. Crie um arquivo `.env` na raiz do projeto (se ainda não existir)
2. Adicione a variável `JWT_SECRET` com a **mesma chave** configurada na API Java:

```env
JWT_SECRET=sua_chave_secreta_aqui_deve_ser_longa_e_complexa
```

**⚙️ Requisitos Importantes:**

- A chave deve ser **idêntica** à configurada na API Java para garantir compatibilidade de autenticação
- Use uma chave forte e complexa (recomendado: mínimo 32 caracteres)
- **NUNCA** compartilhe ou versione o arquivo `.env` com a chave real
- Para referência, consulte o arquivo `.env.example` no projeto

**Por que isso é necessário?**

A API Python recebe tokens JWT do aplicativo mobile e precisa validá-los. Como os tokens são gerados pela API Java, ambas as APIs devem compartilhar a mesma chave secreta (`JWT_SECRET`) para que a validação funcione corretamente.

### **Configuração da API_URL**

A API Python precisa se comunicar com a API Java para obter dados de batimentos cardíacos e movimentos.

**Como configurar:**

Adicione a variável `API_URL` no arquivo `.env` com o endpoint da API Java:

```env
# Para desenvolvimento local
API_URL=http://localhost:8080

# Para produção (servidor Google Cloud)
API_URL=http://34.24.9.134:8080
```

**O que é a API_URL?**

- É o endereço base da API Java
- A API Python usa essa URL para fazer requisições HTTP para endpoints como:
  - `GET /batimentos/animal/{id}` - Obter batimentos cardíacos
  - `GET /movimentos/animal/{id}` - Obter dados de movimento
- Certifique-se de que a API Java está acessível nesse endereço

---

## 📁 Como Executar Localmente

### **📋 Pré-requisitos**

Antes de executar a API Python, certifique-se de ter instalado:

* **Python 3.11** ou superior
  - [Download do Python](https://www.python.org/downloads/)
  - Verifique a instalação: `python --version` ou `python3 --version`
* **pip** (gerenciador de pacotes Python, geralmente incluído com Python)
  - Verifique a instalação: `pip --version`
* **Git** para clonar o repositório
* **API Java** rodando (local ou remota) para comunicação entre APIs

### **🚀 Passos para Execução**

**1. Clone o repositório:**

```bash
git clone https://github.com/FatecFranca/DSM-P4-G07-2025-1.git
cd DSM-P4-G07-2025-1/api-python
```

**2. Crie e ative um ambiente virtual:**

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar no Linux/Mac
source .venv/bin/activate

# Ativar no Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Ativar no Windows (CMD)
.venv\Scripts\activate.bat
```

**3. Configure as variáveis de ambiente:**

Crie um arquivo `.env` na raiz do projeto (copie do `.env.example`):

```bash
cp .env.example .env
```

Edite o arquivo `.env` e configure as seguintes variáveis:

```env
# Chave secreta JWT (deve ser idêntica à da API Java)
JWT_SECRET=sua_chave_secreta_aqui_deve_ser_longa_e_complexa

# URL da API Java
API_URL=http://localhost:8080

# Porta da aplicação (padrão: 8000)
PORT=8000

# ID do animal para análise (obtido da API Java)
ANIMAL_ID=seu_animal_id_aqui
```

**4. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**5. Execute a aplicação:**

```bash
# Modo desenvolvimento (com reload automático)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ou usando o script run.py
python run.py
```

**6. Acesse a aplicação:**

- **API Base:** `http://localhost:8000`
- **Documentação Swagger:** `http://localhost:8000/docs`
- **Documentação ReDoc:** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/health`

### **🔧 Comandos Úteis**

```bash
# Atualizar dependências
pip install --upgrade -r requirements.txt

# Congelar dependências atuais
pip freeze > requirements.txt

# Executar em modo produção (sem reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Executar com múltiplos workers (produção)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **🐳 Executar com Docker (Opcional)**

Se preferir usar Docker:

```bash
# Construir a imagem Docker
docker build -t petdex-api-python .

# Executar o container
docker run -p 8000:8000 --env-file .env petdex-api-python
```

### **⚙️ Configurações Adicionais**

**Porta da Aplicação:**

- A API roda por padrão na porta **8000**
- Para alterar, modifique a variável `PORT` no arquivo `.env` ou use o parâmetro `--port` no comando uvicorn

**Dependências Principais:**

- **FastAPI**: Framework web assíncrono
- **Uvicorn**: Servidor ASGI
- **Pandas**: Análise de dados
- **NumPy**: Cálculos numéricos
- **Scikit-learn**: Modelos de machine learning
- **PyPMML**: Execução de modelos PMML
- **httpx**: Cliente HTTP assíncrono

---

## 🚀 Infraestrutura de Hospedagem

A API está hospedada em um servidor **Google Cloud** com as seguintes especificações:

- **Sistema Operacional:** Ubuntu
- **Tipo de Máquina:** Standard B1ms
- **IP Público:** 34.24.9.134
- **Porta:** 8083

Esta infraestrutura garante alta disponibilidade e performance para o processamento analítico e execução do modelo de IA em tempo real.

---

## ✅ Status

🟢 **Em produção** — a API está em funcionamento e integrada com o ecossistema PetDex.