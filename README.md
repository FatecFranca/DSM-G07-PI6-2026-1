<p align="center">
  <img src="docs/img/capa-dex.svg" alt="Capa do Projeto" width="100%" />
</p>

# 🐾 PetDex

Repositório do **Grupo 07** do Projeto Interdisciplinar do **5º semestre** do curso de **Desenvolvimento de Software Multiplataforma - DSM** (Turma 2025/2).

---

## 🎬 Veja o vídeo do projeto

<p align="center">
  <a href="https://www.youtube.com/watch?v=9IwRMAMUHo0">
    <img src="https://img.youtube.com/vi/9IwRMAMUHo0/0.jpg" alt="Assista ao vídeo no YouTube" width="560" />
  </a>
</p>

📺 [Clique aqui para assistir ao vídeo](https://www.youtube.com/watch?v=9IwRMAMUHo0)

---

## 👨‍💻 Integrantes

- **Felipe Avelino Pedaes**  
- **Gabriel Resende Spirlandelli**  
- **Henrique Almeida Florentino**  
- **Luiz Felipe Vieira Soares**

---

## 🔗 Acesso ao Projeto

* **🎨 FIGMA:** [Protótipo da Interface](https://www.figma.com/design/BZOrhXmiYHgesIZf1Ex3Pw/PetDex.?node-id=0-1&t=8nuIhASiCYaiae4f-1)
* **🐍 API de Análise (FastAPI - Python):** [http://34.24.9.134:8083/docs](http://34.24.9.134:8083/docs)
* **☕ API Principal (Java - Spring Boot):** [http://34.24.9.134:8080/swagger](http://34.24.9.134:8080/swagger)
* **📱 Download do APK (Android):** [Baixar PetDex APK](https://drive.google.com/file/d/1qfmFwAp55BwcIVp8BA7cER1gD2TSqYkW/view?usp=sharing)

### **🔑 Credenciais de Teste**

Para testar a plataforma, utilize as seguintes credenciais:

```json
{
  "email": "henriquealmeidaflorentino@gmail.com",
  "senha": "senha123"
}
```

### **⚠️ Limitação Atual - Usuário de Teste**

**AVISO IMPORTANTE:** No momento, quando um novo usuário é cadastrado e um animal também é cadastrado, o aplicativo **não carregará corretamente** devido à falta de conexão com a coleira física.

**Por que essa limitação existe?**

O aplicativo depende de dados enviados pela coleira física (batimentos cardíacos, localização GPS, movimento). Sem uma coleira conectada ao animal cadastrado, o aplicativo não receberá dados e não funcionará corretamente.

**Solução para Testes:**

Utilize as credenciais acima (`henriquealmeidaflorentino@gmail.com` / `senha123`) que já possuem um animal cadastrado e conectado à coleira, permitindo acesso completo a todas as funcionalidades com dados reais.

---

## 📖 Sobre o Projeto

O **PetDex** é uma solução **IoT + Mobile + IA** desenvolvida para o **monitoramento em tempo real da saúde e segurança de cães e gatos**.

A plataforma combina uma **coleira inteligente** equipada com sensores de batimentos cardíacos, movimentação e localização GPS com um **aplicativo móvel multiplataforma**, permitindo que o tutor acompanhe o bem-estar do animal 24h por dia.

<p align="center">
  <img src="./docs/img/petdex-coleira-1.jpg" alt="Coleira PetDex" width="100%" />
</p>

<p align="center">
  <img src="./docs/img/petdex-coleira-2.jpg" alt="Coleira PetDex - 2" width="49%" />
  <img src="./docs/img/petdex-coleira-3.jpg" alt="Coleira PetDex - 3" width="49%" />
</p>

O sistema coleta dados em tempo real e envia para o backend em nuvem, que processa e analisa essas informações com **inteligência artificial** para detectar alterações fisiológicas, prevenir doenças e notificar o tutor em caso de risco ou fuga.

A solução visa **prevenção, segurança e cuidado contínuo**, fortalecendo o vínculo entre humanos e seus pets.

---

## 📱 Nossa Plataforma

O **aplicativo PetDex**, desenvolvido em **Flutter**, entrega uma experiência completa e intuitiva para acompanhar a rotina do animal.

### **Principais Funcionalidades**

<p align="center">
  <img src="./docs/img/tela1.gif" alt="Tela Inicial do App" width="250px" />
</p>
<p align="center">
  <em><b>Tela Inicial (Figura 9a):</b> mostra a última localização e o batimento cardíaco mais recente do pet, além de um gráfico com as médias das últimas horas.</em>
</p>

---

<p align="center">
  <img src="./docs/img/tela2.gif" alt="Tela de Saúde" width="250px" />
</p>
<p align="center">
  <em><b>Tela de Saúde (Figura 9b):</b> exibe a média de batimentos diários, por data e análises estatísticas referente ao último batimento registrado.</em>
</p>

---

<p align="center">
  <img src="./docs/img/tela3.gif" alt="Tela de Checkup" width="250px" />
</p>
<p align="center">
  <em><b>Tela Checkup Inteligente (Figura 9c):</b> o tutor responde sintomas observados, e a IA da PetDex sugere possíveis condições com base nos dados coletados mas sem emitir diagnósticos, apenas orientações preventivas.</em>
</p>

---

<p align="center">
  <img src="./docs/img/tela4.gif" alt="Tela de Localização" width="250px" />
</p>
<p align="center">
  <em><b>Tela de Localização (Figura 9d):</b> mostra o mapa em tempo real e permite configurar uma <b>área segura</b>. O app envia alertas automáticos caso o pet saia ou retorne ao perímetro.</em>
</p>

---

## 📊 Análises Avançadas

A **API analítica (Python/FastAPI)** fornece endpoints que processam e interpretam os dados recebidos da coleira, incluindo:

- Estatísticas descritivas (média, moda, mediana, desvio padrão)
- Correlações entre movimento e batimentos cardíacos
- Previsões de batimentos futuros via **modelo de regressão linear**
- Status geral de saúde e alertas de anomalias

Esses resultados alimentam os dashboards do aplicativo, oferecendo uma visão clara e personalizada do comportamento e condição do pet.

---

## 🧠 Arquitetura da Solução

A PetDex foi desenvolvida com uma **arquitetura modular e distribuída**, dividida em três pilares:

### **1️⃣ Hardware (IoT) – Coleira Inteligente**

* **Microcontrolador:** ESP32 S3 Zero (Wi-Fi e Bluetooth)
* **Sensores:**
  - GY-MAX30102 → Batimentos cardíacos e oxigenação do sangue  
  - MPU6050 → Movimento e postura  
  - NEO-6M → Localização GPS  
* **Prototipagem:** Case em **impressão 3D (PLA)**, leve e ergonômico
* **Testes práticos:** realizados com o cão **Uno**, confirmando conforto e adaptação

---

### **2️⃣ Backend e Infraestrutura**

* **API Principal:** Java 21 + Spring Boot
  - Padrão **Domain-Driven Design (DDD)**
  - Persistência com **MongoDB** (séries temporais)
  - Documentação com **Swagger/OpenAPI**
  - Autenticação via **JWT (JSON Web Tokens)**

* **API Analítica:** Python 3.11 + FastAPI
  - Processamento estatístico e aprendizado de máquina
  - Bibliotecas: Pandas, NumPy, SciPy, Scikit-learn
  - Modelo de classificação **CART (Árvore de Decisão)** em formato PMML
  - Execução assíncrona com **Uvicorn**

* **Hospedagem:** Servidor Azure
  - Sistema Operacional: **Ubuntu**
  - Tipo de Máquina: **Standard B1ms**
  - APIs acessíveis via IP público

* **Containerização e Orquestração:**
  - **Docker**: Cada API é containerizada em sua própria imagem Docker
  - **Docker Compose**: Orquestração de múltiplos containers (API Java, API Python)
  - Rede interna (`petdex-network`) para comunicação entre containers
  - Volumes persistentes para armazenamento de dados

---

## 🚀 Infraestrutura e Deploy

### **☁️ Hospedagem na Microsoft Azure**

O projeto PetDex está hospedado na **Microsoft Azure**, utilizando uma máquina virtual com as seguintes especificações:

- **Sistema Operacional:** Ubuntu Server
- **Tipo de Máquina:** Standard B1ms
- **IP Público:** 34.24.9.134
- **Região:** East US

### **🐳 Containerização com Docker**

Toda a infraestrutura backend é containerizada usando **Docker**, garantindo:

- **Portabilidade:** Mesma configuração em desenvolvimento e produção
- **Isolamento:** Cada serviço roda em seu próprio container
- **Escalabilidade:** Fácil replicação e balanceamento de carga
- **Consistência:** Ambiente idêntico em qualquer máquina

**Estrutura de Containers:**

```yaml
services:
  api-java:
    - Porta: 8080
    - Imagem: petdex/api-java:main
    - Rede: petdex-network

  api-python:
    - Porta: 8083
    - Imagem: petdex/api-python:main
    - Rede: petdex-network
```

### **🔄 Orquestração com Docker Compose**

O **Docker Compose** gerencia múltiplos containers e suas dependências:

- **Rede Interna:** Containers se comunicam através da rede `petdex-network`
- **Variáveis de Ambiente:** Configurações sensíveis (JWT_SECRET, DATABASE_URI) via `.env`
- **Restart Automático:** Containers reiniciam automaticamente em caso de falha
- **Volumes Persistentes:** Dados importantes são mantidos mesmo após restart

**Como executar localmente com Docker Compose:**

```bash
# Clone o repositório
git clone https://github.com/FatecFranca/DSM-P4-G07-2025-1.git
cd DSM-P4-G07-2025-1

# Configure o arquivo .env
cp .env.example .env

# Inicie todos os serviços
docker-compose up -d

# Visualize os logs
docker-compose logs -f

# Pare todos os serviços
docker-compose down
```

### **⚙️ CI/CD - Deploy Automático**

O projeto implementa um pipeline de **CI/CD (Continuous Integration/Continuous Deployment)** para automatizar o processo de deploy:

**Fluxo de Deploy:**

1. **Commit/Push:** Desenvolvedor faz push para o repositório GitHub
2. **Build Automático:** GitHub Actions detecta mudanças e inicia o build
3. **Criação de Imagens Docker:** Novas imagens são construídas automaticamente
4. **Push para Registry:** Imagens são enviadas para o Docker Hub/Registry
5. **Deploy no Servidor:** Servidor Azure puxa as novas imagens e reinicia os containers
6. **Verificação:** Health checks garantem que os serviços estão funcionando

**Benefícios:**

- ✅ Deploy rápido e confiável
- ✅ Redução de erros humanos
- ✅ Rollback fácil em caso de problemas
- ✅ Histórico completo de deploys

### **📡 Informações do Servidor**

**IP do Servidor Azure:** `34.24.9.134`

**Endpoints das APIs:**

| Serviço | URL Base | Documentação | Porta |
|:--------|:---------|:-------------|:------|
| **API Java** | `http://34.24.9.134:8080` | [Swagger](http://34.24.9.134:8080/swagger) | 8080 |
| **API Python** | `http://34.24.9.134:8083` | [Docs](http://34.24.9.134:8083/docs) | 8083 |
| **WebSocket** | `ws://34.24.9.134:8080/ws-petdex` | - | 8080 |

**Rotas Principais:**

**API Java (Spring Boot):**
- `POST /auth/login` - Autenticação de usuários
- `GET /animais/{id}` - Consultar dados do animal
- `GET /batimentos/animal/{id}` - Histórico de batimentos cardíacos
- `GET /localizacoes/animal/{id}` - Histórico de localizações
- `WS /ws-petdex` - Conexão WebSocket para dados em tempo real

**API Python (FastAPI):**
- `GET /batimentos/estatisticas` - Estatísticas de batimentos
- `GET /batimentos/media-ultimos-5-dias` - Média diária dos últimos 5 dias
- `GET /batimentos/probabilidade?valor=XX` - Probabilidade de um batimento
- `GET /batimentos/regressao` - Análise de regressão linear
- `GET /health` - Status da API

---

### **3️⃣ Aplicativo Mobile**

* **Framework:** Flutter  
* **Recursos:**  
  - Monitoramento em tempo real  
  - Dashboards de saúde  
  - Checkup inteligente com IA  
  - Notificações e alertas de fuga  
  - Mapa interativo (Google Maps API)

---

## 🔐 Sistema de Autenticação JWT

A PetDex implementa um sistema robusto de autenticação baseado em **JWT (JSON Web Tokens)** para garantir a segurança das comunicações entre os componentes da plataforma.

### **Como Funciona**

1. **Login do Usuário:** O usuário realiza login através do aplicativo mobile, enviando suas credenciais para a API Java
2. **Geração do Token:** A API Java valida as credenciais e gera um token JWT assinado
3. **Propagação do Token:** O token é armazenado no aplicativo e enviado em todas as requisições subsequentes
4. **Fluxo de Autenticação:** Cliente → API Python → API Java
   - O aplicativo mobile envia o token JWT para a API Python
   - A API Python valida e propaga o token para a API Java
   - A API Java valida o token e processa a requisição

### **Configuração**

Ambas as APIs (Java e Python) compartilham a mesma chave secreta JWT (`JWT_SECRET`) configurada nos arquivos `.env`, garantindo que os tokens possam ser validados em toda a infraestrutura.

---

## 🧠 Modelo de Inteligência Artificial

A PetDex utiliza um modelo de **classificação de espécies** treinado com técnicas de aprendizado de máquina para identificar se um animal é um cão ou gato com base em características físicas.

### **O Desafio: Generalista vs. Especialista**

Durante o desenvolvimento, enfrentamos uma questão estratégica: treinar um modelo **generalista** capaz de classificar 8 espécies diferentes de animais presentes no dataset, ou um modelo **especialista** focado apenas em cães e gatos?

### **Processo de Desenvolvimento**

1. **Treinamento de Múltiplos Modelos:** Foram treinados **12 modelos classificadores diferentes**, incluindo:
   - SVM (Support Vector Machine)
   - Logistic Regression
   - Árvores de Decisão (CART)
   - Random Forest
   - E outros algoritmos do Scikit-learn

2. **Exportação Universal:** Todos os modelos foram exportados para o formato **PMML (Predictive Model Markup Language)**, um padrão universal compatível com a API Python e diversas outras plataformas

### **Validação e Seleção do Modelo**

- **Cross-Validation:** Realizamos análise rigorosa com validação cruzada para avaliar a performance de cada modelo
- **Análise Visual:** Gráficos Boxplot foram gerados para comparar a distribuição de acurácia entre os modelos
- **Teste Final:** Simulação de uso real com **20 casos reais de cães e gatos**

### **O Vencedor: CART Especialista**

O modelo **CART (Classification and Regression Trees)** treinado **APENAS com dados de cães e gatos** atingiu **100% de acerto** no teste final, superando todos os modelos generalistas.

O arquivo `modelo_CART.pmml` foi escolhido como o **"cérebro" oficial da PetDex** e está integrado à API Python, sendo utilizado pelo aplicativo Flutter para realizar classificações em tempo real.

---

## 🧩 Tecnologias Utilizadas

| Camada | Tecnologias |
|:-------|:-------------|
| **Hardware (IoT)** | ESP32 S3 Zero, GY-MAX30102, MPU6050, NEO-6M, Impressão 3D (PLA) |
| **Backend** | Java + Spring Boot, MongoDB, Swagger, JWT, FastAPI (Python), Scikit-learn, PMML |
| **Frontend** | Flutter, API Google Maps |
| **Infraestrutura** | Azure (Ubuntu, Standard B1ms), arquitetura de microsserviços |

---

## 🧪 Resultados

- Integração completa entre **coleira, backend e app**
- Transmissão e análise de dados em tempo real
- Teste físico com pet real validou **ergonomia e conforto**
- Modelo preditivo funcional de frequência cardíaca
- Base pronta para futuras versões com **IA classificadora** e **telemedicina veterinária**

---

> Projeto desenvolvido como parte das atividades acadêmicas da **FATEC** – Faculdade de Tecnologia.  
> Orientado pelos princípios de inovação, prevenção e bem-estar animal 🐕💙

