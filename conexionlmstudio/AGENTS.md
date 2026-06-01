# AGENTS.md

## Proyecto

Conexión de OpenCode con LM Studio para uso de modelos locales.

## Configuracion

La unica fuente de verdad es `opencode.json`.

## Archivos del Proyecto

| Archivo | Proposito |
|---------|-----------|
| `opencode.json` | Configuracion principal (provider, modelos, opciones) |
| `README.md` | Documentacion general del proyecto |
| `AGENTS.md` | Este archivo — guia operativa para el agente |
| `GUIA_LMSTUDIO.md` | Guia detallada de configuracion de LM Studio |
| `ESTRUCTURA_PROYECTO.md` | Estructura de archivos del proyecto |

## Gestion de Contexto (Modelo Local)

Dado que se utiliza **Gemma 4 E4B** con contexto limitado (`limit.context: 14096`), el agente DEBE seguir estas reglas:

1. **Planificacion Obligatoria**: Antes de cualquier ejecucion tecnica, desglosar la solicitud en tareas atomicas en `task.md`. Ninguna tarea debe abarcar mas de un componente logico a la vez.
2. **Enfoque de Lectura Selectiva**: Evitar leer archivos completos si superan las 200 lineas. Usar lectura por rangos o `grep_search` para localizar fragmentos especificos.
3. **Puntos de Control y Reseteo**: Tras completar cada sub-tarea del `task.md`, informar del progreso. Se recomienda al usuario reiniciar la conversacion si nota lentitud o perdida de coherencia.
4. **Resumenes Post-Tarea**: Al finalizar un bloque de trabajo, generar un resumen conciso de los cambios para que el usuario pueda iniciar una nueva sesion con el contexto fresco.
5. **Reasoning activado**: El modelo soporta `reasoning_content` interleaved. El agente puede mostrar su cadena de razonamiento cuando sea util.
