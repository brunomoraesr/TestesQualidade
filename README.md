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
