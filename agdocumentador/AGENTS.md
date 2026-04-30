---
version: 1.4
---
# AGENTS.md

## Propósito

Agente de documentación técnica diseñado para ser **desplegado sobre proyectos en curso**. Analiza y documenta proyectos existentes desde OpenCode, ejecutando subagentes en paralelo para generar:

- Documentación de arquitectura
- Diagramas técnicos (ERD, sequence, flowchart, C4)
- README y guías de uso
- Documentación de APIs
- Runbooks y guías de operación

## Despliegue

Este agente puede desplegarse sobre cualquier proyecto que ya tenga desarrollo iniciado. Los subagentes y skills se ejecutan desde OpenCode en paralelo para analizar y documentar el proyecto objetivo.

## Skills Disponibles

### documentation
Genera documentación técnica estructurada:
- README, API docs, Runbooks
- Arquitectura y diseño
- Guías de onboarding

### mermaid-diagrams
Crea diagramas técnicos en sintaxis Mermaid:
- Diagrams ERD, sequence, flowchart
- C4 architecture
- Class diagrams, state diagrams

## Agentes

### explorer
Analiza proyectos a nivel técnico:
- Tech stack y dependencias
- Estructura de directorios
- API endpoints y modelos
- Patrones de arquitectura

### writer
Genera documentación basada en análisis:
- README y guías
- Documentación de arquitectura
- Runbooks de operación

### diagrams
Crea diagramas Mermaid:
- C4 (System, Container, Component)
- ERD y modelos de datos
- Sequence diagrams
- Flowcharts y estados

### AGDOC_validator
Valida documentación y diagramas contra el código real del proyecto:
- Cruza endpoints documentados con rutas reales
- Verifica ERD contra esquemas de base de datos
- Valida ejemplos de código con firmas reales
- Genera reporte de discrepancias

## Flujo de Uso

```
AGDOC_explorer → AGDOC_diagrams → AGDOC_writer → AGDOC_validator
```

1. **AGDOC_explorer**: Analiza el proyecto y genera informe técnico
2. **AGDOC_diagrams**: Crea diagramas basados en el análisis
3. **AGDOC_writer**: Genera documentación completa con diagramas
4. **AGDOC_validator**: Valida la documentación generada contra el código del proyecto

## Estructura

```
.agents/
├── docs_ocode/           ← Documentación de salida (siempre por defecto)
├── skills/
│   ├── documentation/
│   └── mermaid-diagrams/
├── agents/
│   ├── explorer/
│   ├── writer/
│   ├── diagrams/
│   └── AGDOC_validator/
└── AGENTS.md
```

## Ubicación de Salida

:file_folder: ** Toda la documentación debe generarse en: `/docs_ocode/` **
(excepto si el usuario indica explícitamente otra ruta)

## Theme

El proyecto utiliza por defecto el theme **theme-documentators.json** con paleta de colores amarillos:
- Archivo: `theme-documentators.json`
- Colores: Amarillo dorado (#FFD700) como primario
- Incluye configuración para diagramas Mermaid

## Comandos Common

- `npm run lint` - Validar código
- `npm run typecheck` - Verificar tipos