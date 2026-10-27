# Contexto do projeto PET Engenharia Elétrica UFC

## Objetivo e estado

A placa 01 apresenta AND, OR e NOT por transistores discretos, com botões e LEDs. A revisão A foi desenvolvida no KiCad 9.0.2 instalado em 2026-10-27; KiCad 10 não estava disponível. O repositório guarda fontes editáveis, scripts determinísticos, relatórios e exports. Os resultados de ERC, DRC, paridade e simulação pertencem à revisão indicada e não representam teste físico.

## Leitura da referência e geometria

A fotografia fornecida foi preservada em `assets/reference/logic-gates-reference.png`. A placa da foto é vertical, com cantos arredondados, borda dupla fina, título no topo e três regiões separadas visualmente. Cada região tem botões à esquerda, um símbolo de porta grande no centro, LED `Z` e tabela-verdade à direita. AND ocupa o terço superior, OR o central e NOT o inferior. Os transistores aparecem dentro ou junto do símbolo, com resistores acima/abaixo. A marca PET substitui a identificação comercial da foto no rodapé da revisão.

Não há escala física na fotografia. Como aproximação, o contorno foi fixado em **123 × 155 mm**, cantos R3 mm, margens visuais de 5–8 mm. A faixa superior tem cerca de 20 mm; AND ocupa aproximadamente y=27–59 mm, OR y=69–101 mm e NOT y=113–145 mm. Os símbolos centrais se estendem aproximadamente de x=49 a 86 mm, cada tabela está em x=100–122 mm, e os botões ficam em x=13–25,5 mm. Essas dimensões são decisões de projeto, não medições da imagem.

O PNG de marca recebido está em `assets/logos/pet_logo.png`, cópia preservada de `identity/logos/pet_logo.png`. A versão monocromática `assets/logos/pet_logo_silkscreen.svg` foi traçada a partir do PNG para F.Silkscreen. Não se recebeu SVG oficial ou manual de identidade: a forma básica da marca deriva da imagem fornecida, mas a conversão e a cor observada não constituem especificação oficial. Máscara branca e silk preta devem ser escolhidas no pedido da PCB.

## Decisões elétricas

| Bloco | Transistores | Função |
|---|---|---|
| AND | Q1–Q2 em série, Q3 inversor | NAND seguido de inversão; Q4 aciona D2 |
| OR | Q5–Q6 em paralelo, Q7 inversor | NOR seguido de inversão; Q8 aciona D3 |
| NOT | Q9 emissor comum | Inversão; Q10 aciona D4 |

Os botões Omron B3F-4050 de 12 × 12 mm conectam cada entrada a `VCC` quando pressionados. Cinco resistores de 10 kΩ fazem pull-down. Outros dez resistores de 10 kΩ limitam corrente de base. Os cinco pull-ups dos nós NAND/NOR/saída valem **2,2 kΩ**: 10 kΩ deixaria a saída alta em aproximadamente metade de `VCC` por causa do resistor de base do próximo estágio. Com 2,2 kΩ e carga de base de 10 kΩ, o cálculo de primeira ordem dá `VH = (10k·VCC + 2,2k·VBE)/(12,2k)`. Para `VCC=4,3 V` e `VBE=0,65 V`, `VH≈3,64 V`. Com `VCC=5,05 V`, corrente máxima do pull-up saturado é `(5,05−0,2)/2,09k≈2,32 mA` considerando −5% no resistor. Corrente de base no estágio seguinte é da ordem de 0,28–0,35 mA, razão forçada inferior a 10 na condição calculada. Os limitadores de LED são 1,5 kΩ; a corrente simulada acesa é 1,84–2,17 mA na faixa de entrada analisada.

O [datasheet onsemi 2N3904](https://www.onsemi.com/pdf/datasheet/2n3904-d.pdf) documenta pinos **1 E, 2 B, 3 C** e ponto de caracterização de saturação `IC=10 mA, IB=1 mA, VCE(sat)≤0,2 V`. O símbolo `Q_NPN_EBC` e o footprint `TO-92_Inline` foram escolhidos para corresponder a essa ordem. O [datasheet Vishay TLHR5200](https://www.vishay.com/docs/83011/tlhr5200.pdf) informa LED vermelho de 5 mm e `VF` típico de 2 V a 20 mA. O [datasheet Omron B3F](https://components.omron.com/us-en/datasheet_pdf/A070-E1.pdf) descreve B3F-4050 e a malha de furos de 12 × 12 mm. O [datasheet Diodes 1N5819](https://www.diodes.com/datasheet/download/1N5819.pdf) identifica o cátodo pela faixa. O 1N5819 foi posto em série com J1 para bloquear inversão de polaridade; C1=100 nF desacopla VCC. Não há proteção contra sobretensão sustentada nem fusível: alimentar somente com 5 V regulados e corrente limitada.

USB-C foi considerado, mas a entrada THT de dois pinos foi escolhida pela montagem manual simples. Uma alimentação USB-C consumidora precisaria de `Rd` em CC1 e CC2 e de conector SMD. A escolha não implica que qualquer conector de dois pinos seja automaticamente à prova de erro: verificar polaridade de J1 antes de ligar.

## Validação reproduzível

`scripts/validate_logic_gates.sh` regenera fontes e BOM e executa ERC/DRC com KiCad 9.0.2. O resultado em 2026-10-27 foi 0 violações ERC, 0 violações DRC, 0 pads sem conexão, 0 erros de footprint e 0 problemas de paridade. `scripts/check_logic_gates_netlist.py` comparou 98 identidades de pin/pad e 44 valores/footprints da netlist exportada com a PCB e confirmou zona GND preenchida. Largura mínima de trilha é 0,35 mm, clearance mínimo de cobre é 0,20 mm, vias 0,8/0,4 mm e a placa tem duas camadas. Os pads de TO-92 padrão KiCad têm espaçamento nominal de 0,22 mm; o mínimo de 0,20 mm foi escolhido por causa desse footprint e precisa estar dentro da capacidade do fabricante selecionado.

O ngspice 44.2 foi executado de pacote Debian extraído temporariamente sem instalação global. `scripts/simulate_logic_gates.py` usa modelos simplificados `BF=80`, diodo Schottky e LED aproximados. Em 4,75–5,25 V de entrada, o pior alto observado foi **3,837 V**, o pior baixo foi **0,058 V**, e o máximo de corrente nos LEDs acesos foi **2,171 mA**. Os doze pontos e tensões de coletor estão em `boards/01-logic-gates/reports/simulation.csv`. Foram adotados alto ≥3,5 V e baixo ≤0,4 V. Esses resultados não cobrem tolerâncias completas, envelhecimento, temperatura extrema, bounce dos botões ou cargas externas. Os LEDs têm drivers separados para limitar a carga nas saídas lógicas.

Os Gerbers, drills, PDFs, BOM, GLB e STEP foram gerados pela CLI e estão em `boards/01-logic-gates/manufacturing/`. O modelo 3D dos botões é uma aproximação dimensional: o modelo B3F correspondente não está no pacote KiCad local; um modelo KiCad de botão de 6 mm foi escalado em X/Y para o corpo de 12 mm. A prévia PNG isométrica é ilustrativa, não captura do visualizador 3D. Não há `DISPLAY`/renderizador 3D interativo nesta sessão. A inspeção frontal e traseira foi feita pelas exportações SVG/PNG; a placa ainda precisa de revisão física do protótipo.
