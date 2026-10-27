# Experimento: portas AND, OR e NOT

## Objetivo
Observar como níveis lógicos nas entradas determinam a saída de portas AND, OR e NOT.

## Tabelas-verdade

AND: 00→0, 01→0, 10→0, 11→1.  
OR: 00→0, 01→1, 10→1, 11→1.  
NOT: 0→1, 1→0.

## Entradas e saídas da placa
Os botões A e B são momentâneos e ativos em nível alto. Soltar os botões deve produzir nível lógico 0 por meio dos resistores de pull-down. As saídas planejadas são `Y_AND = A·B`, `Y_OR = A+B` e `Y_NOT = ¬A`, cada uma com LED indicador. O botão B não altera `Y_NOT`.

## Procedimento previsto
Com a placa desligada, inspecione polaridades e conexões. Conecte uma fonte regulada e limitada em corrente de 5 V à entrada identificada, respeitando a polaridade. Aplique cada combinação de entradas e registre os LEDs. Compare com as tabelas e discuta entradas flutuantes e inversão lógica. Este procedimento só deve ser executado após revisão do projeto e montagem física.

Este roteiro é preliminar: a placa ainda não foi desenhada, validada, fabricada ou montada.

## Exercícios
1. Explique por que uma entrada não pode ficar desconectada.
2. Construa a tabela de uma NAND a partir de AND e NOT.
3. Proponha uma combinação de portas que implemente XOR.
