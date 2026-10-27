# Placa 01: Portas lógicas

## Função planejada

Dois botões momentâneos produzem sinais ativos em nível alto `A` e `B`. Três saídas independentes são exibidas por LEDs:

| Saída | Função | Entradas |
|---|---|---|
| `Y_AND` | AND | `A`, `B` |
| `Y_OR` | OR | `A`, `B` |
| `Y_NOT` | NOT | `A` |

Cada entrada terá resistor de pull-down para garantir nível baixo com o botão solto. A implementação preliminar usa SN74HC08, SN74HC32 e SN74HC04 em DIP-14, com as entradas dos gates não utilizados fixadas em GND e capacitor cerâmico de desacoplamento junto a cada CI. A entrada de alimentação escolhida é um conector THT de dois pinos para 5 V regulados, seguido por um diodo Schottky 1N5819 em série para evitar danos por inversão de polaridade. Exigir fonte regulada com limitação de corrente; a placa não terá proteção para sobretensão sustentada. Corrente dos LEDs será limitada individualmente e mantida abaixo de 4 mA por saída.

Os três componentes lógicos aceitam 2–6 V e possuem encapsulamento PDIP-14 segundo as folhas de dados da [TI para SN74HC08](https://www.ti.com/lit/ds/symlink/sn74hc08.pdf), [SN74HC32](https://www.ti.com/lit/ds/symlink/sn74hc32.pdf) e [SN74HC04](https://www.ti.com/lit/ds/symlink/sn74hc04.pdf). A folha do HC04 especifica níveis de saída a 4 mA com VCC=4,5 V; esse limite orienta o teto preliminar de corrente dos LEDs, não substitui o dimensionamento final com o LED e resistor escolhidos. A alternativa USB-C foi avaliada: um sink reversível requer resistores `Rd` independentes em CC1 e CC2, e a proteção de sobretensão exigiria componente SMD de soldagem menos acessível; a placa didática prioriza entrada THT polarizada. O [USB-IF Type-C Specification, Release 2.0](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf) descreve esses requisitos de CC e também exige que o sink respeite a corrente anunciada pela fonte.

## Pendências de engenharia

- Confirmar part numbers de LED, passivos e conector THT; a proteção contra polaridade reversa está preliminarmente especificada com 1N5819 (THT).
- A alimentação aceita somente 5 V regulados de fonte com limitação de corrente. O diodo em série protege inversão de polaridade; ele não substitui fusível nem proteção contra sobretensão sustentada.
- Construir e revisar o esquemático, conferir conectividade, ERC, footprints, contorno, roteamento, DRC, renderização 2D/3D e exportações.
- Nenhum arquivo KiCad, relatório ERC/DRC, BOM final ou arquivo de fabricação foi gerado até agora. Este texto registra uma especificação preliminar, não um projeto validado.

Ver decisões elétricas e limites gerais em [`../../PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md).
