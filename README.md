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
------------------------------------------------------------------------------------------------------------
