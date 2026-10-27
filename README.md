# Open Hardware Projects

Repositório para projetos independentes de hardware aberto. O primeiro é a coleção didática do PET Engenharia Elétrica UFC, em [`projects/pet-eletrica-ufc/`](projects/pet-eletrica-ufc/).

## Organização

- `projects/`: projetos autocontidos, cada um com contexto, documentação e placas.
- `shared/`: automação, bibliotecas e templates realmente reutilizáveis.
- `docs/`: convenções aplicáveis ao repositório inteiro.

Cada placa deve manter seus arquivos-fonte KiCad e documentação junto ao projeto. Relatórios e arquivos de fabricação só devem ser apresentados como resultados quando gerados e revisados com ferramentas reais. Consulte [AGENTS.md](AGENTS.md) antes de contribuir.

## Ambiente observado

No levantamento de 2026-10-27, o worktree estava limpo em `main`, acompanhando `origin/main`. O ambiente é Debian GNU/Linux 13.7, com KiCad, `kicad-cli` e `pcbnew` 9.0.2 instalados. A interface gráfica não foi validada nesta sessão sem `DISPLAY`. Consulte [`projects/pet-eletrica-ufc/PROJECT_CONTEXT.md`](projects/pet-eletrica-ufc/PROJECT_CONTEXT.md) para os limites e decisões do projeto PET.
