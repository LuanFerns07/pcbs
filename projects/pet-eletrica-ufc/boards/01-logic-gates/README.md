# Placa 01: Portas lógicas

Status: esquemático KiCad gerado em `01-logic-gates.kicad_sch`; ERC executado no KiCad 9.0.2 com zero violações. A lista de materiais em [`BOM.csv`](BOM.csv) foi exportada do esquemático. Há um layout preliminar KiCad com footprints e contorno; o DRC geométrico reporta zero violações e 54 pads sem conexão. Roteamento, revisão física, imagens 3D e fabricação continuam pendentes.

## Função planejada

Dois botões momentâneos produzem sinais ativos em nível alto `A` e `B`. Três saídas independentes são exibidas por LEDs:

| Saída | Função | Entradas |
|---|---|---|
| `Y_AND` | AND | `A`, `B` |
| `Y_OR` | OR | `A`, `B` |
| `Y_NOT` | NOT | `A` |

Cada entrada terá resistor de pull-down para garantir nível baixo com o botão solto. A implementação preliminar usa SN74HC08, SN74HC32 e SN74HC04 em DIP-14, com as entradas dos gates não utilizados fixadas em GND e capacitor cerâmico de desacoplamento junto a cada CI. A entrada de alimentação escolhida é um conector THT de dois pinos para 5 V regulados, seguido por um diodo Schottky 1N5819 em série para evitar danos por inversão de polaridade. Exigir fonte regulada com limitação de corrente; a placa não terá proteção para sobretensão sustentada. Corrente dos LEDs será limitada individualmente e mantida abaixo de 4 mA por saída.

Os três componentes lógicos aceitam 2–6 V e possuem encapsulamento PDIP-14 segundo as folhas de dados da [TI para SN74HC08](https://www.ti.com/lit/ds/symlink/sn74hc08.pdf), [SN74HC32](https://www.ti.com/lit/ds/symlink/sn74hc32.pdf) e [SN74HC04](https://www.ti.com/lit/ds/symlink/sn74hc04.pdf). A folha do HC04 especifica níveis de saída a 4 mA com VCC=4,5 V. Cada LED TLHR5200 tem resistor de 1,5 kΩ ±5%; com entrada limitada a 5,25 V no pior caso, até um LED em curto ficaria limitado a 5,25 V / 1,425 kΩ = 3,69 mA, abaixo dos 4 mA usados na caracterização do HC04. Em uso normal, a queda direta do LED reduz ainda mais essa corrente. A [folha TLHR5200 da Vishay](https://www.vishay.com/docs/83011/tlhr5200.pdf) especifica LED vermelho de 5 mm, com Vf típico de 2 V a 20 mA; 1,5 kΩ dá corrente típica estimada de até 2,2 mA sem considerar a queda no diodo de entrada.

A alternativa USB-C foi avaliada: um sink reversível requer resistores `Rd` independentes em CC1 e CC2, e a proteção de sobretensão exigiria componente SMD de soldagem menos acessível; a placa didática prioriza entrada THT polarizada. O [USB-IF Type-C Specification, Release 2.0](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf) descreve esses requisitos de CC e também exige que o sink respeite a corrente anunciada pela fonte. As chaves são Omron B3F-4050 em footprints B3F THT; o diodo 1N5819 THT protege contra polaridade invertida. A entrada deve ser 5,0 V regulada (4,75–5,25 V) e limitada em corrente; essa placa não protege de sobretensão sustentada.

## Pendências de engenharia

- Confirmar disponibilidade local dos part numbers especificados e fechar a versão final de passivos e conector THT.
- A alimentação aceita somente 5 V regulados de fonte com limitação de corrente. O diodo em série protege inversão de polaridade; ele não substitui fusível nem proteção contra sobretensão sustentada.
- Revisar conectividade e footprints na PCB, definir contorno e roteamento, executar DRC, produzir renderizações 2D/3D e revisar exports Gerber/drill.
- Os relatórios estão em [`reports/ERC.rpt`](reports/ERC.rpt) e [`reports/DRC.rpt`](reports/DRC.rpt). O ERC confirma as regras elétricas interpretadas do esquemático. O DRC sem violações geométricas não elimina os 54 pads ainda sem conexão. Não há roteamento concluído, Gerbers, arquivos de furação ou teste físico.

Ver decisões elétricas e limites gerais em [`../../PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md).
