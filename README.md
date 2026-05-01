# TestesQualidade

Projeto de automação de testes dividido em dois módulos independentes: testes de API REST para o Petstore e testes E2E Web para o SauceDemo. O objetivo é demonstrar boas práticas de QA com Python, cobrindo desde a camada de API até a interface do usuário, com integração contínua via GitHub Actions.

---

## Índice

- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Configuração do ambiente](#configuração-do-ambiente)
- [Módulo de API — Petstore](#módulo-de-api--petstore)
- [Módulo Web E2E — SauceDemo](#módulo-web-e2e--saucedemo)
- [Executando os testes](#executando-os-testes)
- [Relatórios](#relatórios)
- [Pipeline CI/CD](#pipeline-cicd)

---

## Tecnologias

- **Python 3.12**
- **pytest 8.3.5** — runner de testes e gerenciamento de fixtures
- **requests 2.32** — requisições HTTP para os testes de API
- **selenium 4.27** — automação do browser para os testes E2E
- **webdriver-manager 4.0** — download automático do ChromeDriver compatível com a versão instalada do Chrome
- **pytest-html 4.1** — geração de relatórios HTML
- **python-dotenv 1.0** — carregamento de variáveis de ambiente via arquivo `.env`
- **faker 33.1** — geração de dados de teste

---

## Estrutura do projeto

```
TestesQualidade/
│
├── api/                          # Módulo de testes de API REST (Petstore)
│   ├── clients/
│   │   └── petstore_client.py   # PetstoreClient (base) + PetClient + StoreClient + UserClient
│   ├── models/
│   │   ├── pet.py               # Dataclasses Pet, Category, Tag
│   │   ├── order.py             # Dataclass Order
│   │   └── user.py              # Dataclass User
│   ├── fixtures/
│   │   ├── pet_data.json        # Payloads de entrada para testes de Pet
│   │   ├── order_data.json      # Payloads de entrada para testes de Store
│   │   └── user_data.json       # Payloads de entrada para testes de User
│   ├── tests/
│   │   ├── test_pet.py          # 19 testes — CRUD /pet e findByStatus
│   │   ├── test_store.py        # 18 testes — inventário e pedidos /store
│   │   └── test_user.py         # 18 testes — CRUD /user, login e logout
│   └── conftest.py              # Fixtures de API: pet_client, store_client, user_client
│
├── web/                          # Módulo de testes E2E Web (SauceDemo)
│   ├── pages/                    # Page Object Model
│   │   ├── base_page.py         # Classe base com métodos Selenium reutilizáveis
│   │   ├── login_page.py        # PO da tela de login
│   │   ├── inventory_page.py    # PO da listagem de produtos
│   │   ├── cart_page.py         # PO do carrinho
│   │   └── checkout_page.py     # CheckoutStepOnePage + CheckoutStepTwoPage + CheckoutCompletePage
│   ├── components/
│   │   └── header.py            # Componente do cabeçalho (menu e ícone do carrinho)
│   ├── fixtures/
│   │   └── users.json           # Credenciais e dados de checkout
│   ├── tests/
│   │   ├── test_login.py        # 10 testes — login válido, inválido e validações
│   │   ├── test_inventory.py    # 14 testes — produtos, contador do carrinho e ordenação
│   │   ├── test_cart.py         #  8 testes — conteúdo e ações do carrinho
│   │   └── test_checkout.py     # 13 testes — fluxo completo e validações de formulário
│   └── conftest.py              # Fixtures Web: page objects e estados pré-configurados
│
├── shared/                       # Código compartilhado entre módulos
│   ├── config.py                 # Leitura de variáveis de ambiente
│   └── utils/
│       └── helpers.py            # Funções utilitárias
│
├── reports/                      # Relatórios HTML gerados pelo pytest-html
│
├── .github/
│   └── workflows/
│       └── tests.yml             # Pipeline GitHub Actions
│
├── conftest.py                   # Fixtures globais: config, api_session, driver
├── pytest.ini                    # Configuração do pytest
├── requirements.txt              # Dependências do projeto
├── .env.example                  # Modelo de variáveis de ambiente
└── .gitignore
```

---

## Configuração do ambiente

### Pré-requisitos

- Python 3.12 ou superior
- Google Chrome instalado
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/TestesQualidade.git
cd TestesQualidade

# 2. Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux / macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Crie o arquivo de variáveis de ambiente
copy .env.example .env        # Windows
cp .env.example .env          # Linux / macOS
```

### Variáveis de ambiente (`.env`)

| Variável | Padrão | Descrição |
|---|---|---|
| `PETSTORE_BASE_URL` | `https://petstore.swagger.io/v2` | URL base da API Petstore |
| `SAUCEDEMO_BASE_URL` | `https://www.saucedemo.com` | URL base do SauceDemo |
| `SAUCEDEMO_USER` | `standard_user` | Usuário padrão |
| `SAUCEDEMO_PASSWORD` | `secret_sauce` | Senha padrão |
| `BROWSER` | `chrome` | Navegador (`chrome` ou `firefox`) |
| `HEADLESS` | `false` | Execução sem janela (`true` para CI/CD) |
| `IMPLICIT_WAIT` | `10` | Tempo máximo de espera implícita em segundos |

---

## Módulo de API — Petstore

Testa a API pública `https://petstore.swagger.io/v2` nos recursos Pet, Store e User.

### Arquitetura

Os testes são organizados em três camadas. Na camada de **clientes HTTP**, a classe base `PetstoreClient` encapsula a biblioteca `requests` e centraliza a URL base e os headers. As subclasses `PetClient`, `StoreClient` e `UserClient` expõem métodos de negócio como `create()`, `get()`, `update()` e `delete()`, sem que os testes conheçam detalhes de transporte. Na camada de **modelos**, os dataclasses `Pet`, `Order` e `User` representam os contratos da API com métodos `to_dict()` e `from_dict()` para serialização. Na camada de **testes**, cada arquivo cobre um recurso com classes separadas por operação CRUD.

### Cobertura dos endpoints

**Pet (`/pet`)** — criar pet com payload válido, buscar por ID existente e inexistente, atualizar e verificar persistência, remover e confirmar ausência, e buscar por status `available`, `pending` e `sold` com `@pytest.mark.parametrize`.

**Store (`/store`)** — validar shape da resposta do inventário (dict com valores inteiros), criar pedido e validar campos de retorno, buscar pedido por ID no range válido, remover pedido e confirmar ausência.

**User (`/user`)** — criar usuário, buscar por username existente e inexistente, atualizar dados, remover usuário, autenticar e verificar headers `X-Rate-Limit` e `X-Expires-After`, encerrar sessão.

### Nota sobre o Petstore público

Por ser uma API de demonstração compartilhada, alguns comportamentos divergem da spec Swagger. Testes que cobrem essas divergências foram ajustados para refletir o comportamento real sem bloquear o CI.

Endpoints que retornam 200 em vez de 400 ou 404 para entradas inválidas usam `assert response.status_code in (200, 400)` com comentário explicativo. Operações que a API aceita mas não persiste de fato, como PUT e DELETE de usuários, são marcadas com `@pytest.mark.xfail(strict=False)`, aparecendo como resultado laranja no relatório sem causar falha no pipeline.

---

## Módulo Web E2E — SauceDemo

Testa o fluxo completo da loja `https://www.saucedemo.com/` com Selenium e o padrão **Page Object Model**.

### Arquitetura — Page Object Model

Cada tela da aplicação possui sua própria classe de Page Object, isolando os seletores CSS e as interações com o Selenium dos testes. Os testes conhecem apenas métodos de negócio como `login()`, `add_to_cart()` e `proceed_to_checkout()`.

A classe `BasePage` é a raiz da hierarquia e centraliza os métodos de localização, ação e navegação. Todos os timeouts usam esperas explícitas via `WebDriverWait` de 20 segundos, evitando o uso de `time.sleep()`. O método `_find_all` retorna lista vazia em vez de lançar exceção quando nenhum elemento é encontrado, permitindo verificações de coleções vazias como carrinho vazio.

O componente `Header` é reutilizado por composição nas páginas pós-login, encapsulando o badge contador do carrinho e o menu lateral com logout, reset de estado e navegação ao inventário.

### Pages implementadas

**LoginPage** — campos de usuário e senha, botão de login, mensagem de erro com botão de fechar, verificação de URL e estado da página.

**InventoryPage** — listagem dos 6 produtos com nome e preço, botão de adicionar ou remover por produto via slug do `data-test`, adição de todos os produtos com re-busca de botões a cada iteração para evitar referências stale, e ordenação por nome e preço via `<select>`.

**CartPage** — lista de itens com nome, preço e quantidade, remoção individual ou total, navegação para checkout e retorno ao inventário.

**CheckoutStepOnePage** — formulário com first name, last name e ZIP code, botão Continue com espera inteligente que detecta tanto a navegação para o step dois quanto o aparecimento de mensagem de erro, botão Cancel.

**CheckoutStepTwoPage** — resumo com itens, subtotal, imposto e total, propriedade `total_matches_subtotal_plus_tax` que valida a matemática, botões Finish e Cancel.

**CheckoutCompletePage** — mensagem de confirmação, imagem de confirmação e botão Back Home.

### Cenários de teste

**Login (10 testes)** — login válido com redirecionamento confirmado, login inválido com verificação do texto da mensagem de erro, tentativa com usuário bloqueado, envio com campos vazios para validação de obrigatoriedade, e fechamento da mensagem de erro pelo botão X.

**Inventário e contador do carrinho (14 testes)** — carga dos 6 produtos com nomes e preços não vazios, ausência do badge antes de adicionar itens, incremento correto do badge de 0 a 6, decremento ao remover, desaparecimento ao remover o único item, e os quatro modos de ordenação verificados com `sorted()` nativo do Python.

**Carrinho (8 testes)** — item adicionado aparece com preço e quantidade corretos, dois produtos diferentes presentes, remoção de 1 item para esvaziar, remoção de 1 de 2 itens mantendo o outro, e retorno ao inventário pelo Continue Shopping.

**Checkout (13 testes)** — o teste principal percorre o fluxo completo do login até a mensagem "Thank you for your order!" com verificação em cada transição de página. Os demais testes cobrem a validação dos três campos obrigatórios do formulário, a matemática do total, o cancelamento no step dois e a navegação de retorno ao inventário após a confirmação.

### Fixtures de estado pré-configurado

A fixture `logged_in` abre o browser, realiza o login e aguarda explicitamente o carregamento completo da lista de produtos antes de retornar o `InventoryPage`. A fixture `cart_with_one_item` herda de `logged_in` e entrega um `CartPage` já com o Sauce Labs Backpack adicionado. Ambas têm escopo `function`, garantindo isolamento total entre os testes com um browser zerado por teste.

---

## Executando os testes

```bash
# Todos os testes
pytest

# Por módulo
pytest api/tests/ -v
pytest web/tests/ -v

# Por arquivo
pytest api/tests/test_pet.py -v
pytest web/tests/test_checkout.py -v

# Por marker
pytest -m api -v
pytest -m web -v
pytest -m smoke -v

# Somente o fluxo completo de compra
pytest web/tests/test_checkout.py::TestCompleteCheckoutFlow::test_full_purchase_flow_confirmation_message -v

# Modo headless
HEADLESS=true pytest web/tests/ -v
```

---

## Relatórios

O `pytest-html` gera automaticamente um relatório HTML ao final de cada execução, salvo em `reports/report.html`.

```bash
# Abrir no Windows
start reports\report.html
```

O relatório exibe resultado por teste (passed, failed, xfail), tempo de execução individual, logs capturados e traceback completo em caso de falha. Os resultados são ordenados com falhas primeiro e podem ser filtrados por tipo na interface.

---

## Pipeline CI/CD

O arquivo `.github/workflows/tests.yml` executa os testes automaticamente a cada push ou pull request para a branch `main`.

### Jobs

Dois jobs rodam em paralelo de forma independente — a falha em um não cancela o outro.

**API — Petstore** executa em `ubuntu-latest` com timeout de 15 minutos. Instala Python 3.12 com cache do pip, instala as dependências e roda os testes de API, salvando o relatório `api-test-report` como artefato mesmo em caso de falha (`if: always()`).

**Web E2E — SauceDemo (headless)** executa em `ubuntu-latest` com timeout de 30 minutos. Instala o Chrome via `browser-actions/setup-chrome`, roda os testes com `HEADLESS=true` e `IMPLICIT_WAIT=15` para compensar a latência de runners compartilhados, e salva o relatório `web-test-report` como artefato. Um terceiro artefato com screenshots de falha é gerado condicionalmente com `if: failure()`.

### Artefatos

Após cada run, os relatórios ficam disponíveis para download na aba **Actions** do repositório, na seção **Artifacts**, retidos por 14 dias.

Nenhuma variável secreta é necessária — o Petstore e o SauceDemo são serviços públicos com credenciais padrão documentadas.

---

## Contagem de testes

| Módulo | Arquivo | Testes |
|---|---|---|
| API | test_pet.py | 19 |
| API | test_store.py | 18 |
| API | test_user.py | 18 |
| Web | test_login.py | 10 |
| Web | test_inventory.py | 14 |
| Web | test_cart.py | 8 |
| Web | test_checkout.py | 13 |
| **Total** | | **100** |
