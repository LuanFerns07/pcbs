# Automação EDA: avaliação inicial

O caminho recomendado é Python para preparar conteúdo determinístico, KiCad CLI para ERC/DRC e exports, e uso gráfico limitado a inspeção. O CLI oficial documenta comandos `sch`, `pcb`, `gerber`, `fp`, `sym` e `api-server`; sua presença depende da instalação local.

`pcbnew` é uma API Python acoplada à instalação/versão do KiCad, portanto não se presume compatibilidade com Python do sistema. A disponibilidade do servidor IPC/API depende da versão e do editor em execução. KiCad 10 deve ser a meta se instalado; o repositório Debian configurado oferece 9.0.2, cuja compatibilidade upstream pode ser preferível a misturar pacotes externos.

MCP serve melhor para consultas contextualizadas e alterações interativas. Antes de adoção, verificar licença, atividade, versão KiCad suportada, transporte IPC e ferramentas realmente implementadas; testar em cópia. Nenhum servidor foi instalado.

Estimativas de tokens são qualitativas. A economia real deve ser medida em uma tarefa representativa, incluindo prompt, chamadas e respostas, em vez de inventar números.
