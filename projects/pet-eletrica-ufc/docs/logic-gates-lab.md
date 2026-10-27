# Aula prática — portas lógicas com transistores discretos

## Objetivo

Relacionar corrente de base e saturação dos BJTs aos estados das portas AND, OR e NOT. Cada porta tem botões próprios. A placa usa 5 V regulados e sinaliza cada saída com LED vermelho.

## Antes de energizar

Consulte o [esquemático](../boards/01-logic-gates/manufacturing/schematic.pdf) e a [lista de materiais](../boards/01-logic-gates/manufacturing/BOM.csv). Identifique `J1` pino 1 `+5V`, pino 2 `GND`; diodo `D1` (faixa no cátodo); LEDs `D2`–`D4` (pad 1 cátodo); e transistores `Q1`–`Q10` (pinos 1 emissor, 2 base, 3 coletor para o 2N3904 escolhido). Verifique as folhas do lote adquirido antes da soldagem.

Meça continuidade em GND e ausência de curto entre alimentação e retorno. Use fonte de 5 V regulados com limite inicial de corrente em torno de 100 mA. Se o limite atuar, desligue e procure erro de montagem. A placa não suporta sobretensão sustentada.

## Princípio

Um botão solto deixa a entrada em 0 por pull-down de 10 kΩ. Ao pressioná-lo, ela vai a `VCC`. Q1/Q2 fazem NAND, Q5/Q6 fazem NOR; Q3 e Q7 invertem esses nós para obter AND e OR. Q9 realiza NOT diretamente. Q4, Q8 e Q10 acionam LEDs sem carregar diretamente as saídas de lógica. O valor 2,2 kΩ dos pull-ups mantém alto mesmo com a corrente de base do próximo estágio.

## Tabelas esperadas

| A_AND | B_AND | Y_AND | LED D2 |
|---:|---:|---:|---|
| 0 | 0 | 0 | apagado |
| 0 | 1 | 0 | apagado |
| 1 | 0 | 0 | apagado |
| 1 | 1 | 1 | aceso |

| A_OR | B_OR | Y_OR | LED D3 |
|---:|---:|---:|---|
| 0 | 0 | 0 | apagado |
| 0 | 1 | 1 | aceso |
| 1 | 0 | 1 | aceso |
| 1 | 1 | 1 | aceso |

| A_NOT | Y_NOT | LED D4 |
|---:|---:|---|
| 0 | 1 | aceso |
| 1 | 0 | apagado |

Na simulação simplificada, para 4,75–5,25 V em J1, as saídas baixas ficaram até 0,058 V e as altas a partir de 3,837 V. Use como critério didático medido **baixo ≤0,4 V** e **alto ≥3,5 V**. Os valores de simulação não são medições de uma placa física.

## Procedimento

1. Com todas as entradas soltas, meça a tensão em `VCC` após D1 e em cada entrada. As entradas devem estar próximas de 0 V; AND/OR apagados e NOT aceso.
2. Na região AND, pressione `SW1` e `SW2` em todas as quatro combinações. Em cada uma, meça `Y_AND` no **pad 2 de R14** com o multímetro e anote o LED D2. Solte os botões entre medições.
3. Repita com `SW3` e `SW4` para OR; meça `Y_OR` no **pad 2 de R16** e observe D3.
4. Meça `Y_NOT` no **pad 2 de R17** e observe D4 com `SW5` solto e pressionado. Confirme que os botões de outras regiões não alteram `Y_NOT`. Use ponta fina para não unir dois pads vizinhos.
5. Se houver discrepância, registre a tensão nos nós `N_AND` ou `N_OR`, as entradas, a saída e o estado do LED. Desligue a fonte antes de tocar nas soldas.

Modelo de registro:

| VIN (V) | Porta | A (V) | B (V) | Z (V) | LED | Esperado | Observação |
|---:|---|---:|---:|---:|---|---:|---|
| | AND | | | | | | |
| | OR | | | | | | |
| | NOT | | — | | | | |

## Exercícios

1. Explique por que os resistores de entrada evitam estados indefinidos.
2. Derive a tabela NAND de Q1/Q2 e mostre por que Q3 produz AND.
3. Compare NOR e OR para as quatro combinações.
4. Calcule a corrente aproximada de um pull-up de 2,2 kΩ quando seu transistor está saturado.
5. Explique por que o LED possui transistor próprio e o que ocorreria se fosse ligado diretamente ao nó lógico com um resistor pequeno.
6. Proponha um circuito para reduzir o bounce do botão se a placa fosse usada como entrada de um contador.

**Estado do laboratório:** ensaio físico ainda não realizado. ERC, DRC e simulação DC estão registrados, mas os valores de medição devem ser preenchidos após montagem do protótipo.
