# Fabricação — placa 01, revisão A

Este diretório é gerado por `../../../scripts/export_logic_gates.sh` a partir das fontes KiCad. A revisão A passou ERC, DRC e paridade sem violações no KiCad 9.0.2. O comportamento foi simulado com modelos simplificados; **não houve protótipo físico nem teste de montagem**. Encomende primeiro um pequeno lote piloto e inspecione a prévia do fabricante.

## Pedido sugerido

- PCB de **2 camadas**, FR-4 de **1,6 mm**, cobre **1 oz**.
- Contorno **123 × 155 mm**, cantos arredondados R3 mm.
- Máscara de solda **branca** e serigrafia **preta** solicitadas explicitamente. Gerbers não especificam a cor. Confirmar disponibilidade, contraste e legibilidade no visualizador da fábrica.
- Capacidade mínima do fabricante: trilha **0,35 mm**, clearance **0,20 mm**, via **0,8/0,4 mm**; verificar também o espaçamento de **0,22 mm** entre pads adjacentes no footprint TO-92.
- Furos PTH para componentes e vias; furos NPTH são pinos de posicionamento dos cinco botões. Não converter NPTH em metalizados. Não há furos de fixação.
- Revisar a polaridade de J1, D1 e dos LEDs na prévia. Não assumir que a faixa de um diodo indica ânodo.

## Gerbers e furação

| Arquivo em `gerbers/` | Uso |
|---|---|
| `01-logic-gates-F_Cu.gtl` | cobre superior |
| `01-logic-gates-B_Cu.gbl` | cobre inferior e plano GND |
| `01-logic-gates-F_Mask.gts` | abertura de máscara superior |
| `01-logic-gates-B_Mask.gbs` | abertura de máscara inferior |
| `01-logic-gates-F_Silkscreen.gto` | serigrafia superior |
| `01-logic-gates-B_Silkscreen.gbo` | serigrafia inferior |
| `01-logic-gates-Edge_Cuts.gm1` | contorno fechado |
| `01-logic-gates-F_Fab.gbr` / `B_Fab.gbr` | desenhos auxiliares de montagem, não camadas físicas da PCB |
| `01-logic-gates-job.gbrjob` | descrição do conjunto Gerber |

`drill/01-logic-gates-PTH.drl` e `drill/01-logic-gates-NPTH.drl` são Excellon em milímetros. Os PDFs `*-drl_map.pdf` permitem conferir posição e diâmetro dos furos. Envie Gerbers de cobre, máscara, silk, contorno e ambos os drills ao fabricante; os desenhos Fab são referência opcional.

## Outras entregas

- `BOM.csv`: referências, valores, footprints e quantidades, exportados do esquemático.
- `schematic.pdf`: circuito completo em uma folha A3; `front-assembly.pdf`, `back-assembly.pdf`, `front-layout.svg`, `back-layout.svg`: vistas de inspeção.
- `01-logic-gates.step` e `01-logic-gates.glb`: modelos 3D exportados pela CLI KiCad. Os botões usam um modelo KiCad de 6 mm escalado em X/Y para aproximar o corpo Omron de 12 mm, porque o modelo B3F específico não está instalado; **não usar esse detalhe do modelo para verificar colisões mecânicas finas**.
- `ERC.rpt`, `DRC.rpt` e `simulation.csv`: evidência reproduzível da revisão. Os relatórios registram zero erros de ERC/DRC e a simulação cobre 4,75, 5,00 e 5,25 V.

## Pendências antes da liberação além do protótipo

1. Confirmar os part numbers exatos dos componentes comprados, principalmente pinagem real do 2N3904 e geometria do B3F-4050.
2. Confirmar a máscara branca/serigrafia preta na prévia do fabricante e conferir que o detalhe da logo continua legível.
3. Montar um protótipo, medir todas as tabelas-verdade e o consumo e registrar os resultados no guia de laboratório.
4. Revisar alcance mecânico dos botões e do conector no produto final. O 3D dos botões é uma aproximação.
