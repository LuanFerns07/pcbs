# Hardware didático do PET Engenharia Elétrica UFC

Coleção aberta de placas para estudar blocos fundamentais de computadores digitais, começando por portas lógicas e avançando para circuitos combinacionais, sequenciais, memória e uma ALU.

## Estrutura

- `boards/01-logic-gates/`: primeira placa planejada (AND, OR e NOT).
- `docs/`: roteiros didáticos e notas específicas.
- `assets/logos/`: imagem PET fornecida para identidade visual.
- `identity/`: ativos e padrões visuais do projeto.
- `libraries/`, `scripts/`, `templates/`: recursos locais reutilizáveis.

O estado de engenharia, decisões elétricas e limitações estão em [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md). As regras locais estão em [`AGENTS.md`](AGENTS.md). O esquemático da placa 01 passou ERC. Existe PCB preliminar; o DRC aponta 54 pads sem rota, e os arquivos de fabricação ainda não foram produzidos.
