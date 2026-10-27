# Hardware didático do PET Engenharia Elétrica UFC

Coleção aberta de placas para estudar blocos fundamentais de computadores digitais, começando por portas lógicas e avançando para circuitos combinacionais, sequenciais, memória e uma ALU.

## Estrutura

- `boards/01-logic-gates/`: placa 01 com AND, OR e NOT por transistores discretos.
- `docs/`: roteiros didáticos e notas específicas.
- `assets/logos/`: imagem PET fornecida para identidade visual.
- `identity/`: ativos e padrões visuais do projeto.
- `libraries/`, `scripts/`, `templates/`: recursos locais reutilizáveis.

O [projeto da placa 01](boards/01-logic-gates/README.md) reúne fontes KiCad, imagens, BOM, simulação e arquivos de fabricação. A revisão A passou ERC/DRC e paridade com zero violações; um protótipo físico ainda não foi fabricado ou medido. Decisões elétricas e limites estão em [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md); as regras locais estão em [`AGENTS.md`](AGENTS.md).
