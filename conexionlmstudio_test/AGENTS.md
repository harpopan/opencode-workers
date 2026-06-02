# AGENTS.md

## Proyecto

Template de proyecto con OpenCode conectado a LM Studio (modelo local).

## Configuracion

La unica fuente de verdad es `opencode.json`.

## Reglas

1. **Planificacion**: Desglosar cada solicitud en tareas atomicas.
2. **Lectura Selectiva**: Evitar leer archivos completos si superan 200 lineas. Usar busqueda por rangos o `grep`.
3. **Puntos de Control**: Tras cada sub-tarea, informar progreso.
4. **Codigo**: Seguir las convenciones existentes del proyecto. No añadir comentarios a menos que se solicite.
5. **Verificacion**: Ejecutar lint y typecheck al finalizar.
