# Automação EDA

## Arquitetura adotada

Usar arquivos nativos KiCad como fonte de verdade, scripts locais determinísticos para tarefas repetitivas e `kicad-cli` para ERC/DRC, exportações e renderização quando a versão oferecer os comandos necessários. A inspeção gráfica fica para revisões visuais pontuais. Essa divisão mantém o fluxo reproduzível e reduz interações repetidas com o modelo sem presumir economia numérica de tokens.

Python pode preparar dados e automatizar operações, mas a API `pcbnew` está vinculada à versão/instalação do KiCad. Confirmar `pcbnew.GetBuildVersion()` e compatibilidade antes de usar um script. Gerar ou editar S-expressions diretamente só quando houver validação com o parser/CLI correspondente.

MCP/IPC não é dependência inicial: a CLI e `pcbnew` estão disponíveis localmente em 9.0.2. MCP pode ser avaliado para uma tarefa interativa concreta, após conferir licença, manutenção, compatibilidade da versão e ferramentas implementadas, sempre em cópia do projeto. Não foi instalado nem testado servidor MCP; tampouco foi medida utilização de tokens.

## Ambiente verificado em 2026-10-27

- Debian GNU/Linux 13.7 (Trixie), Python 3.13.5.
- `kicad-cli version`: 9.0.2.
- `pcbnew.GetBuildVersion()`: 9.0.2+dfsg-1.
- O pacote Debian configurado oferece 9.0.2; não se misturaram repositórios ou pacotes externos para instalar KiCad 10.
- `kicad-cli --help` confirmou os grupos `sch`, `pcb`, `fp`, `sym` e `jobset`; `sch` lista `erc`/`export`, `pcb` lista `drc`/`export`/`render`. O esquemático da placa 01 foi exportado como netlist e passou ERC com zero violações; ainda não existe PCB para validar por DRC.
- A invocação da interface `kicad --version` sem `DISPLAY` falhou ao inicializar GTK e não é considerada verificação da GUI.

Repetir o levantamento com `shared/scripts/environment_report.sh`. As versões podem mudar; registrar novas observações com data e saída reproduzível.
