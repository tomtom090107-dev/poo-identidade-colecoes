# Previsões, evidências e decisões

## Etapa 01 — reconhecer e cadastrar

| Situação | Minha previsão antes de executar | Evidência observada e explicação |
|---|---|---|
| Duas instâncias com LT-101: identidade e igualdade | `is` falso (instâncias distintas), `==` verdadeiro (mesma tag) | Confirmado: identidade distingue objetos; igualdade segue a tag como chave do domínio |
| Inserir 12% e depois 99% com a mesma tag | Segunda inserção recusada; primeira preservada | Confirmado: `inserir` devolve `false` e a leitura continua 12% |
| Buscar outra instância da mesma tag | Encontra o item (igualdade por tag) | Confirmado: `buscar` retorna a medição cadastrada |
| Buscar chave ausente e consultar leitura zero | `nullptr`/`None`, sem criar entrada; zero é valor válido de medição | Confirmado: busca ausente não cria chave; `0 %` é leitura legítima |

1. Os dois `second` do C++ vêm do par retornado por `emplace`: o primeiro é o iterador para a entrada (inserida ou já existente) e o segundo é o booleano que indica se a inserção ocorreu. O `std::map` precisa de ordem porque usa comparação (`operator<`) para localizar a chave; o `dict` do Python precisa de `hash` e `__eq__` porque usa tabela de dispersão e resolve colisões por igualdade.

2. Se cada tentativa sobrescrevesse o cadastro, o `Catalogo` deixaria de representar "primeira leitura válida" e passaria a representar "última escrita vence". Seria adequado em cache ou configuração, onde o valor mais recente substitui o anterior. No domínio de medições, sobrescrever apagaria a primeira leitura sem aviso e quebraria o requisito de preservar a cadastrada.

3. Um conjunto de tags não substitui o catálogo de medições porque armazena só a chave, não o valor associado. Hashes diferentes para objetos iguais seriam inaceitáveis: quebrariam a busca no `dict` e no `set` do Python, e a coerência com `__eq__` deixaria de existir.

## Etapa 02 — remover, consultar e pensar na memória

| Situação | Minha previsão | Evidência C++ e Python |
|---|---|---|
| Remover chave existente duas vezes | Primeira `true`, segunda `false` | Confirmado nas duas linguagens |
| Consultar 0, 2 e 100 últimas de [12, 12, 15] | 0 → vazio; 2 → [12, 15]; 100 → as três, na ordem | Confirmado; histórico original intacto |
| Limpar a coleção devolvida e consultar novamente | Histórico permanece com as três | Confirmado: `ultimas` devolve cópia independente |
| Remover cadastro e consultar histórico independente | Cadastro sai do catálogo; histórico continua com três | Confirmado: coleções distintas |

1. `ultimas` calcula o índice de corte: se `limite` for maior ou igual ao tamanho, devolve tudo; se for zero, devolve vazio; senão devolve os últimos `limite` elementos. A fronteira que mudei por linguagem: em C++ o cálculo de `inicio` evita iterador inválido quando `limite == 0`; em Python a fatia `[-limite:]` já trata o caso, mas exige `limite == 0` tratado antes porque `[-0:]` devolve a lista inteira.

2. A consulta **não** limita a memória do histórico — só devolve uma cópia dos últimos itens. Para exibir apenas os últimos dez, a consulta basta quando o histórico é pequeno e se quer manter tudo para auditoria. Seria necessário descartar dados antigos quando o histórico cresce sem limite e a memória importa. Descartar perde rastreabilidade: não há como responder depois por leituras antigas.

3. Em Python, apagar a entrada do `dict` remove a referência do catálogo. Se o chamador ainda tem o objeto em outra variável, o objeto continua vivo (contagem de referências). Se não tem, o `GC` libera. Em C++, um `T*` obtido antes de `remover` aponta para o elemento apagado do `map`; usar esse ponteiro é comportamento indefinido. O contrato de `buscar` (devolver `nullptr` quando ausente) só é seguro enquanto o item estiver no mapa.

4. Alternativa rejeitada: **retornar a coleção interna**. Ela violaria o encapsulamento — o chamador poderia mutar o estado sem passar por `inserir`/`remover`, quebrando a regra de duplicata. Seria útil em uma visão somente leitura imutável, exposta como cópia ou `const&` sem API de mutação.

## Evidências da entrega

- Comando local, resultado e commit testado: `make test ETAPA=02` → `OK etapa 02 cumulativa (C++ e Python)`.
- URL da execução de Actions desse commit: (preencher com o link da aba Actions do seu fork).
- Um diagnóstico de falha encontrado e como o corrigiu: na primeira execução do `make test ETAPA=01`, as duas linguagens reprovavam porque `inserir`/`buscar` devolviam o marcador `false`/`None`. Corrigi usando `emplace`/`find` em C++ e verificação explícita + `get` em Python.
- Limite observado dos testes: os testes cobrem contrato e fronteiras (duplicata, ausência, 0/2/100 últimas), mas não provam que o painel externo continua falando só com `Catalogo` — isso exige inspeção do diff e explicação.