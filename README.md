# PET Hardware

Coleção modular de placas educacionais de eletrônica digital do PET Engenharia Elétrica UFC. O projeto começa com uma placa de portas lógicas e evolui em direção a uma ALU e a um computador didático.

## Estado inicial

O ambiente detectado é Debian GNU/Linux 13 (Trixie), kernel 6.12, Python 3.13.5. KiCad e `kicad-cli` não estão instalados; o repositório APT configurado oferece KiCad 9.0.2. A versão upstream consultada é 10.0.6. Não havia arquivos SVG, imagem de referência nem repositório Git preexistentes.

Não há ainda resultados ERC/DRC nem projeto fabricável. A criação e validação dos projetos KiCad dependerá da instalação do KiCad e do fornecimento dos ativos oficiais da identidade visual.

## Estrutura

- `identity/`: logotipos, paleta e guia visual
- `libraries/`: símbolos e footprints locais
- `templates/`: convenções reutilizáveis de placa
- `scripts/`: automação reprodutível
- `boards/logic-gates/`: primeira placa
- `docs/`: decisões e material didático
- `manufacturing/`: saídas verificadas de fabricação
- `reports/`: relatórios gerados por ferramentas reais

Ver [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) e [AGENTS.md](AGENTS.md).
