# opencode-workers

Recopilación de **agentes**, **skills** y **scripts** para aplicaciones de IA (OpenCode y similares).

Este repositorio agrupa piezas reutilizables que cubren desde el análisis de requisitos y la documentación automática de proyectos, hasta la configuración de OpenCode contra LMStudio y temas visuales para la TUI.

---

## Mapa de contenidos

### 1. `aganalistaapps` — Análisis de requisitos y estimaciones

Sistema de análisis de requisitos de aplicaciones y estimación de tiempos de desarrollo (v1.3.0).

- **Agentes** (`agents/`): `analista`, `documentador`, `mantenedor`, `contenidos`.
- **Skills** (`.agents/skills/`): `documentation`, `mermaid-diagrams`.
- **Flujo**: `input/` (requisitos) → `output/` (análisis, documentación, mantenimiento y contenidos).
- **Estimaciones**: enfoque conservador (factor 1.5x–2x, testing 40–50%, redondeo al alza).
- **Extras**: `AGENTS.md`, `skills-lock.json` (origen de skills), tema `browniecacsa` (`tui.json`).

> Documentación completa en [`aganalistaapps/README.md`](aganalistaapps/README.md).

### 2. `agdocumentador` — Documentación técnica de proyectos

Agente de documentación diseñado para desplegarse sobre proyectos en curso (v1.4).

- **Pipeline**: `explorer → diagrams → writer → validator`.
- **Subagentes** (`.agents/agents/`): `explorer`, `writer`, `diagrams`, `validator` (valida la doc contra el código real).
- **Skills** (`.agents/skills/`): `documentation`, `mermaid-diagrams`.
- **Salida**: documentación generada en `docs_ocode/`.
- **Extras**: `AGENTS.md`, `.opencode-config.json`, workspace de VS Code y tema propio `agentedocumentador`.

### 3. `agents_templates` — Plantillas y convenciones

Plantillas base para estandarizar proyectos con agentes.

- **`AGENTS - Template.md`**: documento maestro de reglas base, subagentes, skills y ritual de cierre.
- **`docs/`**:
  - `MAP - DOCUMENTACION.md` — índice/mapa central de documentación.
  - `REF - TAXONOMIA DEVS.md` — taxonomía de documentos, frontmatter YAML, estados y prefijos (`REF-`, `PROY-`, `GUIA-`, `LOG-`, etc.).

### 4. `configurador_opencode_local` — OpenCode + LMStudio

Scripts para configurar OpenCode contra LMStudio local.

- **`configurar-opencode-lin.sh`** / **`configurar-opencode-win.ps1`**: detectan los modelos de LMStudio y generan `opencode.jsonc` (con backup previo).
- **`monitor-logs-lmstudio/`**: panel TUI (`lmstudio-monitor.py`) para monitorizar logs y métricas del servidor LMStudio en tiempo real.
- **Extras**: `opencode.jsonc` de ejemplo y temas `laboratoriodelahermita` / `solaria`.

> Documentación completa en [`configurador_opencode_local/README.md`](configurador_opencode_local/README.md).

### 5. `themes` — Temas para la TUI de OpenCode

Colección de temas visuales (formato `theme.json` de OpenCode):

| Tema | Descripción |
|------|-------------|
| `ejemplo-oficial.json` | Paleta Nord (referencia oficial) |
| `laboratorio-cian_magenta.json` | Cian + magenta reactivo |
| `laboratorio-hueso_fluor.json` | Laboratorio hueso fluor |
| `mandarina.json` | Paleta mandarina |
| `nautilus.json` | Paleta nautilus |
| `samjoko_v2.json` | Paleta samjoko |
| `solaria.json` | Paleta solaria |
| `test-rojo-rosa-cantoso.json.json` | Test rojo/rosa |

---

## Resumen rápido

| Carpeta | Qué aporta | Tipo |
|---------|-----------|------|
| `aganalistaapps` | Análisis de requisitos + estimación de tiempos | Agentes + skills |
| `agdocumentador` | Documentación técnica automática de proyectos | Agentes + skills |
| `agents_templates` | Plantillas de `AGENTS.md` y taxonomía de docs | Plantillas |
| `configurador_opencode_local` | Configuración OpenCode ↔ LMStudio + monitor | Scripts |
| `themes` | Temas visuales para la TUI | Temas |
