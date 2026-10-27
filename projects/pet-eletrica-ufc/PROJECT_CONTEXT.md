# Contexto do projeto

## Objetivo
Criar hardware aberto, acessível e didático que permita experimentar blocos fundamentais de computadores digitais. A primeira placa agrupará AND, OR e NOT com entradas manuais, LEDs, símbolos e tabelas verdade.

## Situação e limites do ambiente
- Em 2026-10-27, `git status` mostrou worktree limpo em `main`, acompanhando `origin/main`; o remoto configurado é `origin`.
- SO: Debian GNU/Linux 13.7 Trixie, x86-64; Python 3.13.5.
- KiCad, `kicad-cli` e `pcbnew` estão instalados e respondem na versão 9.0.2 (`kicad-cli version` e `pcbnew.GetBuildVersion()`). A interface gráfica não foi validada, pois não há `DISPLAY` nesta sessão.
- O APT configurado oferece KiCad 9.0.2. A documentação oficial KiCad 10 confirma CLI para ERC/DRC/exportação e documentação de `pcbnew`; a versão 10 não está instalada aqui. Não misturar pacotes externos sem avaliar manutenção e compatibilidade.
- Não foram encontrados arquivos-fonte KiCad, SVGs ou imagens de referência na árvore versionada. Não há instalação adicional ou teste físico realizado.

## Decisão de automação
Arquitetura recomendada: híbrida. Scripts Python geram conteúdo repetitivo e mantêm parâmetros em uma fonte compacta; `kicad-cli` faz ERC/DRC, exporta fabricação e vistas; revisão gráfica humana/assistida ocorre em pontos de decisão visual. IPC/MCP é opcional para consultas ou edição interativa de uma sessão aberta, não a base do projeto.

| Opção | Vantagens | Limitações | Tokens (estimativa, não medição) |
|---|---|---|---|
| Python + arquivos/CLI | Determinístico, em lote, baixo contexto e fácil de versionar | API pcbnew varia; esquemático exige geração/edição de S-expressions ou outras ferramentas | Baixo após scripts reutilizáveis |
| Servidor MCP | Inspeção e edição contextual de KiCad aberto, chamadas semânticas | Maturidade e compatibilidade variáveis; chamadas numerosas podem aumentar contexto; não substitui revisão | Médio, depende da granularidade |
| Agentic GUI | Bom para inspeção visual e correções pontuais | Frágil, lento, difícil reproduzir e caro em interações | Alto para tarefas repetitivas |
| Híbrida | CLI/scripts cobrem trabalho em lote; GUI/MCP para inspeção excepcional | Exige disciplina de validação e compatibilidade explícita | Menor estimativa mantendo revisão |

Não foi feita medição de tokens nem teste de MCP. O KiCad está disponível, mas nenhum servidor MCP foi instalado nem avaliado funcionalmente nesta sessão; não é necessário para a etapa inicial, pois CLI e Python local estão disponíveis. A CLI deve ser a interface determinística para verificações e exportações. Usar IPC/MCP apenas após selecionar uma tarefa interativa concreta e testar em cópia.

## Primeiro circuito: proposta a validar
Usar 74HC08 (AND), 74HC32 (OR) e 74HC04 (inversores) em DIP, com resistores de pull-down ou pull-up para entradas sem flutuação e resistores individuais de LED. Conectar entradas ociosas dos gates a níveis definidos. Alimentação 5 V regulada. Para USB-C como fonte de 5 V, prever receptáculo USB-C sink simples com resistores Rd de 5.1 kΩ em CC1/CC2, proteção de entrada e desacoplamento; dimensionar LEDs e proteção após selecionar componentes/datasheets. Circuito ainda é proposta, não projeto validado.

## Identidade visual
Nenhum SVG ou referência visual veio na árvore versionada. Cores e marca oficial não podem ser inferidas; aguardar ativos PET para fechar padrão. O README em `identity/` marca essa ausência sem criar logotipo substituto.

## Critério de liberação
Não chamar o projeto de funcional/fabricável até haver projeto fonte, ERC/DRC reais, conferência elétrica independente, visualização 2D/3D, exports Gerber/drill revisados e BOM. Teste físico é etapa separada. No estado atual, existem somente requisitos preliminares e documentação; a placa não foi desenhada.
