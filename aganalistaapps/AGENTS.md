# AGENTS.md

## Project Purpose

Analyze application requirements from input files and generate development time estimates.

## Workflow

1. **Input**: Place requirement files (`.md` or `.txt`) in `input/`
2. **Analyze**: Prompt agent to analyze requirements (analista.md)
3. **Document**: Generate documentation with diagrams (documentador.md)
4. **Maintain** (optional): If maintenance horizon specified, invoke mantenedor.md
5. **Contents** (optional): If content implementation required, invoke contenidos.md

## Directories

- `input/` - Requirement files (.md or .txt)
- `output/` - Generated analysis files (*_analisis.md, *_documentacion.md, *_mantenimiento.md, *_contenidos.md)
- `agents/` - Agent definitions (analista.md, documentador.md, mantenedor.md, contenidos.md)
- `.agents/skills/` - Available skills (documentation, mermaid-diagrams)

## Estimation Principle

**Always estimate conservatively** (round up):
- Safety factor: 1.5x-2x on base estimate
- Testing: 40-50% of development time (not 20%)
- Always round to next whole day/hour

## Skills

- `documentation` - Trigger with "write docs for", "document this"
- `mermaid-diagrams` - Trigger with "diagram", "visualize"