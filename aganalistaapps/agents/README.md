# Registro de Agentes

Este directorio contiene los subagentes reutilizables del proyecto.

## Agentes Disponibles

| Agent | Archivo | Descripción |
|-------|---------|-------------|
| Analista | `analista.md` | Analiza requisitos de aplicaciones y calcula estimaciones de tiempo de desarrollo |
| Documentador | `documentador.md` | Transforma análisis técnicos en documentación profesional y estructurada |

## Uso en otros proyectos

Para reutilizar estos agentes en otros proyectos OpenCode:

1. Copiar la carpeta `agents/` al nuevo proyecto
2. O referenciar desde la ubicación original usando el parámetro `prompt` del Task tool

### Ejemplo de uso

```
Task(description="Analizar requisitos", prompt="Usa el agente Analista en agents/analista.md para analizar el archivo input/requisitos.md", subagent_type="general")
```

## Propósito del pipeline

```
input/ (requisitos.md)
    │
    ▼
[Agente Analista] ──▶ output/<nombre>_analisis.md
    │                         │
    │                         ▼
    │              [Agente Documentador]
    │                         │
    ▼                         ▼
              output/<nombre>_documentacion.md
```