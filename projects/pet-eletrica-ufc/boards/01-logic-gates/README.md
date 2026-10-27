# Placa 01: Portas lógicas

## Função planejada

Dois botões momentâneos produzem sinais ativos em nível alto `A` e `B`. Três saídas independentes são exibidas por LEDs:

| Saída | Função | Entradas |
|---|---|---|
| `Y_AND` | AND | `A`, `B` |
| `Y_OR` | OR | `A`, `B` |
| `Y_NOT` | NOT | `A` |

Cada entrada terá resistor de pull-down para garantir nível baixo com o botão solto. A implementação preliminar usa SN74HC08, SN74HC32 e SN74HC04 em DIP-14, com as entradas dos gates não utilizados fixadas em GND e capacitor cerâmico de desacoplamento junto a cada CI. A alimentação prevista é 5 V por USB-C, como sink sem USB-PD; cada pino CC do receptáculo terá seu próprio `Rd` de 5,1 kΩ, conforme USB Type-C. O sink não presumirá corrente acima do limite anunciado pela fonte; a carga prevista é apenas lógica CMOS e três LEDs de baixa corrente. Corrente dos LEDs será limitada individualmente e mantida abaixo de 4 mA por saída.

Os três componentes lógicos aceitam 2–6 V e possuem encapsulamento PDIP-14 segundo as folhas de dados da [TI para SN74HC08](https://www.ti.com/lit/ds/symlink/sn74hc08.pdf), [SN74HC32](https://www.ti.com/lit/ds/symlink/sn74hc32.pdf) e [SN74HC04](https://www.ti.com/lit/ds/symlink/sn74hc04.pdf). A folha do HC04 especifica níveis de saída a 4 mA com VCC=4,5 V; esse limite orienta o teto preliminar de corrente dos LEDs, não substitui o dimensionamento final com o LED e resistor escolhidos. O [USB-IF Type-C Specification, Release 2.0](https://www.usb.org/sites/default/files/USB%20Type-C%20Spec%20R2.0%20-%20August%202019.pdf) define `Rd` nominal de 5,1 kΩ (±20%); para receptáculo reversível, CC1 e CC2 precisam ser terminados separadamente.

## Pendências de engenharia

- Selecionar números de peça concretos para receptáculo USB-C, LEDs, resistores, capacitores e proteção de VBUS; confirmar pinagem e footprints pelos respectivos datasheets.
- Fechar proteção ESD/sobretensão e eventual fusível rearmável após definir o conector e o perfil de corrente. Não assumir capacidade de corrente USB-C anunciada sem detectar os níveis `Rp` em CC.
- Construir e revisar o esquemático, conferir conectividade, ERC, footprints, contorno, roteamento, DRC, renderização 2D/3D e exportações.
- Nenhum arquivo KiCad, relatório ERC/DRC, BOM final ou arquivo de fabricação foi gerado até agora. Este texto registra uma especificação preliminar, não um projeto validado.

Ver decisões elétricas e limites gerais em [`../../PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md).
