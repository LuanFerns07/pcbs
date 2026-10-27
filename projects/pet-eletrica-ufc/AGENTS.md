# Instruções do projeto PET

- Ensine eletrônica digital com documentação em português claro; mantenha nomes de sinais e identificadores técnicos em inglês quando isso facilitar interoperabilidade.
- Organize cada placa independentemente em `boards/NN-name/`, incluindo fontes KiCad, BOM e material de montagem junto à placa.
- Explique em `PROJECT_CONTEXT.md` as decisões elétricas, hipóteses, fontes e limitações.
- Entradas CMOS devem ter nível definido; dimensione resistores, LEDs, desacoplamento e proteção com base em datasheets dos componentes escolhidos.
- Prefira THT e componentes acessíveis quando não houver prejuízo técnico. Registre fabricante e código de componente para escolhas críticas.
- Preserve a arte oficial do PET. Enquanto SVGs e cores oficiais não forem fornecidos, use apenas identidade provisória textual claramente identificada.
- Documente objetivo, teoria, componentes, tabelas-verdade, procedimento, resultados esperados, exercícios e expansões para cada experimento.
- Antes de recomendar fabricação, confira ERC, DRC, conectividade, polaridades, contorno, furos, BOM, Gerbers, drills e vistas 2D/3D. DRC limpo não substitui revisão funcional.
- Não declare validação elétrica, fabricação ou teste físico sem evidência reproduzível; registre pendências explicitamente.
