# Contexto do projeto

## Objetivo
Criar hardware aberto, acessível e didático que permita experimentar blocos fundamentais de computadores digitais. A primeira placa agrupará AND, OR e NOT com entradas manuais, LEDs, símbolos e tabelas verdade.

## Situação e limites do ambiente
- SO detectado: Debian 13.7 Trixie, x86-64; kernel 6.12.113.
- Python: `/usr/bin/python3`, versão 3.13.5.
- KiCad/`kicad-cli`: ausentes; módulo Python `pcbnew`: ausente.
- APT configurado: candidato KiCad 9.0.2+dfsg-1.
- Página oficial consultada indica KiCad 10.0.6 estável (consulta em 2026-10-27).
- Diretório inicialmente não era um repositório Git válido e não continha ativos visuais.
- Sem privilégio administrativo nesta sessão; instalação não executada.

## Decisão de automação
Arquitetura recomendada: híbrida. Scripts Python geram conteúdo repetitivo e mantêm parâmetros em uma fonte compacta; `kicad-cli` faz ERC/DRC, exporta fabricação e vistas; revisão gráfica humana/assistida ocorre em pontos de decisão visual. IPC/MCP é opcional para consultas ou edição interativa de uma sessão aberta, não a base do projeto.

| Opção | Vantagens | Limitações | Tokens (estimativa, não medição) |
|---|---|---|---|
| Python + arquivos/CLI | Determinístico, em lote, baixo contexto e fácil de versionar | API pcbnew varia; esquemático exige geração/edição de S-expressions ou outras ferramentas | Baixo após scripts reutilizáveis |
| Servidor MCP | Inspeção e edição contextual de KiCad aberto, chamadas semânticas | Maturidade e compatibilidade variáveis; chamadas numerosas podem aumentar contexto; não substitui revisão | Médio, depende da granularidade |
| Agentic GUI | Bom para inspeção visual e correções pontuais | Frágil, lento, difícil reproduzir e caro em interações | Alto para tarefas repetitivas |
| Híbrida | CLI/scripts cobrem trabalho em lote; GUI/MCP para inspeção excepcional | Exige disciplina de validação e compatibilidade explícita | Menor estimativa mantendo revisão |

Não foi feita medição de tokens nem teste de MCP. Projetos atuais encontrados para investigação: NiRuLabs (roteamento via IPC, captura esquemática experimental) e Seeed-Studio (análise/edição declarada para KiCad 9+; captura via manipulação S-expression). Não instalar agora: KiCad sequer está disponível no ambiente e a interface IPC depende de versão/sessão compatível.

## Primeiro circuito: proposta a validar
Usar 74HC08 (AND), 74HC32 (OR) e 74HC04 (inversores) em DIP, com resistores de pull-down ou pull-up para entradas sem flutuação e resistores individuais de LED. Conectar entradas ociosas dos gates a níveis definidos. Alimentação 5 V regulada. Para USB-C como fonte de 5 V, prever receptáculo USB-C sink simples com resistores Rd de 5.1 kΩ em CC1/CC2, proteção de entrada e desacoplamento; dimensionar LEDs e proteção após selecionar componentes/datasheets. Circuito ainda é proposta, não projeto validado.

## Identidade visual
Nenhum SVG ou referência visual veio no diretório. Cores e marca oficial não podem ser inferidas; aguardar ativos PET para fechar padrão. Criar sistema reutilizável em `identity/` sem fabricar logotipo substituto.

## Critério de liberação
Não chamar o projeto de funcional/fabricável até haver projeto fonte, ERC/DRC reais, conferência elétrica independente, visualização 2D/3D, exports Gerber/drill revisados e BOM. Teste físico é etapa separada.
