# AGENTS.md

## 📦 Project Type

More details to be defined.

## 🔌 Configuration

The single source of truth is `opencode.json`.

---

## 📚 Related Files

| File | Purpose |
|------|---------|
| `opencode.json` | Runtime configuration |
| `README.md` | Project documentation |
| `AGENTS.md` | This file — agent operational guidance |

---

## 🧠 Gestión de Contexto (Modelo Local)

Dado que se utiliza un modelo local con contexto limitado (LM Studio), el agente DEBE seguir estas reglas estrictas para garantizar la estabilidad:

1. **Planificación Obligatoria**: Antes de cualquier ejecución técnica, desglosar la solicitud en tareas atómicas en `task.md`. Ninguna tarea debe abarcar más de un componente lógico a la vez.
2. **Enfoque de Lectura Selectiva**: Evitar leer archivos completos si superan las 200 líneas. Utilizar lectura por rangos o `grep_search` para localizar fragmentos específicos.
3. **Puntos de Control y Reseteo**: Tras completar cada sub-tarea del `task.md`, el agente debe informar del progreso. Se recomienda al usuario reiniciar la conversación si nota lentitud o pérdida de coherencia, para limpiar el historial de tokens.
4. **Resúmenes Post-Tarea**: Al finalizar un bloque de trabajo, generar un resumen conciso de los cambios para que el usuario pueda iniciar una nueva sesión con el contexto fresco si fuera necesario.