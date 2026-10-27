# Instruções para agentes

## Projeto
Desenvolvemos hardware didático aberto para o PET Engenharia Elétrica UFC. Preserve os arquivos-fonte KiCad, explique decisões elétricas em `PROJECT_CONTEXT.md` e nunca declare validação, fabricação ou teste físico sem evidência reproduzível.

## Fluxo de trabalho
- Antes de editar, confira o estado Git e os arquivos existentes.
- Use scripts determinísticos para tarefas repetitivas; preserve os comandos e dependências.
- Para alterações elétricas, confira datasheets, ERC, DRC e conectividade; um DRC limpo não prova funcionamento.
- Não faça commits sem autorização expressa do mantenedor.
- Nunca invente logs ou resultados de engenharia. Registre indisponibilidade de ferramentas como limitação.
- Preserve SVGs e cores oficiais; até serem fornecidos, use identidade provisória claramente identificada.
- Mantenha a documentação didática acessível em português e os identificadores técnicos em inglês quando útil.

## KiCad
- O alvo é KiCad 10 quando suportado; valide a versão real disponível antes de usar recursos específicos.
- Prefira arquivos-fonte e CLI para validação/exportação; use API Python/IPC apenas após confirmar disponibilidade e compatibilidade.
- Antes de liberar fabricação, verifique ERC/DRC, contorno, furos, polaridades, BOM, Gerbers e drill files.
