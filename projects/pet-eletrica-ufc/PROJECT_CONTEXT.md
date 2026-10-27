# Contexto do projeto

## Objetivo
Criar hardware aberto, acessível e didático que permita experimentar blocos fundamentais de computadores digitais. A primeira placa agrupará AND, OR e NOT com entradas manuais, LEDs, símbolos e tabelas verdade.

## Situação e limites do ambiente
- Em 2026-10-27, `git status` mostrou worktree limpo em `main`, acompanhando `origin/main`; o remoto configurado é `origin`.
- SO: Debian GNU/Linux 13.7 Trixie, x86-64; Python 3.13.5.
- KiCad, `kicad-cli` e `pcbnew` estão instalados e respondem na versão 9.0.2 (`kicad-cli version` e `pcbnew.GetBuildVersion()`). A interface gráfica não foi validada, pois não há `DISPLAY` nesta sessão.
- O APT configurado oferece KiCad 9.0.2. A documentação oficial KiCad 10 confirma CLI para ERC/DRC/exportação e documentação de `pcbnew`; a versão 10 não está instalada aqui. Não misturar pacotes externos sem avaliar manutenção e compatibilidade.
- No inventário inicial não havia fontes KiCad ou ativos visuais. Durante o trabalho apareceu `identity/logos/pet_logo.png` (272 × 182 px); o original foi preservado e copiado para `projects/pet-eletrica-ufc/assets/logos/`. Não há SVG/manual de marca. Nenhuma instalação adicional ou teste físico foi realizado.

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
Topologia da placa: duas chaves momentâneas ativas em nível alto (A e B) comandam SN74HC08 (`Y_AND=A·B`), SN74HC32 (`Y_OR=A+B`) e SN74HC04 (`Y_NOT=¬A`), cada saída com LED indicador. Entradas usam pull-down de 10 kΩ; entradas de gates não usados estão ligadas a GND e suas saídas sem uso marcadas NC; cada CI tem capacitor local de 100 nF. Os três datasheets TI confirmam operação entre 2 e 6 V e opção PDIP-14 ([HC08](https://www.ti.com/lit/ds/symlink/sn74hc08.pdf), [HC32](https://www.ti.com/lit/ds/symlink/sn74hc32.pdf), [HC04](https://www.ti.com/lit/ds/symlink/sn74hc04.pdf)). LEDs Vishay TLHR5200 têm resistores série de 1,5 kΩ ±5%; com entrada de 5,0 V ±5%, corrente máxima em curto no LED é 5,25 V / 1,425 kΩ = 3,69 mA, abaixo dos 4 mA usados pela TI na caracterização do HC04 a VCC=4,5 V. A entrada é conector THT de dois pinos para fonte regulada de 5 V limitada em corrente, com 1N5819 em série para proteger contra inversão de polaridade. USB-C foi avaliado e rejeitado nesta revisão por exigir Rd separado em CC1/CC2 e proteção adicional em componente SMD difícil de soldar à mão; a opção THT atende melhor ao objetivo de montagem didática. O diodo não protege contra sobretensão sustentada nem substitui fusível.

O esquemático KiCad foi gerado por `scripts/generate_schematic.py`. Em 2026-10-27, KiCad 9.0.2 exportou a netlist, passou ERC sem violações, e o script `scripts/check_logic_gates_netlist.py` confirmou os mapeamentos críticos. A PCB preliminar foi gerada com `scripts/generate_logic_gates_pcb.py`; seu relatório DRC registra zero violações geométricas e 54 pads ainda sem conexão. Portanto, o layout não está roteado nem fechado. O ERC cobre apenas regras interpretadas do esquemático; nenhuma validação elétrica de PCB ou teste físico foi feito.

## Identidade visual
O PNG fornecido mostra a marca PET em azul índigo próximo de `#150077` sobre transparência. Esse valor foi amostrado da imagem, não confirmado por manual de marca. O PNG de origem permanece preservado; uma cópia para o projeto está em `assets/logos/`. Não há SVG nem especificação de cores oficial. A arte de serigrafia ainda não foi criada.

## Critério de liberação
Não chamar o projeto de funcional/fabricável até haver projeto fonte, ERC/DRC reais, conferência elétrica independente, visualização 2D/3D, exports Gerber/drill revisados e BOM. Teste físico é etapa separada. No estado atual há um esquemático KiCad com ERC sem violações, BOM exportado e PCB preliminar sem violações geométricas, mas com 54 pads sem conexão. DRC sem violações geométricas não demonstra conectividade concluída. Não existem exports de fabricação e o teste físico não foi realizado.
