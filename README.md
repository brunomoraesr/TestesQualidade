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
