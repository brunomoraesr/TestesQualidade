---Primeiro Commit v1 : Definição da Estrutura do Projeto---
  --Definir Stack e criar estruturas das pastas 
  --Decisões de design:

Camada | ->	 Motivo
clients/ separado dos tests/ ->	|Isola a lógica HTTP; testes ficam sem requests direto
models/	->	| Centraliza a forma dos dados — facilita assertions e criação de payloads
base_page.py	->	| Herança: todas as pages herdam métodos como wait_for_element, click, fill
components/	| ->	  Elementos que aparecem em múltiplas páginas (header) ficam fora dos POs
conftest.py por módulo	->	|  Fixtures de API não poluem o escopo Web e vice-versa
shared/config.py->		|Única fonte de verdade para URLs e credenciais via .env
---------------------  ----------------------------------- -----------------------------------

---Segundo Commit v2 : Configurações bases ( arquivos de configuração )---

requirements.txt — dependências exatas com versão pinada para reproducibilidade.

pytest.ini

--html=reports/report.html --self-contained-html embutido no addopts para gerar relatório automaticamente em toda execução
4 markers declarados: api, web, smoke, regression — evita o warning do pytest sobre markers desconhecidos
conftest.py (raiz) — 3 fixtures + 1 hook:

Fixture	Escopo	Motivo
config	session	Lê .env uma única vez; compartilhada por API e Web
api_session	session	Reutiliza conexão TCP entre todos os testes de API
driver	function	Browser novo por teste — garante isolamento de estado
O builder do driver usa um dict de factories para suportar Chrome/Firefox sem if/elif espalhado
--headless=new para Chrome moderno (Chromium 112+); --headless para Firefox
O hook pytest_configure injeta metadados no cabeçalho do relatório HTML
.env.example — comentado, com valores padrão que funcionam sem alterar nada para iniciar.

.gitignore — inclui .venv/, .idea/, .vscode/ além dos artefatos de teste.

---------------------  ----------------------------------- -----------------------------------
---Terceiro Commit : Criação dos tesetes da API (Petstore ) de user pet e store---
Estado final do módulo de API:


api/
├── clients/
│   └── petstore_client.py   ← PetstoreClient + PetClient + StoreClient + UserClient
├── models/
│   ├── pet.py               ← Pet + Category + Tag (dataclasses)
│   ├── order.py             ← Order (dataclass)
│   └── user.py              ← User (dataclass) — existente
├── fixtures/
│   ├── pet_data.json        ← valid_pet, updated_pet, pending_pet, statuses
│   ├── order_data.json      ← valid_order, invalid_order_id, valid_order_ids
│   └── user_data.json       ← existente
├── conftest.py              ← pet_client, store_client, user_client, 3 fixtures de data
└── tests/
    ├── test_pet.py          ← 19 testes em 5 classes
    ├── test_store.py        ← 18 testes em 4 classes
    └── test_user.py         ← 18 testes em 6 classes — existente
Destaques por módulo:

test_pet.py

TestPetFindByStatus usa @pytest.mark.parametrize nos 3 status válidos — gera 9 testes automaticamente
test_find_by_invalid_status_returns_400 valida rejeição de status desconhecido
Teste de serialização do dataclass Pet valida Category e Tag como objetos tipados
test_store.py

TestStoreInventory verifica shape da resposta (dict com valores inteiros) sem depender de contagens específicas — a API é compartilhada e os números mudam
test_get_valid_order_id_range aceita 200 ou 404 pois a API pública pode ou não ter o pedido
test_get_order_id_above_10_returns_404 cobre a regra de negócio da spec: IDs válidos são apenas 1–10

---Quarto Commit : Automação Web (SauceDemo) / Criação de Page Objects---
Hierarquia de herança:


BasePage
├── LoginPage
├── InventoryPage      (compõe Header)
├── CartPage           (compõe Header)
├── CheckoutStepOnePage (compõe Header)
├── CheckoutStepTwoPage (compõe Header)
├── CheckoutCompletePage
└── Header             (herda BasePage para reuso dos métodos _find/_click)
Decisões de design por arquivo:

Arquivo	Decisão relevante
base_page.py	_find usa visibility_of_element_located; _find_clickable usa element_to_be_clickable — esperas corretas para cada caso
header.py	Componente separado, composto por cada página que o contém — não herança, composição
login_page.py	Retorna self em cada setter para suportar encadeamento fluente
inventory_page.py	_slug() converte nome do produto para o padrão data-test da API; sort_by() aceita 'az' | 'za' | 'lohi' | 'hilo'
cart_page.py	item_prices retorna List[float] já sem o $ — pronto para assertions numéricas
checkout_page.py	3 classes no mesmo arquivo por coesão de fluxo; fill_buyer_info() como método conveniente com encadeamento; total_matches_subtotal_plus_tax encapsula a validação matemática
conftest.py	logged_in e cart_with_one_item são fixtures compostas que entregam estado pré-configurado aos testes

PRINTS DE TESTES DE LOGIN DENTRO DO TERMINAL :
<img width="1236" height="604" alt="image" src="https://github.com/user-attachments/assets/1638dbf0-5d80-41fe-a6f5-a7046a7c7ee3" />
PRINT DO RELATÓRIO DE LOGIN HTML GERADO : 
<img width="1896" height="945" alt="image" src="https://github.com/user-attachments/assets/ed729135-f4f5-4dbd-97b4-89d2448382ec" />


-------------------------- ------------------------------- --------------------------------- -------------------------------
QUINTO COMMIT : TESTES E2E ( CHROME ) USANDO AS PAGES OBJECTS CRIADAS NO QUARTO COMMIT
<img width="1216" height="281" alt="image" src="https://github.com/user-attachments/assets/b360b47f-d944-4ca9-8db6-bab63095d3a2" />
<img width="1912" height="728" alt="image" src="https://github.com/user-attachments/assets/758675d9-6b7d-461e-bb38-ed394d9e7c86" />

